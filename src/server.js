"use strict";

const path = require("path");
const express = require("express");
const http = require("http");
const WSServer = require("ws").Server;

const app = express();

app.use(express.static("/app/static"));

app.get("/", function (request, response) {
  response.sendFile(path.join(__dirname + "/app/static/index.html"));
});

const server = http.createServer(app);

const wss = new WSServer({server: server, path: "/ws"});
wss.on("connection", (ws, req) => {
  ws.on("message", (message) => {
    ws.send(message);
  });
});

server.listen(8081);
