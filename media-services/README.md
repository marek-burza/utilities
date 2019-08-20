# Screencast to Azure Media Services sink

To capture the screen content use **VLC** (https://www.videolan.org/vlc/download-windows.html):

1.	_Media_ -> _Open Capture Device_
2.	Pick: _Capture mode_ - DirectShow; _Video device name_ - Default; _Audio device name_ - Microphone (or other device as necessary)
3.	Click the dropdown button next to the _Play_ button and pick _Stream_
4.	Click _Next_
5.	Pick _UDP (legacy)_ and click _Add_
6.	Enter: _Adres_ – localhost; _Base port_ – 1234; _Stream name_ – test
7.	Click _Next_
8.	For the _Profile_ pick _Video H.264 + MP3 (TS)_
9.	Click _Next_
10.	Click _Stream_

To transcode the stream (though a pass-through codec _copy_ would probably suffice for video) and push it to an RTMP Ingest URL use **ffmpeg** (https://ffmpeg.zeranoe.com/builds/).

    ffmpeg -i udp://localhost:1234 -strict -2 -c:a aac -b:a 128k -ar 44100 -r 30 -g 60 -keyint_min 60 -b:v 200000 -c:v libx264 -preset medium -bufsize 600k -maxrate 200k -f <Primary Azure Ingest URL>/mystream1

For Azure Media Service use:

* Live Encoding (since with **VLC** and **ffmpeg** we have a good control over encoding we could probably use Pass Through instead)
* RTMP for Ingest Protocol.

A few helpful links:

* https://trac.ffmpeg.org/wiki/StreamingGuide
* https://azure.microsoft.com/en-gb/blog/azure-media-services-rtmp-support-and-live-encoders/
* https://docs.microsoft.com/en-us/azure/media-services/media-services-portal-creating-live-encoder-enabled-channel
* https://azure.microsoft.com/en-us/blog/getting-started-with-live-streaming-using-the-azure-management-portal/
