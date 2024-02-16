// <copyright file="Command.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using System.Collections.Generic;
    using Microsoft.Extensions.CommandLineUtils;
    using Microsoft.Extensions.Logging;

    /// <summary>
    /// Command class of the application.
    /// </summary>
    public class Command
    {
        private readonly string commandName;
        private readonly string commandDescription;
        private readonly string argumentDescription;
        private readonly Action<string, ILogger> commandAction;

        /// <summary>
        /// Initializes a new instance of the <see cref="Command"/> class.
        /// </summary>
        /// <param name="commandName">Command name.</param>
        /// <param name="commandDescription">Command description.</param>
        /// <param name="argumentDescription">Argument description.</param>
        /// <param name="commandAction">Command action.</param>
        public Command(string commandName, string commandDescription, string argumentDescription, Action<string, ILogger> commandAction)
        {
            this.commandName = commandName;
            this.commandDescription = commandDescription;
            this.argumentDescription = argumentDescription;
            this.commandAction = commandAction;
        }

        /// <summary>
        /// Registers a single command.
        /// </summary>
        /// <param name="cli">CLI handle.</param>
        /// <param name="definition">Command definition.</param>
        /// <param name="logger">Logger to be used.</param>
        public static void RegisterCommand(CommandLineApplication cli, Command definition, ILogger logger)
        {
            cli.Command(definition.commandName, (command) =>
            {
                command.Description = definition.commandDescription;
                command.HelpOption("-? | -h | --help");
                CommandArgument argument = definition.argumentDescription != null ? command.Argument("argument", definition.argumentDescription) : null;
                command.OnExecute(() =>
                {
                    definition.commandAction(definition.argumentDescription != null ? argument.Value : null, logger);
                    return 0;
                });
            });
        }

        /// <summary>
        /// Registers multiple commands.
        /// </summary>
        /// <param name="cli">CLI handle.</param>
        /// <param name="definitions">Command definitions.</param>
        /// <param name="logger">Logger to be used.</param>
        public static void RegisterCommands(CommandLineApplication cli, IDictionary<string, Command> definitions, ILogger logger)
        {
            foreach (KeyValuePair<string, Command> entry in definitions)
            {
                RegisterCommand(cli, entry.Value, logger);
            }
        }
    }
}