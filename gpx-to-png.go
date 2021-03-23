package main

import (
	"encoding/hex"
	"fmt"
	"image/color"
	"image/png"
	"io/ioutil"
	"os"
	"strconv"
	"strings"

	sm "github.com/flopp/go-staticmaps"
	"github.com/golang/geo/s2"
	"github.com/tkrajina/gpxgo/gpx"
)

func main() {
	if len(os.Args) < 10 {
		fmt.Printf("USAGE: gpx2png INPUT_GPX MAP_STYLE WIDTH HEIGHT MARKER_COLOR MARKER_SIZE PATH_COLOR PATH_SIZE OUTPUT_PNG\n")
		os.Exit(1)
	}

	ctx := sm.NewContext()

	gpxFile := os.Args[1]
	gpxBytes, failure := ioutil.ReadFile(gpxFile)
	if failure != nil {
		fmt.Printf("ERROR: Invalid GPX file (%+v)\n", failure)
		os.Exit(1)
	}
	gpx, failure := gpx.ParseBytes(gpxBytes)
	if failure != nil {
		fmt.Printf("ERROR: Invalid GPX file (%+v)\n", failure)
		os.Exit(1)
	}

	mapStyle := os.Args[2]
	providers := sm.GetTileProviders()
	provider, found := providers[mapStyle]
	if !found {
		mapStyles := make([]string, 0)
		for provider := range providers {
			mapStyles = append(mapStyles, provider)
		}
		fmt.Printf("ERROR: Invalid map style argument (must be one of: %s)\n", strings.Join(mapStyles, " "))
		os.Exit(1)
	}
	ctx.SetTileProvider(provider)

	width, failure := strconv.Atoi(os.Args[3])
	if failure != nil {
		fmt.Printf("ERROR: Invalid width argument (%+v)\n", failure)
		os.Exit(1)
	}
	height, failure := strconv.Atoi(os.Args[4])
	if failure != nil {
		fmt.Printf("ERROR: Invalid height argument (%+v)\n", failure)
		os.Exit(1)
	}
	ctx.SetSize(width, height)

	markerColorString := os.Args[5]
	markerColorBytes, failure := hex.DecodeString(markerColorString)
	if failure != nil || len(markerColorBytes) < 3 {
		fmt.Printf("ERROR: Invalid marker color, should be in hexadecimal format RRGGBB (%+v)\n", failure)
		os.Exit(1)
	}
	markerColor := color.RGBA{markerColorBytes[0], markerColorBytes[1], markerColorBytes[2], 0xFF}

	markerSize, failure := strconv.ParseFloat(os.Args[6], 64)
	if failure != nil {
		fmt.Printf("ERROR: Invalid marker size (%+v)\n", failure)
		os.Exit(1)
	}

	pathColorString := os.Args[7]
	pathColorBytes, failure := hex.DecodeString(pathColorString)
	if failure != nil || len(pathColorBytes) < 3 {
		fmt.Printf("ERROR: Invalid marker color, should be in hexadecimal format RRGGBB (%+v)\n", failure)
		os.Exit(1)
	}
	pathColor := color.RGBA{pathColorBytes[0], pathColorBytes[1], pathColorBytes[2], 0xFF}

	pathSize, failure := strconv.ParseFloat(os.Args[8], 64)
	if failure != nil {
		fmt.Printf("ERROR: Invalid path size (%+v)\n", failure)
		os.Exit(1)
	}

	for _, point := range gpx.Waypoints {
		ctx.AddMarker(
			sm.NewMarker(
				s2.LatLngFromDegrees(point.Latitude, point.Longitude),
				markerColor,
				markerSize,
			),
		)
	}
	for _, route := range gpx.Routes {
		positions := make([]s2.LatLng, 0)
		for _, point := range route.Points {
			positions = append(positions, s2.LatLngFromDegrees(point.Latitude, point.Longitude))
		}
		ctx.AddPath(
			sm.NewPath(
				positions,
				pathColor,
				pathSize,
			),
		)
	}
	for _, track := range gpx.Tracks {
		for _, segment := range track.Segments {
			positions := make([]s2.LatLng, 0)
			for _, point := range segment.Points {
				positions = append(positions, s2.LatLngFromDegrees(point.Latitude, point.Longitude))
			}
			ctx.AddPath(
				sm.NewPath(
					positions,
					pathColor,
					pathSize,
				),
			)
		}
	}

	image, failure := ctx.Render()
	if failure != nil {
		fmt.Printf("ERROR: Failed to render the map (%+v)\n", failure)
		os.Exit(1)
	}

	pngFile := os.Args[9]
	handle, failure := os.Create(pngFile)
	if failure != nil {
		fmt.Printf("ERROR: Failed to create the PNG file (%+v)\n", failure)
		os.Exit(1)
	}

	if failure := png.Encode(handle, image); failure != nil {
		fmt.Printf("ERROR: Failed to encode the PNG file (%+v)\n", failure)
		os.Exit(1)
	}

	if failure := handle.Close(); failure != nil {
		fmt.Printf("ERROR: Failed to close the PNG file (%+v)\n", failure)
		os.Exit(1)
	}
}
