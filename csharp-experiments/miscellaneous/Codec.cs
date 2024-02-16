// <copyright file="Codec.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using System.Buffers.Binary;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Text;
    using Microsoft.Extensions.Logging;
    using Newtonsoft.Json;
    using Newtonsoft.Json.Linq;

    /// <summary>
    /// Codec class of the application.
    /// </summary>
    public sealed class Codec
    {
        private readonly Endian endianness;
        private readonly Type[] types;
        private readonly string[] fields;
        private readonly int size;

        /// <summary>
        /// Initializes a new instance of the <see cref="Codec"/> class.
        /// </summary>
        /// <param name="endianness">Endianness.</param>
        /// <param name="types">Field types.</param>
        /// <param name="fields">Field names.</param>
        public Codec(Endian endianness, Type[] types, string[] fields)
        {
            Debug.Assert(types.Length == fields.Length, "Cardinality of types and fields must be the same");
            this.endianness = endianness;
            this.types = types;
            this.fields = fields;
            this.size = this.CalculateSize();
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="Codec"/> class.
        /// </summary>
        /// <param name="codec">Codec definition in JSON.</param>
        public Codec(JObject codec)
        {
            this.endianness = EndianFromName(codec["endian"].ToString().ToLower());
            this.types = TypesFromNames((JArray)codec["types"]);
            this.fields = codec["fields"].ToObject<List<string>>().ToArray();
            this.size = this.CalculateSize();
        }

        /// <summary>
        /// Endianness.
        /// </summary>
        public enum Endian : int
        {
            /// <summary>
            /// Represents little-endian byte order.
            /// </summary>
            Little,

            /// <summary>
            /// Represents big-endian byte order.
            /// </summary>
            Big,

            /// <summary>
            /// Represents unknown endian byte order.
            /// </summary>
            Unknown,
        }

        /// <summary>
        /// Field type.
        /// </summary>
        public enum Type : int
        {
            /// <summary>
            /// Represents 8-bit unsigned integer.
            /// </summary>
            U8,

            /// <summary>
            /// Represents 8-bit signed integer.
            /// </summary>
            S8,

            /// <summary>
            /// Represents 16-bit unsigned integer.
            /// </summary>
            U16,

            /// <summary>
            /// Represents 16-bit signed integer.
            /// </summary>
            S16,

            /// <summary>
            /// Represents 32-bit unsigned integer.
            /// </summary>
            U32,

            /// <summary>
            /// Represents 32-bit signed integer.
            /// </summary>
            S32,

            /// <summary>
            /// Represents 64-bit unsigned integer.
            /// </summary>
            U64,

            /// <summary>
            /// Represents 64-bit signed integer.
            /// </summary>
            S64,

            /// <summary>
            /// Represents 32-bit float.
            /// </summary>
            F32,

            /// <summary>
            /// Represents 64-bit float.
            /// </summary>
            F64,

            /// <summary>
            /// Represents boolean.
            /// </summary>
            B,

            /// <summary>
            /// Represents an unknown type.
            /// </summary>
            Unknown,
        }

        /// <summary>
        /// Logs hex outcome.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void ConvertToHex(string argument, ILogger logger)
        {
            logger.LogInformation(Hex(Encoding.UTF8.GetBytes(argument)));
        }

        /// <summary>
        /// Logs codec outcome.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogCodec(string argument, ILogger logger)
        {
            JObject batch = JObject.Parse(argument);
            Codec codec = new Codec((JObject)batch["codec"]);
            string operation = batch["operation"].ToString().ToLower();

            if ("encode".Equals(operation))
            {
                byte[] octets = new byte[codec.size];
                codec.Encode((JObject)batch["content"], octets);
                logger.LogInformation(Hex(octets));
            }

            if ("decode".Equals(operation))
            {
                byte[] octets = batch["octets"].ToObject<List<byte>>().ToArray();
                JObject content = new JObject();
                codec.Decode(octets, content);
                logger.LogInformation(JsonConvert.SerializeObject(content));
            }
        }

        private static Endian EndianFromName(string endianName)
        {
            if ("little".Equals(endianName))
            {
                return Endian.Little;
            }

            if ("big".Equals(endianName))
            {
                return Endian.Big;
            }

            return Endian.Unknown;
        }

        private static Type[] TypesFromNames(JArray typeNames)
        {
            List<Type> types = new List<Type>();
            foreach (string typeRaw in typeNames)
            {
                string typeName = typeRaw.ToUpper();
                Type type = Type.Unknown;
                if ("U8".Equals(typeName))
                {
                    type = Type.U8;
                }

                if ("S8".Equals(typeName))
                {
                    type = Type.S8;
                }

                if ("U16".Equals(typeName))
                {
                    type = Type.U16;
                }

                if ("S16".Equals(typeName))
                {
                    type = Type.S16;
                }

                if ("U32".Equals(typeName))
                {
                    type = Type.U32;
                }

                if ("S32".Equals(typeName))
                {
                    type = Type.S32;
                }

                if ("U64".Equals(typeName))
                {
                    type = Type.U64;
                }

                if ("S64".Equals(typeName))
                {
                    type = Type.S64;
                }

                if ("F32".Equals(typeName))
                {
                    type = Type.F32;
                }

                if ("F64".Equals(typeName))
                {
                    type = Type.F64;
                }

                if ("B".Equals(typeName))
                {
                    type = Type.B;
                }

                types.Add(type);
            }

            return types.ToArray();
        }

        private static int TypeToSize(Type type)
        {
            switch (type)
            {
                case Type.U8:
                case Type.S8:
                case Type.B:
                    return 1;
                case Type.U16:
                case Type.S16:
                    return 2;
                case Type.U32:
                case Type.S32:
                case Type.F32:
                    return 4;
                case Type.U64:
                case Type.S64:
                case Type.F64:
                    return 8;
                default:
                    return 0;
            }
        }

        private static bool IsCompatible(Type type, JToken token)
        {
            switch (type)
            {
                case Type.U8:
                case Type.S8:
                case Type.U16:
                case Type.S16:
                case Type.U32:
                case Type.S32:
                case Type.U64:
                case Type.S64:
                    return token.Type == JTokenType.Integer;
                case Type.F32:
                case Type.F64:
                    return token.Type == JTokenType.Float;
                case Type.B:
                    return token.Type == JTokenType.Boolean;
                default:
                    return false;
            }
        }

        private static string Hex(Span<byte> octets) => BitConverter.ToString(octets.ToArray()).Replace("-", string.Empty);

        private int CalculateSize()
        {
            int size = 0;
            foreach (Type type in this.types)
            {
                size += TypeToSize(type);
            }

            return size;
        }

        private bool IsCompatible(JObject content)
        {
            for (int i = 0; i < this.types.Length; i++)
            {
                if (!IsCompatible(this.types[i], content[this.fields[i]]))
                {
                    return false;
                }
            }

            return true;
        }

        private void Decode(Span<byte> octets, JObject content)
        {
            switch (this.endianness)
            {
                case Endian.Little:
                    this.DecodeLittle(octets, content);
                    break;
                case Endian.Big:
                    this.DecodeBig(octets, content);
                    break;
            }
        }

        private void DecodeLittle(Span<byte> octets, JObject content)
        {
            for (int i = 0, offset = 0; i < this.types.Length; i++)
            {
                switch (this.types[i])
                {
                    case Type.U8:
                        content[this.fields[i]] = (byte)octets[offset];
                        break;
                    case Type.S8:
                        content[this.fields[i]] = (sbyte)octets[offset];
                        break;
                    case Type.U16:
                        content[this.fields[i]] = BinaryPrimitives.ReadUInt16LittleEndian(octets.Slice(offset));
                        break;
                    case Type.S16:
                        content[this.fields[i]] = BinaryPrimitives.ReadInt16LittleEndian(octets.Slice(offset));
                        break;
                    case Type.U32:
                        content[this.fields[i]] = BinaryPrimitives.ReadUInt32LittleEndian(octets.Slice(offset));
                        break;
                    case Type.S32:
                        content[this.fields[i]] = BinaryPrimitives.ReadInt32LittleEndian(octets.Slice(offset));
                        break;
                    case Type.U64:
                        content[this.fields[i]] = BinaryPrimitives.ReadUInt64LittleEndian(octets.Slice(offset));
                        break;
                    case Type.S64:
                        content[this.fields[i]] = BinaryPrimitives.ReadInt64LittleEndian(octets.Slice(offset));
                        break;
                    case Type.F32:
                        int f32 = BinaryPrimitives.ReadInt32LittleEndian(octets.Slice(offset));
                        if (!BitConverter.IsLittleEndian)
                        {
                            f32 = BinaryPrimitives.ReverseEndianness(f32);
                        }

                        content[this.fields[i]] = BitConverter.Int32BitsToSingle(f32);
                        break;
                    case Type.F64:
                        long f64 = BinaryPrimitives.ReadInt64LittleEndian(octets.Slice(offset));
                        if (!BitConverter.IsLittleEndian)
                        {
                            f64 = BinaryPrimitives.ReverseEndianness(f64);
                        }

                        content[this.fields[i]] = BitConverter.Int64BitsToDouble(f64);
                        break;
                    case Type.B:
                        content[this.fields[i]] = octets[offset] == 1;
                        break;
                }

                offset += TypeToSize(this.types[i]);
            }
        }

        private void DecodeBig(Span<byte> octets, JObject content)
        {
            for (int i = 0, offset = 0; i < this.types.Length; i++)
            {
                switch (this.types[i])
                {
                    case Type.U8:
                        content[this.fields[i]] = (byte)octets[offset];
                        break;
                    case Type.S8:
                        content[this.fields[i]] = (sbyte)octets[offset];
                        break;
                    case Type.U16:
                        content[this.fields[i]] = BinaryPrimitives.ReadUInt16BigEndian(octets.Slice(offset));
                        break;
                    case Type.S16:
                        content[this.fields[i]] = BinaryPrimitives.ReadInt16BigEndian(octets.Slice(offset));
                        break;
                    case Type.U32:
                        content[this.fields[i]] = BinaryPrimitives.ReadUInt32BigEndian(octets.Slice(offset));
                        break;
                    case Type.S32:
                        content[this.fields[i]] = BinaryPrimitives.ReadInt32BigEndian(octets.Slice(offset));
                        break;
                    case Type.U64:
                        content[this.fields[i]] = BinaryPrimitives.ReadUInt64BigEndian(octets.Slice(offset));
                        break;
                    case Type.S64:
                        content[this.fields[i]] = BinaryPrimitives.ReadInt64BigEndian(octets.Slice(offset));
                        break;
                    case Type.F32:
                        int f32 = BinaryPrimitives.ReadInt32BigEndian(octets.Slice(offset));
                        if (BitConverter.IsLittleEndian)
                        {
                            f32 = BinaryPrimitives.ReverseEndianness(f32);
                        }

                        content[this.fields[i]] = BitConverter.Int32BitsToSingle(f32);
                        break;
                    case Type.F64:
                        long f64 = BinaryPrimitives.ReadInt64BigEndian(octets.Slice(offset));
                        if (BitConverter.IsLittleEndian)
                        {
                            f64 = BinaryPrimitives.ReverseEndianness(f64);
                        }

                        content[this.fields[i]] = BitConverter.Int64BitsToDouble(f64);
                        break;
                    case Type.B:
                        content[this.fields[i]] = octets[offset] == 1;
                        break;
                }

                offset += TypeToSize(this.types[i]);
            }
        }

        private void Encode(JObject content, Span<byte> octets)
        {
            switch (this.endianness)
            {
                case Endian.Little:
                    this.EncodeLittle(content, octets);
                    break;
                case Endian.Big:
                    this.EncodeBig(content, octets);
                    break;
            }
        }

        private void EncodeLittle(JObject content, Span<byte> octets)
        {
            for (int i = 0, offset = 0; i < this.types.Length; i++)
            {
                switch (this.types[i])
                {
                    case Type.U8:
                    case Type.S8:
                        octets[offset] = (byte)content[this.fields[i]];
                        break;
                    case Type.U16:
                        BinaryPrimitives.WriteUInt16LittleEndian(octets.Slice(offset), (ushort)content[this.fields[i]]);
                        break;
                    case Type.S16:
                        BinaryPrimitives.WriteInt16LittleEndian(octets.Slice(offset), (short)content[this.fields[i]]);
                        break;
                    case Type.U32:
                        BinaryPrimitives.WriteUInt32LittleEndian(octets.Slice(offset), (uint)content[this.fields[i]]);
                        break;
                    case Type.S32:
                        BinaryPrimitives.WriteInt32LittleEndian(octets.Slice(offset), (int)content[this.fields[i]]);
                        break;
                    case Type.U64:
                        BinaryPrimitives.WriteUInt64LittleEndian(octets.Slice(offset), (ulong)content[this.fields[i]]);
                        break;
                    case Type.S64:
                        BinaryPrimitives.WriteInt64LittleEndian(octets.Slice(offset), (long)content[this.fields[i]]);
                        break;
                    case Type.F32:
                        int f32 = BitConverter.SingleToInt32Bits((float)content[this.fields[i]]);
                        if (!BitConverter.IsLittleEndian)
                        {
                            f32 = BinaryPrimitives.ReverseEndianness(f32);
                        }

                        BinaryPrimitives.WriteInt32LittleEndian(octets.Slice(offset), f32);
                        break;
                    case Type.F64:
                        long f64 = BitConverter.DoubleToInt64Bits((double)content[this.fields[i]]);
                        if (!BitConverter.IsLittleEndian)
                        {
                            f64 = BinaryPrimitives.ReverseEndianness(f64);
                        }

                        BinaryPrimitives.WriteInt64LittleEndian(octets.Slice(offset), f64);
                        break;
                    case Type.B:
                        octets[offset] = ((bool)content[this.fields[i]]) ? (byte)1 : (byte)0;
                        break;
                }

                offset += Codec.TypeToSize(this.types[i]);
            }
        }

        private void EncodeBig(JObject content, Span<byte> octets)
        {
            for (int i = 0, offset = 0; i < this.types.Length; i++)
            {
                switch (this.types[i])
                {
                    case Type.U8:
                    case Type.S8:
                        octets[offset] = (byte)content[this.fields[i]];
                        break;
                    case Type.U16:
                        BinaryPrimitives.WriteUInt16BigEndian(octets.Slice(offset), (ushort)content[this.fields[i]]);
                        break;
                    case Type.S16:
                        BinaryPrimitives.WriteInt16BigEndian(octets.Slice(offset), (short)content[this.fields[i]]);
                        break;
                    case Type.U32:
                        BinaryPrimitives.WriteUInt32BigEndian(octets.Slice(offset), (uint)content[this.fields[i]]);
                        break;
                    case Type.S32:
                        BinaryPrimitives.WriteInt32BigEndian(octets.Slice(offset), (int)content[this.fields[i]]);
                        break;
                    case Type.U64:
                        BinaryPrimitives.WriteUInt64BigEndian(octets.Slice(offset), (ulong)content[this.fields[i]]);
                        break;
                    case Type.S64:
                        BinaryPrimitives.WriteInt64BigEndian(octets.Slice(offset), (long)content[this.fields[i]]);
                        break;
                    case Type.F32:
                        int f32 = BitConverter.SingleToInt32Bits((float)content[this.fields[i]]);
                        if (BitConverter.IsLittleEndian)
                        {
                            f32 = BinaryPrimitives.ReverseEndianness(f32);
                        }

                        BinaryPrimitives.WriteInt32BigEndian(octets.Slice(offset), f32);
                        break;
                    case Type.F64:
                        long f64 = BitConverter.DoubleToInt64Bits((double)content[this.fields[i]]);
                        if (BitConverter.IsLittleEndian)
                        {
                            f64 = BinaryPrimitives.ReverseEndianness(f64);
                        }

                        BinaryPrimitives.WriteInt64BigEndian(octets.Slice(offset), f64);
                        break;
                    case Type.B:
                        octets[offset] = ((bool)content[this.fields[i]]) ? (byte)1 : (byte)0;
                        break;
                }

                offset += TypeToSize(this.types[i]);
            }
        }
    }
}
