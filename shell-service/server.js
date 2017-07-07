"use strict";

const path = require("path");
const express = require("express");
const http = require("http");
const WSServer = require("ws").Server;
const child_process = require("child_process");

const bash = child_process.spawn("/bin/bash");

bash.stdout.on("data", (data) => {
  broadcast(`${data}`);
});

bash.stderr.on("data", (data) => {
  broadcast(`${data}`);
});

bash.on("close", (code) => {
  console.log(`child process exited with code ${code}`);
});


const app = express();

app.use(express.static("../shell-app"));

app.get("/", function (request, response) {
  response.sendFile(path.join(__dirname + "../shell-app/index.html"));
});

const server = http.createServer(app);

const wss = new WSServer({server: server, path: "/ws"});
wss.on("connection", (ws, req) => {
  ws.on("message", (message) => {
    console.log(message);
    bash.stdin.write(message + "\n");
  });
});

function broadcast(data) {
  wss.clients.forEach(function each(ws) {
    ws.send(data);
  });
}

server.listen(8081);
