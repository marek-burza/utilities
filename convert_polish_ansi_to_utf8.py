# Python script converting polish text files from ANSI to UTF8.
# Just drag and drop the files onto this script.
#
# The MIT License (MIT)
#
# Copyright (c) 2016 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys

# Mapping from ANSI to UTF-8
mapANSI2UTF8 = {
    '\xB9':'\xC4\x85',
    '\xE6':'\xC4\x87',
    '\xEA':'\xC4\x99',
    '\xB3':'\xC5\x82',
    '\xF1':'\xC5\x84',
    '\xF3':'\xC3\xB3',
    '\x9C':'\xC5\x9B',
    '\x9F':'\xC5\xBA',
    '\xBF':'\xC5\xBC',
    '\xA5':'\xC4\x84',
    '\xC6':'\xC4\x86',
    '\xCA':'\xC4\x98',
    '\xA3':'\xC5\x81',
    '\xD1':'\xC5\x83',
    '\xD3':'\xC3\x93',
    '\x8C':'\xC5\x9A',
    '\x8F':'\xC5\xB9',
    '\xAF':'\xC5\xBB'
    }

# Mapping from ANSI to ASCII (in case anyone prefers)
mapANSI2ASCII = {
    '\xB9':'a',
    '\xE6':'c',
    '\xEA':'e',
    '\xB3':'l',
    '\xF1':'n',
    '\xF3':'o',
    '\x9C':'s',
    '\x9F':'z',
    '\xBF':'z',
    '\xA5':'A',
    '\xC6':'C',
    '\xCA':'E',
    '\xA3':'L',
    '\xD1':'N',
    '\xD3':'O',
    '\x8C':'S',
    '\x8F':'Z',
    '\xAF':'Z'
    }

# Processes a file byte-by-byte and converts polish characters from ANSI to UTF8
def convert(path):
    srt = open(path, 'rb')
    text = '\xEF\xBB\xBF'
    while True:
        byte = srt.read(1)
        if '' == byte:
            break
        if byte in mapANSI2UTF8:
            text += mapANSI2UTF8[byte]
        else:
            text += byte
    srt.close()
    srt = open(path, 'wb')
    srt.write(text)
    srt.close()

# Runs conversion for every file passed as input argument
for file in sys.argv[1:]:
    convert(file)
