FROM golang:1.16.2-alpine AS Build

WORKDIR /input
COPY . .
RUN go get -d -v
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /output/gpx2png


FROM golang:1.16.2-alpine

COPY --from=Build /output/gpx2png /gpx2png

ENTRYPOINT [ "/gpx2png" ]
