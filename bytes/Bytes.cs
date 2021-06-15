using System;
using System.Text;

namespace bytes
{
    /// <summary>
    /// With the methods of this Java class you can write/read 1, 2, 4 or 8 byte long signed/unsigned
    /// integers with big/little endianness from a byte array at any offset.
    /// </summary>
    public class Bytes
    {
        /// <summary>
        /// Writes a multi-byte integer in little-endian byte order into a byte array
        /// at the given offset.
        /// </summary>
        /// <param name="value">A multi-byte integer to be written.</param>
        /// <param name="data">Byte array where the value will be written to.</param>
        /// <param name="offset">Offset within the byte array where the value will be written.</param>
        /// <param name="count">Number of bytes to be written.</param>
        public static void PutLE(long value, byte[] data, int offset, int count)
        {
            for (int i = 0; i < count; i++)
            {
                data[offset] = (byte)(value & 0xFF);
                offset++;
                value >>= 8;
            }
        }

        /// <summary>
        /// Reads a multi-byte integer in little-endian byte order from a byte array
        /// at the given offset.
        /// </summary>
        /// <param name="data">Byte array where the value will be read from.</param>
        /// <param name="offset">Offset within the byte array where the value will be read.</param>
        /// <param name="count">Number of bytes to be written.</param>
        /// <param name="signed">Indicates whether the value should preserve the sign.</param>
        /// <returns>
        /// A multi-byte integer read.
        /// </returns>
        public static long GetLE(byte[] data, int offset, int count, bool signed)
        {
            long value = 0;
            for (int i = 0; i < count; i++)
            {
                value = (long)((ulong)value >> 8);
                value |= ((long)data[offset]) << 56;
                offset++;
            }
            if (signed)
            {
                value >>= (8 - count) * 8;
            }
            else
            {
                value = (long)((ulong)value >> ((8 - count) * 8));
            }
            return (value);
        }

        /// <summary>
        /// Writes a multi-byte integer in big-endian byte order into a byte array
        /// at the given offset.
        /// </summary>
        /// <param name="value">A multi-byte integer to be written.</param>
        /// <param name="data">Byte array where the value will be written to.</param>
        /// <param name="offset">Offset within the byte array where the value will be written.</param>
        /// <param name="count">Number of bytes to be written.</param>
        public static void PutBE(long value, byte[] data, int offset, int count)
        {
            offset += count - 1;
            for (int i = 0; i < count; i++)
            {
                data[offset] = (byte)(value & 0xFF);
                offset--;
                value >>= 8;
            }
        }

        /// <summary>
        /// Reads a multi-byte integer in big-endian byte order from a byte array
        /// at the given offset.
        /// </summary>
        /// <param name="data">Byte array where the value will be read from.</param>
        /// <param name="offset">Offset within the byte array where the value will be read.</param>
        /// <param name="count">Number of bytes to be written.</param>
        /// <param name="signed">Indicates whether the value should preserve the sign.</param>
        /// <returns>
        /// A multi-byte integer read.
        /// </returns>
        public static long GetBE(byte[] data, int offset, int count, bool signed)
        {
            offset += count - 1;
            long value = 0;
            for (int i = 0; i < count; i++)
            {
                value = (long)((ulong)value >> 8);
                value |= ((long)data[offset]) << 56;
                offset--;
            }
            if (signed)
            {
                value >>= (8 - count) * 8;
            }
            else
            {
                value = (long)((ulong)value >> ((8 - count) * 8));
            }
            return (value);
        }

        public static string ByteArrayToString(byte[] bytes)
        {
            StringBuilder hex = new StringBuilder(bytes.Length * 2);
            foreach (byte octet in bytes)
            {
                hex.AppendFormat("{0:x2}", octet);
            }
            return hex.ToString();
        }

        public static byte[] StringToByteArray(string hex)
        {
            int length = hex.Length;
            byte[] bytes = new byte[length / 2];
            for (int i = 0; i < length; i += 2)
            {
                bytes[i / 2] = Convert.ToByte(hex.Substring(i, 2), 16);
            }
            return bytes;
        }

        public static void Main(string[] args)
        {
            if (args.Length < 1)
            {
                System.Console.WriteLine("ERROR - First argument must be one of: 'pl', 'gl', 'pb', 'gb'");
                return;
            }
            if (args.Length < 5)
            {
                System.Console.WriteLine("ERROR - There must be five arguments");
                return;
            }
            switch (args[0])
            {
                case "pl":
                    {
                        long value = Int64.Parse(args[1]);
                        byte[] data = StringToByteArray(args[2]);
                        int offset = Int32.Parse(args[3]);
                        int count = Int32.Parse(args[4]);
                        PutLE(value, data, offset, count);
                        System.Console.WriteLine(ByteArrayToString(data));
                    }
                    break;
                case "gl":
                    {
                        byte[] data = StringToByteArray(args[1]);
                        int offset = Int32.Parse(args[2]);
                        int count = Int32.Parse(args[3]);
                        bool signed = Boolean.Parse(args[4]);
                        long result = GetLE(data, offset, count, signed);
                        System.Console.WriteLine("Hex: {0:X}", result);
                    }
                    break;
                case "pb":
                    {
                        long value = Int64.Parse(args[1]);
                        byte[] data = StringToByteArray(args[2]);
                        int offset = Int32.Parse(args[3]);
                        int count = Int32.Parse(args[4]);
                        PutBE(value, data, offset, count);
                        System.Console.WriteLine(ByteArrayToString(data));
                    }
                    break;
                case "gb":
                    {
                        byte[] data = StringToByteArray(args[1]);
                        int offset = Int32.Parse(args[2]);
                        int count = Int32.Parse(args[3]);
                        bool signed = Boolean.Parse(args[4]);
                        long result = GetLE(data, offset, count, signed);
                        System.Console.WriteLine("Hex: {0:X}", result);
                    }
                    break;
                default:
                    System.Console.WriteLine("ERROR - First argument must be one of: 'pl', 'gl', 'pb', 'gb'");
                    break;
            }
        }
    }
}