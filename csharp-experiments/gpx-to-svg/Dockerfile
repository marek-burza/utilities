FROM mcr.microsoft.com/dotnet/sdk:5.0 as BuildStage

ADD . /app
WORKDIR /app

RUN dotnet publish -c Release


FROM nginx:1.21.0-alpine

COPY --from=BuildStage /app/bin/Release/net5.0/publish/wwwroot /app
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
