using Microsoft.AspNetCore.Components;
using Microsoft.JSInterop;
using System;
using System.Collections.Generic;
using System.Reflection;
using System.Text.Json;
using System.Threading.Tasks;
using FisSst.BlazorMaps;

namespace CommuteTimeMapper.Pages
{
    public partial class Index
    {
        private string point = "2 Kingdom St, London W2 6BD, UK";

        private LatLng location = new LatLng(51.519029, -0.181703);

        private string mode = BingMaps.ModeDriving;

        private Dictionary<string, string> modes = new Dictionary<string, string>()
        {
            { BingMaps.ModeDriving, "🚗" },
            { BingMaps.ModeTransit, "🚌" },
            { BingMaps.ModeWalking, "🚶" }
        };

        private PolygonOptions Time10 = new PolygonOptions() { Stroke = false, FillOpacity = 0.5, FillColor = "#0000FF" };  // Dark blue
        private PolygonOptions Time15 = new PolygonOptions() { Stroke = false, FillOpacity = 0.5, FillColor = "#0080FF" };  // Light blue
        private PolygonOptions Time20 = new PolygonOptions() { Stroke = false, FillOpacity = 0.5, FillColor = "#00FFFF" };  // Cyan
        private PolygonOptions Time25 = new PolygonOptions() { Stroke = false, FillOpacity = 0.5, FillColor = "#00FF00" };  // Green
        private PolygonOptions Time30 = new PolygonOptions() { Stroke = false, FillOpacity = 0.5, FillColor = "#FFFF00" };  // Yellow
        private PolygonOptions Time35 = new PolygonOptions() { Stroke = false, FillOpacity = 0.5, FillColor = "#FF8000" };  // Orange
        private PolygonOptions Time40 = new PolygonOptions() { Stroke = false, FillOpacity = 0.5, FillColor = "#FF0000" };  // Red
        private PolygonOptions Time45 = new PolygonOptions() { Stroke = false, FillOpacity = 0.5, FillColor = "#FF00FF" };  // Magenta
        private PolygonOptions Time50 = new PolygonOptions() { Stroke = false, FillOpacity = 0.5, FillColor = "#000000" }; // Black

        private int density = 10;

        private bool exploring = false;
        private double progress = 100;

        private readonly LatLng center;
        private Map mapRef;
        private MapOptions mapOptions;

        private List<Polygon> polygons = new List<Polygon>();

        [Inject]
        private IPolygonFactory PolygonFactory { get; init; }

        public Index()
        {
            this.center = location;
            this.mapOptions = new MapOptions()
            {
                DivId = "mapId",
                Center = center,
                Zoom = 11,
                UrlTileLayer = "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
                SubOptions = new MapSubOptions()
                {
                    Attribution = "&copy; <a lhref='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>",
                    MaxZoom = 18,
                    TileSize = 256,
                    ZoomOffset = 0,
                }
            };
        }

        [Inject]
        private BingMaps BingMapsHttp { get; set; }

        private async void Go()
        {
            location = await BingMapsHttp.QueryLocation(point);
            await mapRef.SetView(location);
            await mapRef.SetZoom(zoom: 11);
        }

        private async void Explore()
        {
            progress = 0;
            exploring = true;
            double height, width;
            (height, width) = await GetBounds();
            double step = Math.Min(height, width) / density;
            LatLng center = await mapRef.GetCenter();
            LatLng destination = location;
            double length = (height / step) * (width / (2 * step));
            foreach (Polygon polygon in polygons)
            {
                await polygon.Remove();
            }
            for (int y = 0; y < height / step; y++)
            {
                for (int x = 0; x < width / (2 * step); x++)
                {
                    LatLng origin = new LatLng(
                        center.Lat + (height / 2) - (y + 0.5) * step,
                        center.Lng - (width / 2) + (x + 0.5) * (2 * step));
                    int duration = await BingMapsHttp.QueryCommute(mode, origin, destination);
                    Polygon polygon = await this.PolygonFactory.CreateAndAddToMap(Square(origin, step), this.mapRef);
                    await polygon.SetStyle(Style(duration / 60));
                    polygons.Add(polygon);
                    double index = y * width / (2 * step) + x;
                    progress = 100 * index / length;
                    StateHasChanged();
                }
            }
            exploring = false;
            StateHasChanged();
        }

        private async Task<(double, double)> GetBounds()
        {
            PropertyInfo property = typeof(Map).GetProperty("MapReference", BindingFlags.NonPublic | BindingFlags.Instance);
            MethodInfo getter = property.GetGetMethod(nonPublic: true);
            IJSObjectReference MapReference = (IJSObjectReference)getter.Invoke(mapRef, null);
            JsonElement result = await MapReference.InvokeAsync<JsonElement>("getBounds");
            double south = result.GetProperty("_southWest").GetProperty("lat").GetDouble();
            double west = result.GetProperty("_southWest").GetProperty("lng").GetDouble();
            double north = result.GetProperty("_northEast").GetProperty("lat").GetDouble();
            double east = result.GetProperty("_northEast").GetProperty("lng").GetDouble();
            double width = Math.Abs(west - east);
            double height = Math.Abs(north - south);
            return (height, width);
        }

        private PolygonOptions Style(int time)
        {
            PolygonOptions styled = Time50;
            if (time >= 45)
            {
                styled = Time50;
            }
            else if (time >= 40)
            {
                styled = Time45;
            }
            else if (time >= 35)
            {
                styled = Time40;
            }
            else if (time >= 30)
            {
                styled = Time35;
            }
            else if (time >= 25)
            {
                styled = Time30;
            }
            else if (time >= 20)
            {
                styled = Time25;
            }
            else if (time >= 15)
            {
                styled = Time20;
            }
            else if (time >= 10)
            {
                styled = Time15;
            }
            else
            {
                styled = Time10;
            }
            return styled;
        }

        private List<LatLng> Square(LatLng spot, double step)
        {
            List<LatLng> squared = new List<LatLng>();
            LatLng ne = new LatLng(spot.Lat + 0.5 * step, spot.Lng + step);
            squared.Add(ne);
            LatLng se = new LatLng(spot.Lat - 0.5 * step, spot.Lng + step);
            squared.Add(se);
            LatLng sw = new LatLng(spot.Lat - 0.5 * step, spot.Lng - step);
            squared.Add(sw);
            LatLng nw = new LatLng(spot.Lat + 0.5 * step, spot.Lng - step);
            squared.Add(nw);
            return squared;
        }
    }
}
