FROM mcr.microsoft.com/dotnet/sdk:5.0 AS Build

COPY Program.cs Startup.cs websocket-echo.csproj /app/

WORKDIR /app

RUN dotnet publish -c Release -r linux-x64 -p:PublishSingleFile=true --self-contained true

FROM mcr.microsoft.com/dotnet/runtime:5.0

WORKDIR /app

COPY --from=Build /app/bin/Release/net5.0/linux-x64/publish/websocket-echo /app/websocket-echo
COPY wwwroot/index.html wwwroot/socket.js /app/wwwroot/

EXPOSE 5000

CMD ["/app/websocket-echo"]
