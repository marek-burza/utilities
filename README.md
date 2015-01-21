Web-DDR
=======

I needed to prototype quickly a system which was supposed to use input from a Dance Dance Revolution mat. Fortunately I remembered that some mats are simply USB HID devices and thus perceived by a computer as a keyboard (with a limited number of keys). I had just such mat at my disposal so I quickly prototyped a handy JavaScript library for use by the system.

Here is the library/script itself:

[ddr.js](ddr.js)

And that's how you can use it:

[ddr.html](ddr.html)

See the example in action [here](https://rawgit.com/altermarkive/Web-DDR/master/ddr.html) (press arrow buttons if you don't have a DDR mat).