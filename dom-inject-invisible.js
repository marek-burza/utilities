/*

This code injects an invisible DIV element with specified HTML content.

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

// Injects an invisible DIV element with specified HTML content
function domInjectInvisible(html){
  var parent = null;
  try{
    parent = document.getElementsByTagName("body")[0];
  }catch(exception){
    parent = document.getElementsByTagName("head")[0];
  }
  var div = document.createElement("div");
  div.style.width  = "0";
  div.style.height = "0";
  div.style.display = "block";
  div.style.overflow = "hidden";
  div.innerHTML = html;
  parent.appendChild(div);
}
