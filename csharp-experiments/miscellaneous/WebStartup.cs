// <copyright file="WebStartup.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using Microsoft.AspNetCore;
    using Microsoft.AspNetCore.Builder;
    using Microsoft.AspNetCore.Hosting;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.Extensions.Configuration;
    using Microsoft.Extensions.DependencyInjection;
    using Microsoft.Extensions.Hosting;
    using Microsoft.Extensions.Logging;

    /// <summary>
    /// Main class of the program.
    /// </summary>
    public class WebStartup
    {
        /// <summary>
        /// Initializes a new instance of the <see cref="WebStartup"/> class.
        /// </summary>
        /// <param name="configuration">ASP.NET Core app configuration.</param>
        public WebStartup(IConfiguration configuration)
        {
            this.Configuration = configuration;
        }

        /// <summary>
        /// Gets the ASP.NET Core app configuration.
        /// </summary>
        public IConfiguration Configuration { get; }

        /// <summary>
        /// Launches the ASP.NET Core app.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LaunchWeb(string argument, ILogger logger)
        {
            WebHost.CreateDefaultBuilder().UseStartup<WebStartup>().Build().Run();
        }

        /// <summary>
        /// Configures the services of the ASP.NET Core app.
        /// </summary>
        /// <param name="services">Services of the ASP.NET Core app.</param>
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc(option => option.EnableEndpointRouting = false).AddNewtonsoftJson().SetCompatibilityVersion(CompatibilityVersion.Version_3_0);
        }

        /// <summary>
        /// Creates the request processing pipeline for the ASP.NET Core app.
        /// </summary>
        /// <param name="application">Provides the mechanisms to configure an application's request pipeline.</param>
        /// <param name="environment">Provides information about the web hosting environment an application is running in.</param>
        public void Configure(IApplicationBuilder application, IWebHostEnvironment environment)
        {
            if (environment.IsDevelopment())
            {
                application.UseDeveloperExceptionPage();
            }

            application.UseMvc().UseDefaultFiles().UseStaticFiles();
        }
    }
}
