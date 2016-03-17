/*
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

package altermarkive.utilities;

/**
 * With the methods of this Java class you can write/read 1, 2, 4 or 8 byte long signed/unsigned
 * integers with big/little endianness from a byte array at any offset.
 */
public class Bytes {
    /**
     * Writes a multi-byte integer in little-endian byte order into a byte array
     * at the given offset.
     *
     * @param value  A multi-byte integer to be written.
     * @param data   Byte array where the value will be written to.
     * @param offset Offset within the byte array where the value will be written.
     * @param count  Number of bytes to be written.
     */
    public static void putLE(long value, byte[] data, int offset, int count) {
        for (int i = 0; i < count; i++) {
            data[offset] = (byte) (value & 0xFF);
            offset++;
            value >>= 8;
        }
    }

    /**
     * Reads a multi-byte integer in little-endian byte order from a byte array
     * at the given offset.
     *
     * @param data   Byte array where the value will be read from.
     * @param offset Offset within the byte array where the value will be read.
     * @param count  Number of bytes to be written.
     * @param signed Indicates whether the value should preserve the sign
     * @return A multi-byte integer read.
     */
    public static long getLE(byte[] data, int offset, int count, boolean signed) {
        long value = 0;
        for (int i = 0; i < count; i++) {
            value >>>= 8;
            value |= ((long) data[offset]) << 56;
            offset++;
        }
        if (signed) {
            value >>= (8 - count) * 8;
        } else {
            value >>>= (8 - count) * 8;
        }
        return (value);
    }

    /**
     * Writes a multi-byte integer in big-endian byte order into a byte array
     * at the given offset.
     *
     * @param value  A multi-byte integer to be written.
     * @param data   Byte array where the value will be written to.
     * @param offset Offset within the byte array where the value will be written.
     * @param count  Number of bytes to be written.
     */
    public static void putBE(long value, byte[] data, int offset, int count) {
        offset += count - 1;
        for (int i = 0; i < count; i++) {
            data[offset] = (byte) (value & 0xFF);
            offset--;
            value >>= 8;
        }
    }

    /**
     * Reads a multi-byte integer in big-endian byte order from a byte array
     * at the given offset.
     *
     * @param data   Byte array where the value will be read from.
     * @param offset Offset within the byte array where the value will be read.
     * @param count  Number of bytes to be written.
     * @param signed Indicates whether the value should preserve the sign
     * @return A multi-byte integer read.
     */
    public static long getBE(byte[] data, int offset, int count, boolean signed) {
        offset += count - 1;
        long value = 0;
        for (int i = 0; i < count; i++) {
            value >>>= 8;
            value |= ((long) data[offset]) << 56;
            offset--;
        }
        if (signed) {
            value >>= (8 - count) * 8;
        } else {
            value >>>= (8 - count) * 8;
        }
        return (value);
    }
}
