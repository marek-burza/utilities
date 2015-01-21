/*

Nothing to see here - move along! :)
It's just a basic JavaScript code for getting and posting HTTP requests.

This code is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This code is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with code. If not, see <http://www.gnu.org/licenses/>.

*/

function httpGet(url){
  http = new XMLHttpRequest();
  http.open("GET", url, false);
  http.send(null);
  return({status: http.status, text:http.responseText});
}

function httpPost(url, data){
  http = new XMLHttpRequest();
  http.open("POST", url, false);
  http.send(data);
  return({status: http.status, text:http.responseText});
}
