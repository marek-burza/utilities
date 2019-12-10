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

        /// <summary>
        /// Logs array ordered by "key".
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogOrderedArray(string argument, ILogger logger)
        {
            JArray array = JArray.Parse(argument);
            array = OrderByKey(array, "key");
            logger.LogInformation(JsonConvert.SerializeObject(array));
        }

        /// <summary>
        /// Logs aggregated array of objects.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogAggregated(string argument, ILogger logger)
        {
            JArray array = JArray.Parse(argument);
            JObject aggregated = Aggregate(array);
            logger.LogInformation(JsonConvert.SerializeObject(aggregated));
        }

        /// <summary>
        /// Logs min and max of an array.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogMinMax(string argument, ILogger logger)
        {
            double[] array = JArray.Parse(argument).ToObject<List<double>>().ToArray();
            double min = array.Cast<double>().Min();
            double max = array.Cast<double>().Max();
            logger.LogInformation($"MIN: {min}; MAX: {max};");
        }

        /// <summary>
        /// Logs keys.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogKeys(string argument, ILogger logger)
        {
            JObject dictionary = JObject.Parse(argument);
            ISet<string> keys = dictionary.Properties().Select(property => property.Name).ToHashSet();
            foreach (string key in keys)
            {
                logger.LogInformation(key);
            }
        }

        /// <summary>
        /// Logs range of values.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogRange(string argument, ILogger logger)
        {
            JObject dictionary = JObject.Parse(argument);
            JToken begin, end;
            dictionary.TryGetValue("begin", out begin);
            dictionary.TryGetValue("end", out end);
            List<int> range = Enumerable.Range((int)begin, (int)end).ToList().ConvertAll(value => (int)value);
            foreach (int value in range)
            {
                logger.LogInformation($"{value}");
            }
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

        private static JArray OrderByKey(JArray array, string key)
        {
            return new JArray(array.OrderBy(item => (long)item[key]));
        }

        private static JObject Aggregate(JArray objects)
        {
            return objects.Select(item => (JObject)item).Aggregate(new JObject(), (a, b) => Merge(a, b));
        }

        private static JObject Merge(JObject a, JObject b)
        {
            ISet<string> keysA = a.Properties().Select(property => property.Name).ToHashSet();
            ISet<string> keysB = b.Properties().Select(property => property.Name).ToHashSet();
            ISet<string> keys = keysA.Union(keysB).ToHashSet();
            JObject merged = new JObject();
            foreach (string key in keys)
            {
                JArray array = new JArray();
                if (a.ContainsKey(key))
                {
                    array.Merge(a[key]);
                }

                if (b.ContainsKey(key))
                {
                    array.Merge(b[key]);
                }

                merged[key] = array;
            }

            return merged;
        }
    }
}
