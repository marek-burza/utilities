FROM mcr.microsoft.com/dotnet/core/sdk:3.0 as CoreNetBuilder

ADD . /app
WORKDIR /app

RUN dotnet restore ./AzureBlobUpload.csproj
RUN dotnet publish -c release -o published -r linux-x64


FROM mcr.microsoft.com/dotnet/core/runtime:3.0

WORKDIR /app
COPY --from=CoreNetBuilder /app/published .

ENTRYPOINT ["dotnet", "/app/AzureBlobUpload.dll"]
