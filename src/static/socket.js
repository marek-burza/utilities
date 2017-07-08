class Conduit {
  constructor(url) {
    var socket = this.socket = new WebSocket(url);
    socket.onopen = function() {
      console.log("Ready");
    };
    socket.onmessage = function (message) {
      alert(message.data);
    };
    socket.onclose = function (event) {
      console.log(event);
    }
    socket.onerror = function (event) {
      console.log(event);
    };
  }

  send(data){
    this.socket.send(data);
  }
}

var origin = window.location.href;
origin = origin.substring(origin.indexOf("//") + 2);
origin = origin.substring(0, origin.indexOf("/"));
var conduit = new Conduit("ws://" + origin + "/ws", this);

function post(message) {
  if ("undefined" !== typeof message) {
    conduit.send(message);
  }
}
