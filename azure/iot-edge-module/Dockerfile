FROM mcr.microsoft.com/dotnet/core/sdk:3.0.100-preview6-buster as CoreNetBuilder
ENV DOTNET_CLI_TELEMETRY_OPTOUT 1

ADD module /app
WORKDIR /app

RUN dotnet publish -c release -o published -r linux-arm


FROM mcr.microsoft.com/dotnet/core/runtime:3.0.0-preview6-buster-slim-arm32v7

WORKDIR /app
COPY --from=CoreNetBuilder /app/published .

ENTRYPOINT ["dotnet", "/app/module.dll"]