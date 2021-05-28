FROM mcr.microsoft.com/dotnet/core/sdk:3.1 as CoreNetBuilder
ENV DOTNET_CLI_TELEMETRY_OPTOUT 1

COPY . /app
WORKDIR /app

RUN dotnet publish -c release -o published -r linux-x64


FROM mcr.microsoft.com/dotnet/core/runtime:3.1-buster-slim

RUN apt-get -yq update && DEBIAN_FRONTEND=noninteractive apt-get -yq install libgdiplus

WORKDIR /app
COPY --from=CoreNetBuilder /app/published .

ENTRYPOINT ["/app/Explorer"]
