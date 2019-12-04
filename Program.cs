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
    using Newtonsoft.Json;
    using Newtonsoft.Json.Linq;

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
            RegisterCommand(cli, "resource", "Log lines from resource", null, LogLinesFromResource);
            RegisterCommand(cli, "csv", "Parse CSV lines", "JSON with CSV lines", ParseCSV);
            RegisterCommand(cli, "sequence", "Obtain sequence", null, ObtainSequence);
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
                    action(argumentDescription != null ? argument.Value : null);
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

        private static void LogLinesFromResource(string argument)
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
                        Logger.LogInformation(line);
                    }
                }
            }
        }

        private static void ParseCSV(string encodedLines)
        {
            JArray decodedLines = JArray.Parse(encodedLines);
            List<string> lines = decodedLines.ToObject<List<string>>();
            float[,] parsedCSV = ListToArray(lines.Select(line => Array.ConvertAll(line.Split(','), float.Parse)).ToList());
            Logger.LogInformation(JsonConvert.SerializeObject(parsedCSV));
        }

        private static T[,] ListToArray<T>(IList<T[]> arrays)
        {
            int count = arrays.Max(array => array.Count());
            T[,] result = new T[arrays.Count, count];

            for (int i = 0; i < arrays.Count; i++)
            {
                for (int j = 0; j < arrays[i].Length; j++)
                {
                    result[i, j] = arrays[i][j];
                }
            }

            return result;
        }

        private static void ObtainSequence(string argument)
        {
            Logger.LogInformation($"{Sequence.Obtain()}");
        }
    }
}
