using System.Net;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

public static async Task<IActionResult> Run(HttpRequest req, ILogger logger)
{
    logger.LogInformation("HTTP TRIGGER: Random");
    logger.LogInformation($"ENVIRONMENT: {System.Environment.GetEnvironmentVariable("ENVIRONMENT_VARIABLE")}");

    string body = await new StreamReader(req.Body).ReadToEndAsync();
    logger.LogInformation($"INPUT: {body}");

    return new OkObjectResult($"{{value: {new Random().Next()}}}");
}
