// <copyright file="Json.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using Microsoft.Extensions.Logging;
    using Newtonsoft.Json;
    using Newtonsoft.Json.Linq;

    /// <summary>
    /// Stamp class of the application.
    /// </summary>
    public static class Json
    {
        /// <summary>
        /// Logs Unix timestamp.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void ParseCSV(string argument, ILogger logger)
        {
            JArray decodedLines = JArray.Parse(argument);
            List<string> lines = decodedLines.ToObject<List<string>>();
            float[,] parsedCSV = ListToArray(lines.Select(line => Array.ConvertAll(line.Split(','), float.Parse)).ToList());
            logger.LogInformation(JsonConvert.SerializeObject(parsedCSV));
        }

        /// <summary>
        /// Logs array of strings parsed to array of floats.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogParsedArray(string argument, ILogger logger)
        {
            JArray array = JArray.Parse(argument);
            array = ParseStringToFloatArray(array, 0);
            logger.LogInformation(JsonConvert.SerializeObject(array));
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

        private static JArray ParseStringToFloatArray(JArray array, int offset)
        {
            return new JArray(Array.ConvertAll(array.ToObject<List<string>>().ToArray().AsSpan().Slice(offset).ToArray(), float.Parse));
        }
    }
}
