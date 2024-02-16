using System;
using System.Collections.Specialized;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using System.Threading.Tasks;
using System.Web;
using FisSst.BlazorMaps;

namespace CommuteTimeMapper
{
    public class BingMaps
    {
        private const string BingMapsApiKey = "$BING_MAPS_API_KEY";

        internal const string ModeDriving = "driving";
        internal const string ModeTransit = "transit";
        internal const string ModeWalking = "walking";
        internal readonly string[] Modes = { ModeTransit, ModeDriving, ModeWalking };

        private readonly HttpClient http;

        public BingMaps(HttpClient http)
        {
            this.http = http;
        }

        public async Task<LatLng> QueryLocation(string location)
        {
            NameValueCollection query = HttpUtility.ParseQueryString(string.Empty);
            query["q"] = location;
            query["o"] = "json";
            query["key"] = BingMapsApiKey;
            query["maxResults"] = "1";
            UriBuilder builder = new UriBuilder("https://dev.virtualearth.net/REST/v1/Locations/");
            builder.Port = -1;
            builder.Query = query.ToString();
            string url = builder.ToString();
            JsonElement result = await http.GetFromJsonAsync<JsonElement>(url);
            result = result.GetProperty("resourceSets")[0].GetProperty("resources")[0].GetProperty("point").GetProperty("coordinates");
            return new LatLng(result[0].GetDouble(), result[1].GetDouble());
        }

        public async Task<int> QueryCommute(string mode, LatLng fromHere, LatLng toThere)
        {
            NameValueCollection query = HttpUtility.ParseQueryString(string.Empty);
            query["wp.0"] = $"{fromHere.Lat},{fromHere.Lng}";
            query["wp.1"] = $"{toThere.Lat},{toThere.Lng}";
            query["o"] = "json";
            query["key"] = BingMapsApiKey;
            query["optmz"] = "time";
            query["ra"] = "routePath,routePathAnnotations,routeProperties,routeInfoCard,TransitFrequency";
            query["du"] = "km";
            query["tt"] = "departure";
            query["maxSolns"] = "1";
            query["rpo"] = "None";
            UriBuilder builder = new UriBuilder($"https://dev.virtualearth.net/REST/v1/Routes/{mode}");
            builder.Port = -1;
            builder.Query = query.ToString();
            string url = builder.ToString();
            JsonElement result = await http.GetFromJsonAsync<JsonElement>(url);
            int duration = result.GetProperty("resourceSets")[0].GetProperty("resources")[0].GetProperty("travelDuration").GetInt32();
            return duration;
        }
    }
}