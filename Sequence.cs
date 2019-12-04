// <copyright file="Sequence.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;

    /// <summary>
    /// Sequence class of the application.
    /// </summary>
    public static class Sequence
    {
        private static readonly object Protector = new object();
        private static Random random = new Random((int)(DateTimeOffset.UtcNow.ToUnixTimeSeconds() & 0xFFFFFFFF));
        private static uint sequence = (uint)random.Next();

        /// <summary>
        /// Obtains next sequence number.
        /// </summary>
        /// <returns>Result next sequence.</returns>
        public static uint Obtain()
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
