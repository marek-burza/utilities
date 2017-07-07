"use strict";

var path = require('path');
var express = require('express');

const app = express();

app.use(express.static('../shell-app'));

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname + '../shell-app/index.html'));
});

app.listen(8081);
