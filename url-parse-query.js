/*

The urlParseQuery function implemented here extracts the key-value pairs
from the query portion of a URL.

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

// Use this function with window.location.href to parse own query
function urlParseQuery(url){
  var re = new RegExp("[?&]+([^=&]+)=([^&]*)", "gi");
  var map = {};
  var parts = url.replace(re, function(ignore, key, value){map[key] = decodeURIComponent(value);});
  return(map);
}
