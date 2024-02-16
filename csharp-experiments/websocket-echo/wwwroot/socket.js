var url = document.getElementById("url");
var connect = document.getElementById("connect");
var state = document.getElementById("state");
var message = document.getElementById("message");
var send = document.getElementById("send");
var log = document.getElementById("log");
var disconnect = document.getElementById("disconnect");
var socket;

console.log(document.location.protocol);
console.log(document.location.port);
console.log(document.location.hostname);

var scheme = document.location.protocol === "https:" ? "wss" : "ws";
var port = document.location.port ? (":" + document.location.port) : "";

url.value = scheme + "://" + document.location.hostname + port + "/ws";

function updateState() {
  function disable() {
    message.disabled = true;
    send.disabled = true;
    disconnect.disabled = true;
  }
  function enable() {
    message.disabled = false;
    send.disabled = false;
    disconnect.disabled = false;
  }

  url.disabled = true;
  connect.disabled = true;

  if (!socket) {
    disable();
  } else {
    switch (socket.readyState) {
      case WebSocket.CLOSED:
        state.innerHTML = "Disconnected";
        disable();
        url.disabled = false;
        connect.disabled = false;
        break;
      case WebSocket.CLOSING:
        state.innerHTML = "Disconnecting...";
        disable();
        break;
      case WebSocket.CONNECTING:
        state.innerHTML = "Connecting...";
        disable();
        break;
      case WebSocket.OPEN:
        state.innerHTML = "Connected";
        enable();
        break;
      default:
        state.innerHTML = "Unknown: " + htmlEscape(socket.readyState);
        disable();
        break;
    }
  }
}

disconnect.onclick = function () {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    alert("Socket not connected");
  }
  socket.close(1000, "Closing from client");
};

send.onclick = function () {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    alert("Socket not connected");
  }
  var data = message.value;
  socket.send(data);
  log.innerHTML += "Client -&gt; Server: " + htmlEscape(data) + "<br />";
};

connect.onclick = function () {
  state.innerHTML = "Connecting";
  socket = new WebSocket(url.value);
  socket.onopen = function (event) {
    updateState();
    log.innerHTML += "Connected<br />";
  };
  socket.onclose = function (event) {
    updateState();
    log.innerHTML += "Disconnected (" + htmlEscape(event.code) + "; " + htmlEscape(event.reason) + ")<br />";
  };
  socket.onerror = updateState;
  socket.onmessage = function (event) {
    log.innerHTML += "Server -&gt; Client: " + htmlEscape(event.data) + "<br />"
  };
};

function htmlEscape(str) {
  return str.toString()
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/"/g, "&#39;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
