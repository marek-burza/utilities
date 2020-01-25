# Example Azure App Service

This repository implements an example password protected App Service (with auth timeout) which exposes a Swagger API and proxies to Azure Blob Storage for static frontend (without anonymous blob access).

After running the create script the app will be available at:

    https://[PREFIX]app.azurewebsites.net/index.html


# Extras

## Sources & Materials

* [Advanced usage of authentication and authorization in Azure App Service (works only for a web app but web apps do not have proxies)](https://docs.microsoft.com/en-us/azure/app-service/app-service-authentication-how-to)
* [Azure Functions Python developer guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
* [Quickstart V2 Python Functions with Azure Functions Core Tools](https://github.com/yokawasa/azure-functions-python-samples/blob/master/docs/quickstart-v2-python-functions.md)
* [Starting point for ASP.NET Core](https://docs.microsoft.com/en-us/aspnet/core/?view=aspnetcore-2.2)
* [Serverless web application on Azure](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/serverless/web-app)
* [Map a custom domain to an Azure Blob Storage endpoint](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-custom-domain-name)

## Swagger - Code Generation

Command to generate the Swagger server code (here example for ASP.NET Core):

    docker run --rm -it -v api.json:/api.json -v config.json:/config.json -v $PWD/server:/server swaggerapi/swagger-codegen-cli generate -i /api.json -l aspnetcore -c /config.json -o /server

The content of the `config.json` file defines the C# namespace:

    {
      "packageName" : "example"
    }

Command to build Swagger client code (for JavaScript):

    docker build -t swagger-client . && docker run --rm -it -v $PWD/client:/client swagger-client

The content of the Dockerfile:

    FROM node:8
    RUN git clone --branch v3.8.6 https://github.com/swagger-api/swagger-js.git && \
        cd /swagger-js && \
        npm install && \
        npm run build-bundle
    CMD ["cp", "/swagger-js/browser/swagger-client.js", "/client/swagger-client.js"]
