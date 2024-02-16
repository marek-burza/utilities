using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Microsoft.Extensions.DependencyInjection;
using MudBlazor.Services;
using FisSst.BlazorMaps.DependencyInjection;

namespace CommuteTimeMapper
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = WebAssemblyHostBuilder.CreateDefault(args);
            builder.RootComponents.Add<App>("#app");

            builder.Services.AddMudServices();

            builder.Services.AddHttpClient<BingMaps>(
                client => client.BaseAddress = new Uri(builder.HostEnvironment.BaseAddress));

            builder.Services.AddBlazorLeafletMaps();

            await builder.Build().RunAsync();
        }
    }
}
