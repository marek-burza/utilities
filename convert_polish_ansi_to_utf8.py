# Python script converting polish text files from ANSI to UTF8.
# Just drag and drop the files onto this script.
#
# This code is free software: you can redistribute it and/or modify it under the
# terms of  the  GNU  Lesser  General  Public  License  as published by the Free
# Software Foundation,  either version 3 of the License, or (at your option) any
# later version.
#
# This code is distributed in the hope that it will be useful, but  WITHOUT  ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See  the  GNU  Lesser  General  Public  License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with code. If not, see http://www.gnu.org/licenses/.

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
def convert(file):
    file = open(file, 'r+b')
    text = '\xEF\xBB\xBF'
    while True:
        byte = file.read(1)
        if '' == byte:
            break
        if byte in mapANSI2UTF8:
            text += mapANSI2UTF8[byte]
        else:
            text += byte
    file.seek(0)
    file.truncate(0)
    file.write(text)
    file.close()

# Runs conversion for every file passed as input argument
for file in sys.argv[1:]:
    convert(file)
