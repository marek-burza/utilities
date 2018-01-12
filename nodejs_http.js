var http = require('http');

console.log("Hello World");

var headers = {
  "Content-Type": "application/json"
}
var options = {
    host: "samples.openweathermap.org",
    path: "/data/2.5/weather?q=London",
    method: "GET",
    headers: headers
  };
  http.request(options, function(res) {
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    res.setEncoding('utf8');
    res.on('data', function (chunk) {
      console.log('BODY: ' + chunk);
    });
  }).end();
