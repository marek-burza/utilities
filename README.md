# Exploring C#

To create this project I ran:

    docker run -it -v $PWD:/project -w /project mcr.microsoft.com/dotnet/core/sdk:3.0 dotnet new console

To build the container:

    docker build -t explorer .

To run the container:

    docker run --rm -it explorer
