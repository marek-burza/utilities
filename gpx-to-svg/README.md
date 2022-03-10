# GPX to SVG

Originally started as a CLI written in Go but ported to C# as a Blazor WebAssembly front-end app

To build & run it locally:

```bash
docker build -t gpx-to-svg .
docker run --rm -it -p 8080:80 gpx-to-svg
```

To use a pre-built Docker container image:

```bash
docker run --rm -it -p 8080:80 altermarkive/gpx-to-svg
```

Or just go [here](https://altermarkive.github.io/gpx-to-svg/).
