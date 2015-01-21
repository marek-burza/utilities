/*

UNIVERSAL ANIMATOR
This library is simplifying HTML5 animations in a web browser independent way.

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

// Ancient and most browser-compatible way of animating
function uaAncient(frame){
  window.setTimeout(frame, 1000.0 / 25.0);
}

// Holds function which requests animation for a specific web browser
var uaAnimator =  window.requestAnimationFrame
               || window.webkitRequestAnimationFrame
               || window.mozRequestAnimationFrame
               || window.oRequestAnimationFrame
               || window.msRequestAnimationFrame
               || uaAncient;

// Function which will trigger the animation
function uaAnimate(frame){
  frame();
  uaAnimator(function(){uaAnimate(frame);});
}


