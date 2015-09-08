/*
This code is free software: you can redistribute it and/or modify it under the
terms of  the  GNU  Lesser  General  Public  License  as published by the Free
Software Foundation,  either version 3 of the License, or (at your option) any
later version.

This code is distributed in the hope that it will be useful, but  WITHOUT  ANY
WARRANTY;  without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See  the  GNU  Lesser  General  Public  License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with code. If not, see http://www.gnu.org/licenses/.
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
