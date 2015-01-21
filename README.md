Passing JS function/callback to Emscripten-generated code
=========================================================

I needed to compile a piece of C code with Emscripten. It was meant to be called
by a hand-written JavaScript code and reply a string via a callback function
passed as a parameter to the Emscripten-generated code.

It is, in fact, quite simple. First, let's assume that the C code looks like this:

[callback.c](callback.c)

Then, you can compile the code with Emscripten like so:

    emcc callback.c -o callback.js -s EXPORTED_FUNCTIONS="['_call']" 

Next, the call to the Emscripten-generated code is realized with
a following HTML/JavaScript file:

[callback.html](callback.html)

See the example in action [here](https://rawgit.com/altermarkive/Emscripten-Callback/master/callback.html).