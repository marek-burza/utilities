/*

This is a simple code demonstrating how to capture DDR events.
It is assumed here that the DDR is an HID device (not all of them are).

The MIT License (MIT)

Copyright (c) 2016 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

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
