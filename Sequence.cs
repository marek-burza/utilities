// <copyright file="Sequence.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using Microsoft.Extensions.Logging;

    /// <summary>
    /// Sequence class of the application.
    /// </summary>
    public static class Sequence
    {
        private static readonly object Protector = new object();
        private static Random random = new Random((int)(DateTimeOffset.UtcNow.ToUnixTimeSeconds() & 0xFFFFFFFF));
        private static uint sequence = (uint)random.Next();

        /// <summary>
        /// Logs next sequence number.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogSequence(string argument, ILogger logger)
        {
            logger.LogInformation($"{Obtain()}");
        }

        private static uint Obtain()
        {
            uint obtained;

            lock (Protector)
            {
                sequence = (sequence + 1) & 0xFFFFFFFF;
                obtained = sequence;
            }

            return obtained;
        }
    }
}
