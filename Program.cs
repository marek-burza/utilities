// <copyright file="Program.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Reflection;
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
        private static readonly IDictionary<string, Command> Commands = new Dictionary<string, Command>
        {
            {
                "hex", new Command("hex", "Convert text to hexadecimal", "Text to convert", Codec.ConvertToHex)
            },
            {
                "file", new Command("file", "Log lines from file", "File to log", LogLinesFromFile)
            },
            {
                "resource", new Command("resource", "Log lines from resource", null, LogLinesFromResource)
            },
            {
                "csv", new Command("csv", "Parse CSV lines", "JSON with CSV lines", Json.ParseCSV)
            },
            {
                "sequence", new Command("sequence", "Obtain sequence", null, Sequence.LogSequence)
            },
            {
                "interfaces", new Command("interfaces", "List interfaces", null, Network.LogInterfaces)
            },
            {
                "broadcasts", new Command("broadcasts", "List broadcasting addresses", null, Network.LogBroadcastAddresses)
            },
            {
                "matching", new Command("matching", "Look-up matching own address", "Address to match", Network.LogMatchingAddress)
            },
            {
                "unix", new Command("unix", "Convert date/time to Unix timestamp", "Date/time", Stamp.LogUnixTimestamp)
            },
            {
                "floats", new Command("floats", "Parse array of strings to array of floats", "Array of strings", Json.LogParsedArray)
            },
            {
                "order", new Command("order", "Orders array by key", "Array of objects", Json.LogOrderedArray)
            },
            {
                "datetime", new Command("datetime", "Local date/time offsets", "Unix timestamp", Stamp.LogLocalTimestamp)
            },
            {
                "aggregate", new Command("aggregate", "Aggregate objects", "Array of objects", Json.LogAggregated)
            },
            {
                "codec", new Command("codec", "Apply binary codec", "Configuration", Codec.LogCodec)
            },
        };

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
            Command.RegisterCommands(cli, Commands, Logger);
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

        private static void RegisterCommand(CommandLineApplication cli, string commandName, string commandDescription, string argumentDescription, Action<string, ILogger> action)
        {
            cli.Command(commandName, (command) =>
            {
                command.Description = commandDescription;
                command.HelpOption("-? | -h | --help");
                CommandArgument argument = argumentDescription != null ? command.Argument("argument", argumentDescription) : null;
                command.OnExecute(() =>
                {
                    action(argumentDescription != null ? argument.Value : null, Logger);
                    return 0;
                });
            });
        }

        private static void LogLinesFromFile(string path, ILogger logger)
        {
            List<string> lines = File.ReadAllLines(path, Encoding.UTF8).ToList();
            foreach (string line in lines)
            {
                logger.LogInformation(line);
            }
        }

        private static void LogLinesFromResource(string argument, ILogger logger)
        {
            Assembly assembly = Assembly.GetEntryAssembly();
            string name = $"Explorer.resources.example.txt";
            using (Stream stream = assembly.GetManifestResourceStream(name))
            {
                using (StreamReader reader = new StreamReader(stream, Encoding.UTF8))
                {
                    List<string> lines = reader.ReadToEnd().Split(Environment.NewLine.ToCharArray(), StringSplitOptions.RemoveEmptyEntries).ToList();
                    foreach (string line in lines)
                    {
                        logger.LogInformation(line);
                    }
                }
            }
        }
    }
}
