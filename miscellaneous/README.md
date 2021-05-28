# Exploring C#

To create this project I ran:

    docker run -it -v $PWD:/project -w /project mcr.microsoft.com/dotnet/core/sdk:3.1 dotnet new console

To add NuGet package:

    docker run -it -v $PWD:/project -w /project mcr.microsoft.com/dotnet/core/sdk:3.1 dotnet add package $PACKAGE

To build the container:

    docker build -t explorer .

To run the container:

    docker run --rm -it explorer

To build the application in a container:

    docker run --rm -it -v $PWD:/project -w /project mcr.microsoft.com/dotnet/core/sdk:3.1 /bin/sh -c "dotnet restore ./Explorer.csproj && dotnet publish -c release -o published -r win10-x64"
