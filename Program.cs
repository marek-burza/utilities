// <copyright file="Program.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Text;
    using Microsoft.Extensions.CommandLineUtils;
    using Microsoft.Extensions.DependencyInjection;
    using Microsoft.Extensions.Logging;

    /// <summary>
    /// Main class of the program.
    /// </summary>
    public class Program
    {
        private static readonly ServiceProvider Provider = InitLogging();
        private static readonly ILogger Logger = Program.Provider.GetService<ILogger<Program>>();

        /// <summary>
        /// Main entry into the program.
        /// </summary>
        /// <param name="arguments">Command line arguments of the program.</param>
        /// <returns>Result code of the application.</returns>
        public static int Main(string[] arguments)
        {
            CommandLineApplication cli = new CommandLineApplication();
            cli.Name = "Explorer";
            cli.Description = "Explorer Application";
            cli.HelpOption("-? | -h | --help");
            RegisterCommand(cli, "hex", "Convert text to hexadecimal", "Text to convert", ConvertToHex);
            RegisterCommand(cli, "file", "Log lines from file", "File to log", LogLinesFromFile);
            try
            {
                return cli.Execute(arguments);
            }
            catch (CommandParsingException)
            {
                return 1;
            }
            finally
            {
                Provider.Dispose();
                System.Threading.Thread.Sleep(1000);
            }
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

        private static void RegisterCommand(CommandLineApplication cli, string commandName, string commandDescription, string argumentDescription, Action<string> action)
        {
            cli.Command(commandName, (command) =>
            {
                command.Description = commandDescription;
                command.HelpOption("-? | -h | --help");
                CommandArgument argument = argumentDescription != null ? command.Argument("argument", argumentDescription) : null;
                command.OnExecute(() =>
                {
                    action(argument.Value);
                    return 0;
                });
            });
        }

        private static void ConvertToHex(string text)
        {
            Logger.LogInformation(Hex(Encoding.UTF8.GetBytes(text)));
        }

        private static string Hex(Span<byte> octets) => BitConverter.ToString(octets.ToArray()).Replace("-", string.Empty);

        private static void LogLinesFromFile(string path)
        {
            List<string> lines = File.ReadAllLines(path).ToList();
            foreach (string line in lines)
            {
                Logger.LogInformation(line);
            }
        }
    }
}
