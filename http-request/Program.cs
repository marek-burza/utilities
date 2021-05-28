using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace http_request
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World");
            Go().Wait();
        }

        private async static Task Go()
        {
            HttpClient client = new HttpClient();
            client.DefaultRequestHeaders.TryAddWithoutValidation("Content-Type", "application/json");
            try
            {
                HttpResponseMessage response = await client.GetAsync(
                    "http://samples.openweathermap.org/data/2.5/weather?q=London");
                Console.WriteLine("STATUS: {0}", response.StatusCode);
                Console.WriteLine("HEADERS:\n{0}", response.Headers.ToString());
                Console.WriteLine("BODY: {0}", await response.Content.ReadAsStringAsync());
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine("EXCEPTION: {0}", e.Message);
            }
        }
    }
}