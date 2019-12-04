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

        /// <summary>
        /// Logs local date/time.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogLocalTimestamp(string argument, ILogger logger)
        {
            long stamp = long.Parse(argument);
            DateTime epoch = new DateTime(1970, 1, 1, 0, 0, 0, 0, System.DateTimeKind.Utc);
            DateTime datetime = new DateTime(1970, 1, 1, 0, 0, 0, 0, System.DateTimeKind.Utc).AddSeconds(stamp);
            logger.LogInformation($"Days since epoch: {(datetime.Date - epoch.Date).TotalDays}");
            logger.LogInformation($"Days since midnight: {datetime.TimeOfDay.TotalSeconds}");
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
