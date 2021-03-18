# Geolocation API in an iOS Web App

## TL;DR

This experiment started with a simple need for quickly looking up my current geographical coordinates (latitude & longitude) on my iPhone. Surely, there's an app for that, but it felt like an overkill - I just wanted something disposable, light-weight, self-contained. There's barely anything fitting the bill better than a single-file Progressive Web Aapp which can be added to the home screen. If that's all you'd like to know about it, you can go ahead and click [here](https://altermarkive.github.io/web-experiments/location/).

## 1. Web App Template

I started with a minimalistic HTML file:

```html
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8" />
    <title>⤓</title>
    <style>
        body {
            background-color: white;
            color: black;
        }
    </style>
</head>

<body>
    <center>
        <h1>⤓</h1>
    </center>
</body>

</html>
```

Then, I added an indication for the Safari browser that the HTML file can run as a full-screen web app with a default status bar and an unassuming app name:

```html
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="default" />
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

## 2. Rigid View

Typically, Safari goes a long way towards adaptive scaling & adding bounce effects when scrolling.
Instead, I wanted to have a more rigid view and to disable some of those effects.

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

And last, I disable the bounce effect when the user is attempting scrolling.

```css
body,
html {
    height: 100%;
    overflow: hidden;
    position: relative;
}
```
