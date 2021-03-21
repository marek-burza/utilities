# Geolocation API in an iOS Web App

## TL;DR

This experiment started with a simple need for quickly looking up my current geographical coordinates (latitude & longitude) on my iPhone. Surely, there's an app for that, but it felt like an overkill - I just wanted something disposable, light-weight, self-contained. There's barely anything fitting the bill better than a single-file Progressive Web Aapp which can be added to the home screen. If that's all you'd like to know about it, you can go ahead and click [here](https://altermarkive.github.io/web-experiments/location/).

## 1. Progressive Web App Template

I started with a minimalistic HTML file:

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <title>⤓</title>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: sans-serif;
        }
    </style>
</head>

<body>
    <div id="card">
    </div>
</body>

</html>
```

Then, I added an indication for the Safari browser that the HTML file can run as a full-screen web app with a translucent status bar and an unassuming app name:

```html
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
<meta name="apple-mobile-web-app-title" content="⤓" />
```

Next, I included icons for several different form factors (to be featured as app icons when it is added to the home screen):

```html
<link href="https://altermarkive.github.io/altermarkive/altermarkive.152.png" sizes="152x152" rel="apple-touch-icon" />
<link href="https://altermarkive.github.io/altermarkive/altermarkive.144.png" sizes="144x144" rel="apple-touch-icon" />
<link href="https://altermarkive.github.io/altermarkive/altermarkive.120.png" sizes="120x120" rel="apple-touch-icon" />
<link href="https://altermarkive.github.io/altermarkive/altermarkive.114.png" sizes="114x114" rel="apple-touch-icon" />
<link href="https://altermarkive.github.io/altermarkive/altermarkive.76.png" sizes="76x76" rel="apple-touch-icon" />
<link href="https://altermarkive.github.io/altermarkive/altermarkive.72.png" sizes="72x72" rel="apple-touch-icon" />
<link href="https://altermarkive.github.io/altermarkive/altermarkive.57.png" sizes="57x57" rel="apple-touch-icon" />
```

Given that it is intended to be a small app and quick to load, I opted to skip adding splash/loading screens.

## 2. Rigid Viewport

Typically, Safari goes a long way towards adaptive scaling & adding bounce effects when scrolling.
Instead, I wanted to have a more rigid viewport and to disable some of those effects.

First, I prevent the viewport from rescaling with "pinch":

```html
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=0, minimum-scale=1, maximum-scale=1" />
```

Next, I prevent the text from resizing when changing the device orientation:

```css
html {
    -webkit-text-size-adjust: 100%;
}
```

And last, I disable the bounce effect when the user is attempting scrolling:

```css
html {
    height: 100%;
    width: 100%;
    overflow: hidden;
    position: fixed;
}
```

## 3. Placeholders

The Geolocation API returns a rich set of values and I decided to show them on individual `div` elements:

```html
<div id="card">
    <div id="coordinates" class="field">&nbsp;</div>
    <div>°N,°E</div>
    <div id="accuracy" class="field">&nbsp;</div>
    <div>±meters</div>
    <div id="altitude" class="field">&nbsp;</div>
    <div>meters</div>
    <div id="altitude-accuracy" class="field">&nbsp;</div>
    <div>±meters</div>
    <div id="heading" class="field">&nbsp;</div>
    <div>°</div>
    <div id="speed" class="field">&nbsp;</div>
    <div>meters/second</div>
    <div id="status" class="field">&nbsp;</div>
    <div>
        <a id="google" href="https://maps.google.com/"><img src="data:image/x-icon;base64,..." /></a>
        <a id="openstreetmap" href="https://www.openstreetmap.org/"><img src="data:image/png;base64,..." /></a>
        <a id="microsoft" href="https://www.bing.com/maps/"><img src="data:image/x-icon;base64,..." /></a>
    </div>
</div>
```

You can see that each field comes with a label featuring the unit for it value. I also included placeholder links to three popular online map providers (and each of them is using an appropriate favicon image embedded in the HTML file).

## 4. Geolocating

Given that this operation will be used often throughout the code I included two utility functions - one for setting the content of a `div` element and another for setting `href` attribute of an `a` element:

```javascript
function set(id, text) {
    document.getElementById(id).innerHTML = text;
}

function link(id, url) {
    document.getElementById(id).setAttribute("href", url);
}
```

Depending on the circumstances the Geolocation API may return `null` values which I want to display as a questionmark. When the values are available I also want to keep them down to a prescribed accuracy. To facilitate this I created another utility function:

```javascript
function safe(value, digits) {
    return value != null ? value.toFixed(digits) : "?";
}
```

The core of the functionality using the Geolocation API is as follows:

```javascript
function updated(position) {
    var timestamp = new Date(position.timestamp);
    var latitude = position.coords.latitude.toFixed(5);
    var longitude = position.coords.longitude.toFixed(5);
    set("coordinates", `${latitude},${longitude}`);
    set("accuracy", safe(position.coords.accuracy, 0));
    set("altitude", safe(position.coords.altitude, 0));
    set("altitude-accuracy", safe(position.coords.altitudeAccuracy, 0));
    set("heading", safe(position.coords.heading, 0));
    set("speed", safe(position.coords.speed, 1));
    set("status", `${timestamp.toLocaleDateString()} ${timestamp.toLocaleTimeString()}`);
    link("google", `https://maps.google.com/maps?z=17&q=${latitude},${longitude}`);
    link("openstreetmap", `https://www.openstreetmap.org/?zoom=17&mlat=${latitude}&mlon=${longitude}`);
    link("microsoft", `https://www.bing.com/maps/?v=2&lvl=17&cp=${latitude}~${longitude}`);
}

function failed(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            error = "Permission Denied";
            break;
        case error.POSITION_UNAVAILABLE:
            error = "Position Unavailable";
            break;
        case error.TIMEOUT:
            error = "Timeout";
            break;
        default:
            error = `Error: ${error.code}`;
    }
    set("status", error);
}

function request() {
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(updated, failed, { enableHighAccuracy: true });
    }
}

request();
```

You can see that the code is using the `watchPosition` function which registers callbacks - one to receive the geographical position whenever there is an update and another to receive the error in case of a failure. Please note that the `status` field has an overloaded function - it either shows the timestamp of the last update or the error in absence of an update.

## 5. Retry Functionality

In case the user declines granting access to the location and later changes their mind I added a "retry" button:

```html
<div id="card">

    <a href="#" onclick="retry()">↻</a>
</div>
```

I did not want it to look like a link, thus I skipped the underlining:

```css
a {
    text-decoration: none;
}
```

All it does is that the page gets reloaded:

```javascript
function retry() {
    location.reload();
}
```

## 6. Style & Viewport Size

Though the form factors that the app can be rendered on can differ wildly, I still wanted it to look similar and esthetically pleasing. First of all I made the font size match the viewport size:

```css
body {

    font-size: 4vmin;
}

a {

    font-size: 10vmin;
}

img {
    width: 6vmin;
    height: 6vmin;
}
```

I also decided to stick to the black-and-white looks so the "Retry" button and the links to maps received appropriate styling:

```css
a {

    color: white;
}

img {

    filter: grayscale(100%);
}
```

I also centered the `div` element with all placeholders and preserved some space around it to prevent the values and their labels from getting to close to the edges of the screen:

```css
#card {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 95%;
    height: 95%;
}
```

Last, but not least, I used the flex layout to space the fields and labels evenly and ceter them within the viewport:

```css
#card {

    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
}
```
