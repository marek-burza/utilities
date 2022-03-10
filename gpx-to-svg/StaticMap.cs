using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace GpxToSvg
{
    public class Coordinates
    {
        public double Longitude { get; set; }
        public double Latitude { get; set; }

        public Coordinates(double longitude, double latitude)
        {
            Longitude = longitude;
            Latitude = latitude;
        }

        public override string ToString()
        {
            return $"({Longitude},{Latitude})";
        }
    }

    // Based loosely on: https://github.com/komoot/staticmap
    public class StaticMap
    {
        public const string TileServerBaseAddress = "a.tile.opentopomap.org";

        private readonly HttpClient http;

        public StaticMap(HttpClient http)
        {
            this.http = http;
        }

        private string BytesToDataURI(byte[] data, string mime)
        {
            StringBuilder uri = new StringBuilder();
            uri.Append($"data:{mime};base64,");
            uri.Append(Convert.ToBase64String(data));
            return uri.ToString();
        }

        private string StringToDataURI(string data, string mime)
        {
            StringBuilder uri = new StringBuilder();
            uri.Append($"data:{mime};base64,");
            uri.Append(Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(data)));
            return uri.ToString();
        }

        private (IList<Coordinates> places, IList<IList<Coordinates>> paths) ExtractGpx(string gpx)
        {
            IList<Coordinates> places = new List<Coordinates>();
            IList<IList<Coordinates>> paths = new List<IList<Coordinates>>();
            XmlDocument xmlDoc = new XmlDocument();
            xmlDoc.LoadXml(gpx);
            foreach (XmlElement wptElement in xmlDoc.GetElementsByTagName("wpt"))
            {
                double longitude = Double.Parse(wptElement.Attributes["lon"].Value);
                double latitude = Double.Parse(wptElement.Attributes["lat"].Value);
                places.Add(new Coordinates(longitude, latitude));
            }
            foreach (XmlElement trksegElement in xmlDoc.GetElementsByTagName("rte"))
            {
                IList<Coordinates> path = new List<Coordinates>();
                paths.Add(path);
                foreach (XmlElement trkptElement in trksegElement.GetElementsByTagName("rtept"))
                {
                    double longitude = Double.Parse(trkptElement.Attributes["lon"].Value);
                    double latitude = Double.Parse(trkptElement.Attributes["lat"].Value);
                    path.Add(new Coordinates(longitude, latitude));
                }
            }
            foreach (XmlElement trksegElement in xmlDoc.GetElementsByTagName("trkseg"))
            {
                IList<Coordinates> path = new List<Coordinates>();
                paths.Add(path);
                foreach (XmlElement trkptElement in trksegElement.GetElementsByTagName("trkpt"))
                {
                    double longitude = Double.Parse(trkptElement.Attributes["lon"].Value);
                    double latitude = Double.Parse(trkptElement.Attributes["lat"].Value);
                    path.Add(new Coordinates(longitude, latitude));
                }
            }
            return (places, paths);
        }

        private (Coordinates minimum, Coordinates maximum) DetermineBounds(IList<Coordinates> places, IList<IList<Coordinates>> paths)
        {
            IList<Coordinates> all = new List<Coordinates>(places);
            foreach (IList<Coordinates> path in paths)
            {
                foreach (Coordinates place in path)
                {
                    all.Add(place);
                }
            }
            Coordinates minimum = new Coordinates(Double.MaxValue, Double.MaxValue);
            Coordinates maximum = new Coordinates(Double.MinValue, Double.MinValue);
            foreach (Coordinates place in all)
            {
                minimum.Longitude = Math.Min(place.Longitude, minimum.Longitude);
                maximum.Longitude = Math.Max(place.Longitude, maximum.Longitude);
                minimum.Latitude = Math.Min(place.Latitude, minimum.Latitude);
                maximum.Latitude = Math.Max(place.Latitude, maximum.Latitude);
            }
            return (minimum, maximum);
        }

        private double LongitudeToX(double longitude, int zoom)
        {
            if (!(-180.0 <= longitude && longitude <= 180.0))
            {
                longitude = (longitude + 180.0) % 360.0 - 180.0;
            }
            double x = ((longitude + 180.0) / 360.0) * (1 << zoom);
            return ((longitude + 180.0) / 360.0) * (1 << zoom);
        }

        private double LatitudeToY(double latitude, int zoom)
        {
            if (!(-90.0 <= latitude && latitude <= 90.0))
            {
                latitude = (latitude + 90.0) % 180.0 - 90.0;
            }
            double y = (1.0 - Math.Log(Math.Tan(latitude * Math.PI / 180.0) + 1.0 / Math.Cos(latitude * Math.PI / 180.0)) / Math.PI) / 2.0 * (1 << zoom);
            return (1.0 - Math.Log(Math.Tan(latitude * Math.PI / 180.0) + 1.0 / Math.Cos(latitude * Math.PI / 180.0)) / Math.PI) / 2.0 * (1 << zoom);
        }

        private int DetermineZoom(Coordinates minimum, Coordinates maximum, int width, int height, int paddingWidth, int paddingHeight, int tileSize)
        {
            for (int zoom = 17; zoom >= 0; zoom--)
            {
                double calculatedWidth = (LongitudeToX(maximum.Longitude, zoom) - LongitudeToX(minimum.Longitude, zoom)) * tileSize;
                if (calculatedWidth > (width - paddingWidth * 2))
                {
                    continue;
                }
                double calculatedHeight = (LatitudeToY(minimum.Latitude, zoom) - LatitudeToY(maximum.Latitude, zoom)) * tileSize;
                if (calculatedHeight > (height - paddingHeight * 2))
                {
                    continue;
                }
                return zoom;
            }
            return 0;
        }

        private int XToPixels(double x, double centerX, int tileSize, int width)
        {
            double px = (x - centerX) * tileSize + (width >> 1);
            return (int)Math.Round(px);
        }

        private int YToPixels(double y, double centerY, int tileSize, int height)
        {
            double px = (y - centerY) * tileSize + (height >> 1);
            return (int)Math.Round(px);
        }

        private async Task<string> GenerateBaseLayer(int width, int height, int tileSize, double centerX, double centerY, int zoom, bool reverseY)
        {
            StringBuilder baseLayer = new StringBuilder();
            int minX = (int)Math.Floor(centerX - (0.5 * width / tileSize));
            int minY = (int)Math.Floor(centerY - (0.5 * height / tileSize));
            int maxX = (int)Math.Ceiling(centerX + (0.5 * width / tileSize));
            int maxY = (int)Math.Ceiling(centerY + (0.5 * height / tileSize));
            IList<Task<byte[]>> tiles = new List<Task<byte[]>>();
            IList<int> xs = new List<int>();
            IList<int> ys = new List<int>();
            for (int x = minX; x < maxX; x++)
            {
                for (int y = minY; y < maxY; y++)
                {
                    int tileMax = 1 << zoom;
                    int tileX = (x + tileMax) % tileMax;
                    int tileY = (y + tileMax) % tileMax;
                    if (reverseY)
                    {
                        tileY = ((1 << zoom) - tileY) - 1;
                    }
                    xs.Add(x);
                    ys.Add(y);
                    tiles.Add(http.GetByteArrayAsync($"https://a.tile.opentopomap.org/{zoom}/{x}/{y}.png"));
                }
            }
            for (int index = 0; index < tiles.Count; index++)
            {
                string image = BytesToDataURI(await tiles[index], "image/png");
                int xPixel = XToPixels(xs[index], centerX, tileSize, width);
                int yPixel = YToPixels(ys[index], centerY, tileSize, height);
                baseLayer.Append($"<image href=\"{image}\" x=\"{xPixel}\" y=\"{yPixel}\" width=\"{tileSize}\" height=\"{tileSize}\"/>");
            }
            return baseLayer.ToString();
        }

        private string GenerateFeatureLayer(IList<Coordinates> places, IList<IList<Coordinates>> paths, int width, int height, int tileSize, double centerX, double centerY, int zoom)
        {
            StringBuilder featureLayer = new StringBuilder();
            foreach (IList<Coordinates> path in paths)
            {
                StringBuilder d = new StringBuilder();
                foreach (Coordinates place in path)
                {
                    double x = XToPixels(LongitudeToX(place.Longitude, zoom), centerX, tileSize, width);
                    double y = YToPixels(LatitudeToY(place.Latitude, zoom), centerY, tileSize, height);
                    if (d.Length == 0)
                    {
                        d.Append($"M {x},{y} L");
                    }
                    else
                    {
                        d.Append($" {x},{y}");
                    }
                }
                featureLayer.Append($"<path d=\"{d.ToString()}\" stroke=\"#FF0000\" stroke-width=\"2\" fill=\"none\"/>");
            }
            foreach (Coordinates place in places)
            {
                double x = XToPixels(LongitudeToX(place.Longitude, zoom), centerX, tileSize, width);
                double y = YToPixels(LatitudeToY(place.Latitude, zoom), centerY, tileSize, height);
                featureLayer.Append($"<circle cx=\"{x}\" cy=\"{y}\" r=\"3\" fill=\"#FFFF00\" stroke=\"none\"/>");
            }
            return featureLayer.ToString();
        }

        private async Task<string> GenerateSvg(IList<Coordinates> places, IList<IList<Coordinates>> paths, int width, int height, int paddingWidth, int paddingHeight, int tileSize, bool reverseY)
        {
            Coordinates minimum, maximum;
            (minimum, maximum) = DetermineBounds(places, paths);
            int zoom = DetermineZoom(minimum, maximum, width, height, paddingWidth, paddingHeight, tileSize);
            double centerX = LongitudeToX((minimum.Longitude + maximum.Longitude) / 2.0, zoom);
            double centerY = LatitudeToY((minimum.Latitude + maximum.Latitude) / 2.0, zoom);
            StringBuilder svg = new StringBuilder();
            svg.Append($"<svg width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" version=\"1.1\">");
            svg.Append(await GenerateBaseLayer(width, height, tileSize, centerX, centerY, zoom, reverseY));
            svg.Append(GenerateFeatureLayer(places, paths, width, height, tileSize, centerX, centerY, zoom));
            svg.Append("</svg>");
            return await Task.FromResult<string>(StringToDataURI(svg.ToString(), "image/svg+xml"));
        }

        public async Task<string> RenderAsync(string gpx)
        {
            IList<Coordinates> places;
            IList<IList<Coordinates>> paths;
            (places, paths) = ExtractGpx(gpx);
            return await GenerateSvg(places, paths, 1080, 1080, 0, 0, 256, false);
        }
    }
}