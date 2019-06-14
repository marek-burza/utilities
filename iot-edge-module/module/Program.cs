using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Loader;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Azure.Devices.Client;
using Microsoft.Azure.Devices.Shared;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;


namespace module
{
    public class Program
    {
        private static readonly IServiceProvider Provider = InitLogging();

        private static IServiceProvider InitLogging()
        {
            IServiceCollection services = new ServiceCollection();
            services.AddLogging(configuration =>
            {
                configuration.ClearProviders();
                configuration.AddConsole();
            });
            services.Configure<LoggerFilterOptions>(options => options.MinLevel = LogLevel.Debug);
            return services.BuildServiceProvider();
        }

        private static ILogger Logger;

        public static void Main(string[] arguments)
        {
            Logger = Program.Provider.GetService<ILogger<Program>>();
            if (arguments.Length == 0)
            {
                Run().GetAwaiter().GetResult();
            }
            else
            {
                Adjust(int.Parse(arguments[0])).GetAwaiter().GetResult();
            }
        }

        private static ModuleClient Client = null;

        private static async Task Run()
        {
            AmqpTransportSettings setting = new AmqpTransportSettings(TransportType.Amqp_Tcp_Only);
            ITransportSettings[] settings = { setting };

            try
            {
                Logger.LogInformation("Connecting to hub");
                Client = await ModuleClient.CreateFromEnvironmentAsync(settings);
                await Client.OpenAsync();
                Client.SetConnectionStatusChangesHandler(ConnectionStatusChangeHandler);

                Logger.LogInformation("Retrieving twin");
                Twin twin = await Client.GetTwinAsync();

                await Client.SetDesiredPropertyUpdateCallbackAsync(OnDesiredPropertyChanged, null);

                Logger.LogInformation("Initial twin received {0}", JsonConvert.SerializeObject(twin));

                Logger.LogInformation("Sending default value as reported property");
                TwinCollection reportedProperties = new TwinCollection();
                reportedProperties["value"] = 0;

                await Client.UpdateReportedPropertiesAsync(reportedProperties);

                // Method will be enabled when the first method handler is added (IoT Hub Device)
                // await Client.SetMethodHandlerAsync("METHOD", Method, null);

                // Register callback to be called when a message is received by the module
                await Client.SetInputMessageHandlerAsync("input1", PipeMessage, Client);

                // Wait until the app unloads or is cancelled
                CancellationTokenSource cts = new CancellationTokenSource();
                AssemblyLoadContext.Default.Unloading += (ctx) => cts.Cancel();
                Console.CancelKeyPress += (sender, cpe) => cts.Cancel();
                await WhenCancelled(cts.Token);
            }
            catch (AggregateException exceptions)
            {
                foreach (Exception exception in exceptions.InnerExceptions)
                {
                    Logger.LogError("Error: {0}", exception);
                }
            }
            catch (Exception exception)
            {
                Logger.LogError("Error: {0}", exception.Message);
            }
            Logger.LogInformation("Exiting...");

            // Remove the METHOD handler (IoT Hub Device)
            // Client?.SetMethodHandlerAsync("METHOD", null, null).Wait();

            Client?.CloseAsync().Wait();
        }

        private static void EchoValueProperty(TwinCollection desiredProperties, TwinCollection reportedProperties)
        {
            try
            {
                reportedProperties["value"] = (int)desiredProperties["value"];
            }
            catch (Exception exception)
            {
                Logger.LogError(exception.ToString());
            }
        }

        private static void ConnectionStatusChangeHandler(ConnectionStatus status, ConnectionStatusChangeReason reason)
        {
            Logger.LogInformation("Connection status changed to {0}", status);
            Logger.LogInformation("Connection status changed reason is {0}", reason);
        }

        private static Task OnDesiredPropertyChanged(TwinCollection desiredProperties, object userContext)
        {
            Logger.LogInformation("Desired property change: {0}", JsonConvert.SerializeObject(desiredProperties));
            TwinCollection reportedProperties = new TwinCollection();
            Logger.LogInformation("Sending current value as reported property");
            EchoValueProperty(desiredProperties, reportedProperties);
            Client.UpdateReportedPropertiesAsync(reportedProperties).Wait();
            return Task.CompletedTask;
        }

        // Only for IoT Hub Device
        // private static Task<MethodResponse> Method(MethodRequest methodRequest, object userContext)
        // {
        //     Logger.LogInformation("Received METHOD method request: {0} {1}", methodRequest.DataAsJson, userContext.ToString());
        //     return Task.FromResult(new MethodResponse(new byte[0], 200));
        // }

        private static int Counter;

        private static async Task<MessageResponse> PipeMessage(Message message, object userContext)
        {
            int counter = Interlocked.Increment(ref Counter);

            ModuleClient moduleClient = (ModuleClient)userContext;
            if (moduleClient == null)
            {
                throw new InvalidOperationException("User context does not contain expected content");
            }

            byte[] messageBytes = message.GetBytes();
            string messageString = Encoding.UTF8.GetString(messageBytes);
            Logger.LogInformation($"Received message #{counter}: {messageString}");

            if (!string.IsNullOrEmpty(messageString))
            {
                Message pipeMessage = new Message(messageBytes);
                foreach (KeyValuePair<string, string> prop in message.Properties)
                {
                    pipeMessage.Properties.Add(prop.Key, prop.Value);
                }
                await moduleClient.SendEventAsync("output1", pipeMessage);
                Logger.LogInformation("Received message sent");
            }
            return MessageResponse.Completed;
        }

        private static Task WhenCancelled(CancellationToken cancellationToken)
        {
            TaskCompletionSource<bool> tcs = new TaskCompletionSource<bool>();
            cancellationToken.Register(source => ((TaskCompletionSource<bool>)source).SetResult(true), tcs);
            return tcs.Task;
        }

        private static async Task Adjust(int value)
        {
            Microsoft.Azure.Devices.RegistryManager manager = Microsoft.Azure.Devices.RegistryManager.CreateFromConnectionString(Environment.GetEnvironmentVariable("IOTHUB_SERVICE_CONNECTION_STRING"));
            string device = Environment.GetEnvironmentVariable("IOTEDGE_DEVICE_ID");
            string module = Environment.GetEnvironmentVariable("IOTEDGE_MODULE_NAME");
            Microsoft.Azure.Devices.IQuery query = manager.CreateQuery($"SELECT * FROM devices.modules WHERE deviceId = '{device}' AND moduleId = '{module}'", 100);
            Twin twin = (await query.GetNextAsTwinAsync()).Single();
            string patch = $"{{\"properties\":{{\"desired\":{{\"value\":{value}}}}}}}";
            await manager.UpdateTwinAsync(twin.DeviceId, module, patch, twin.ETag);
            Logger.LogInformation($"Adjusted value to: {value}");
        }
    }
}
