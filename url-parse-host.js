/*

The urlParseHost function implemented here extracts the host from a URL.

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

// Use this function with window.location.href to find out the origin host
function urlParseHost(url){
  var re = new RegExp("^(?:f|ht)tp(?:s)?\://([^/]+)", "im");
  return(url.match(re)[1].toString());
}
