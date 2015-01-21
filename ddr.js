/*

This is a simple code demonstrating how to capture DDR events.
It is assumed here that the DDR is an HID device (not all of them are).

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

// Internal variable which keeps the DDR status
var ddrStatus = {left:false, up:false, right:false, down:false};

// Keeps the reference to the DDR status callback
var ddrCallback = null;

// Use outside of this script to register a DDR status callback
function ddrRegister(callback){
  ddrCallback = callback;
}

// Remember the original keyboard event handlers
var ddrDown = document.onkeydown;
var ddrUp = document.onkeyup;

// Capture DDR (HID keyboard) key down events
document.onkeydown = function(e){
  // Catch only the direction/arrow keys
  if(e.keyCode == 37){ ddrStatus.left  = true; }
  if(e.keyCode == 38){ ddrStatus.up    = true; }
  if(e.keyCode == 39){ ddrStatus.right = true; }
  if(e.keyCode == 40){ ddrStatus.down  = true; }
  // Call the callback only if registered
  if(null != ddrCallback){
    ddrCallback(ddrStatus);
  }
  // Call the original handler if there was one
  if(null != ddrDown){
    ddrDown(e);
  }
}

// Capture DDR (HID keyboard) key up events
document.onkeyup = function(e){
  // Catch only the direction/arrow keys
  if(e.keyCode == 37){ ddrStatus.left  = false; }
  if(e.keyCode == 38){ ddrStatus.up    = false; }
  if(e.keyCode == 39){ ddrStatus.right = false; }
  if(e.keyCode == 40){ ddrStatus.down  = false; }
  // Call the callback only if registered
  if(null != ddrCallback){
    ddrCallback(ddrStatus);
  }
  // Call the original handler if there was one
  if(null != ddrUp){
    ddrUp(e);
  }
}
