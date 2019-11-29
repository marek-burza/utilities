// <copyright file="Program.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using Microsoft.Extensions.DependencyInjection;
    using Microsoft.Extensions.Logging;

    /// <summary>
    /// Main class of the program.
    /// </summary>
    public class Program
    {
        /// <summary>
        /// Service provider for logging.
        /// </summary>
        public static readonly ServiceProvider Provider = InitLogging();

        /// <summary>
        /// Main entry into the program.
        /// </summary>
        /// <param name="arguments">Command line arguments of the program.</param>
        public static void Main(string[] arguments)
        {
            ILogger logger = Program.Provider.GetService<ILogger<Program>>();
            logger.LogDebug("Hello World!");
            System.Threading.Thread.Sleep(1000);
        }

        private static ServiceProvider InitLogging()
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
    }
}
