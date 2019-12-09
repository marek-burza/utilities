// <copyright file="WebApi.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using System.Drawing;
    using System.IO;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.AspNetCore.Mvc.NewtonsoftJson;
    using Newtonsoft.Json.Linq;

    /// <summary>
    /// Web API class of the application.
    /// </summary>
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
        [Produces("application/json")]
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

        /// <summary>
        /// Image API end-point.
        /// </summary>
        /// <param name="text">Text to be drawn.</param>
        /// <param name="width">Width of the image.</param>
        /// <param name="height">Height of the image.</param>
        /// <returns>HTTP result.</returns>
        [HttpGet]
        [Route("image")]
        [Produces("image/png")]
        public IActionResult Image([FromQuery(Name = "text")]string text, [FromQuery(Name = "width")]int width, [FromQuery(Name = "height")]int height)
        {
            Bitmap bitmap = new Bitmap(width, height);
            using (Graphics graphics = Graphics.FromImage(bitmap))
            {
                Brush gray = new SolidBrush(Color.FromArgb(0xFF, 0x80, 0x80, 0x80));
                Brush black = new SolidBrush(Color.FromArgb(0xFF, 0x00, 0x00, 0x00));
                FontFamily family = new FontFamily("Arial");
                Font font = new Font(family, 16, FontStyle.Regular, GraphicsUnit.Pixel);
                StringFormat format = new StringFormat();
                format.Alignment = StringAlignment.Center;
                format.LineAlignment = StringAlignment.Center;
                graphics.FillRectangle(gray, 0, 0, width, height);
                graphics.DrawString(text, font, black, width / 2, height / 2, format);
                using (MemoryStream stream = new MemoryStream())
                {
                    bitmap.Save(stream, System.Drawing.Imaging.ImageFormat.Png);
                    return this.File(stream.ToArray(), "image/png");
                }
            }
        }
    }
}
