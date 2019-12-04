// <copyright file="Stamp.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using System.Globalization;
    using Microsoft.Extensions.Logging;

    /// <summary>
    /// Stamp class of the application.
    /// </summary>
    public static class Stamp
    {
        /// <summary>
        /// Logs Unix timestamp.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogUnixTimestamp(string argument, ILogger logger)
        {
            logger.LogInformation($"{DateTimeToUnixTimestamp(StringToDateTime(argument))}");
        }

        private static DateTime StringToDateTime(string stamp)
        {
            return DateTime.Parse(stamp.Trim(), CultureInfo.InvariantCulture, DateTimeStyles.RoundtripKind);
        }

        private static uint DateTimeToUnixTimestamp(DateTime stamp)
        {
            return (uint)(TimeZoneInfo.ConvertTimeToUtc(stamp) - new DateTime(1970, 1, 1, 0, 0, 0, 0, System.DateTimeKind.Utc)).TotalSeconds;
        }
    }
}
