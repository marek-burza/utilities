// <copyright file="WebApi.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.AspNetCore.Mvc.NewtonsoftJson;
    using Newtonsoft.Json.Linq;

    /// <summary>
    /// Web API class of the application.
    /// </summary>
    [Produces("application/json")]
    [Route("/api")]
    public class WebApi : ControllerBase
    {
        /// <summary>
        /// Echo API end-point.
        /// </summary>
        /// <param name="arguments">JSON arguments for the API end-point.</param>
        /// <returns>HTTP result.</returns>
        [HttpPost]
        [Route("echo")]
        public IActionResult Echo([FromBody]JObject arguments)
        {
            try
            {
                return this.Ok(arguments);
            }
            catch (Exception)
            {
                return this.StatusCode(500, new JObject());
            }
        }
    }
}
