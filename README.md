# GPX to PNG

To convert a GPX to a static image in PNG format run:

    docker run --rm -it -v $PWD:/data -w /data altermarkive/gpx2png tour.gpx opentopomap 5000 5000 FF0000 16 FF00FF 16 tour.png
