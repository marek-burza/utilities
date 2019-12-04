// <copyright file="Network.cs" company="altermarkive">
// Copyright (c) 2019 altermarkive.
// </copyright>
namespace Explorer
{
    using System;
    using System.Collections.Generic;
    using System.Net;
    using System.Net.NetworkInformation;
    using System.Net.Sockets;
    using Microsoft.Extensions.Logging;

    /// <summary>
    /// Networking class of the application.
    /// </summary>
    public static class Network
    {
        /// <summary>
        /// Logs the list of network interfaces.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogInterfaces(string argument, ILogger logger)
        {
            logger.LogInformation(FormatInterfaces());
        }

        /// <summary>
        /// Logs the list broadcast addresses.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogBroadcastAddresses(string argument, ILogger logger)
        {
            foreach (IPAddress ip in EnumerateBroadcastAddresses())
            {
                logger.LogInformation(ip.ToString());
            }
        }

        /// <summary>
        /// Logs own IP address on the same subnet as the given one.
        /// </summary>
        /// <param name="argument">Command argument.</param>
        /// <param name="logger">Logger.</param>
        public static void LogMatchingAddress(string argument, ILogger logger)
        {
            logger.LogInformation($"{MatchingOwnAddress(IPAddress.Parse(argument)).ToString()}");
        }

        private static string FormatIPGlobalProperties()
        {
            IPGlobalProperties globalProperties = IPGlobalProperties.GetIPGlobalProperties();
            string result = string.Empty;
            result += $"Computer name:                         {globalProperties.HostName}\n";
            result += $"Domain name:                           {globalProperties.DomainName}\n";
            result += $"Node type:                             {globalProperties.NodeType:f}\n";
            try
            {
                result += $"DHCP scope:                            {globalProperties.DhcpScopeName}\n";
                result += $"WINS proxy:                            {globalProperties.IsWinsProxy}\n";
            }
            catch (PlatformNotSupportedException)
            {
            }

            return result;
        }

        private static string FormatIPAddressInformationCollection(IPAddressInformationCollection collection, string label)
        {
            string result = string.Empty;
            if (collection != null)
            {
                foreach (IPAddressInformation addressInformation in collection)
                {
                    result += string.Format(label, addressInformation.Address.ToString(), addressInformation.IsTransient, addressInformation.IsDnsEligible);
                }
            }

            return result;
        }

        private static string FormatIPAddressCollection(IPAddressCollection collection, string label)
        {
            string result = string.Empty;
            if (collection != null)
            {
                foreach (IPAddress address in collection)
                {
                    result += string.Format(label, address.ToString());
                }
            }

            return result;
        }

        private static string FormatGatewayIPAddressInformationCollection(GatewayIPAddressInformationCollection collection)
        {
            string result = string.Empty;
            if (collection != null)
            {
                foreach (GatewayIPAddressInformation addressInformation in collection)
                {
                    result += $"  Gateway address:                     {addressInformation.Address.ToString()}\n";
                }
            }

            return result;
        }

        private static string FormatMulticastIPAddressInformationCollection(MulticastIPAddressInformationCollection collection)
        {
            string result = string.Empty;
            if (collection != null)
            {
                string dateTimeFormat = "yyyy.MM.dd HH:mm:ss";
                DateTime when;
                foreach (MulticastIPAddressInformation addressInformation in collection)
                {
                    result += $"  Multicast address:                   {addressInformation.Address.ToString()}\n";
                    when = DateTime.UtcNow + TimeSpan.FromSeconds(addressInformation.AddressPreferredLifetime);
                    result += $"    Preferred lifetime:                {when.ToString(dateTimeFormat, System.Globalization.CultureInfo.CurrentCulture)}\n";
                    when = DateTime.UtcNow + TimeSpan.FromSeconds(addressInformation.AddressValidLifetime);
                    result += $"    Valid lifetime:                    {when.ToString(dateTimeFormat, System.Globalization.CultureInfo.CurrentCulture)}\n";
                    when = DateTime.UtcNow + TimeSpan.FromSeconds(addressInformation.DhcpLeaseLifetime);
                    result += $"    DHCP lease lifetime:               {when.ToString(dateTimeFormat, System.Globalization.CultureInfo.CurrentCulture)}\n";
                    result += $"    Duplicate address detection:       {addressInformation.DuplicateAddressDetectionState}\n";
                    result += $"    Prefix origin:                     {addressInformation.PrefixOrigin}\n";
                    result += $"    Suffix origin:                     {addressInformation.SuffixOrigin}\n";
                }
            }

            return result;
        }

        private static string FormatUnicastIPAddressInformationCollection(UnicastIPAddressInformationCollection collection)
        {
            string result = string.Empty;
            if (collection != null)
            {
                string dateTimeFormat = "yyyy.MM.dd HH:mm:ss";
                DateTime when;
                foreach (UnicastIPAddressInformation addressInformation in collection)
                {
                    result += $"  Unicast address:                     {addressInformation.Address.ToString()}\n";
                    result += $"    IPv4 mask:                         {addressInformation.IPv4Mask}\n";
                    try
                    {
                        when = DateTime.UtcNow + TimeSpan.FromSeconds(addressInformation.AddressPreferredLifetime);
                        result += $"    Preferred lifetime:                {when.ToString(dateTimeFormat, System.Globalization.CultureInfo.CurrentCulture)}\n";
                        when = DateTime.UtcNow + TimeSpan.FromSeconds(addressInformation.AddressValidLifetime);
                        result += $"    Valid lifetime:                    {when.ToString(dateTimeFormat, System.Globalization.CultureInfo.CurrentCulture)}\n";
                        when = DateTime.UtcNow + TimeSpan.FromSeconds(addressInformation.DhcpLeaseLifetime);
                        result += $"    DHCP lease lifetime:               {when.ToString(dateTimeFormat, System.Globalization.CultureInfo.CurrentCulture)}\n";
                        result += $"    Duplicate address detection:       {addressInformation.DuplicateAddressDetectionState}\n";
                        result += $"    DNS eligible:                      {addressInformation.IsDnsEligible}\n";
                        result += $"    Transient:                         {addressInformation.IsTransient}\n";
                        result += $"    Prefix length:                     {addressInformation.PrefixLength}\n";
                        result += $"    Prefix origin:                     {addressInformation.PrefixOrigin}\n";
                        result += $"    Suffix origin:                     {addressInformation.SuffixOrigin}\n";
                    }
                    catch (PlatformNotSupportedException)
                    {
                    }
                }
            }

            return result;
        }

        private static string FormatIPv4InterfaceProperties(IPv4InterfaceProperties ipv4Properties)
        {
            string result = string.Empty;
            if (ipv4Properties != null)
            {
                result += $"  IPv4 properties:\n";
                result += $"    Index:                             {ipv4Properties.Index}\n";
                result += $"    MTU:                               {ipv4Properties.Mtu}\n";
                result += $"    Uses WINS:                         {ipv4Properties.UsesWins}\n";
                result += $"    Forwarding enabled:                {ipv4Properties.IsForwardingEnabled}\n";
                try
                {
                    result += $"    DHCP enabled:                      {ipv4Properties.IsDhcpEnabled}\n";
                    result += $"    APIPA active:                      {ipv4Properties.IsAutomaticPrivateAddressingActive}\n";
                    result += $"    APIPA enabled:                     {ipv4Properties.IsAutomaticPrivateAddressingEnabled}\n";
                }
                catch (PlatformNotSupportedException)
                {
                }
            }

            return result;
        }

        private static string FormatIPv6InterfaceProperties(IPv6InterfaceProperties ipv6Properties)
        {
            string result = string.Empty;
            if (ipv6Properties != null)
            {
                result += $"  IPv6 properties:\n";
                result += $"    Index:                             {ipv6Properties.Index}\n";
                result += $"    MTU:                               {ipv6Properties.Mtu}\n";
                try
                {
                    result += $"    Scope ID:                          {ipv6Properties.GetScopeId(ScopeLevel.None)}\n";
                }
                catch (PlatformNotSupportedException)
                {
                }
            }

            return result;
        }

        private static string FormatIPInterfaceProperties(IPInterfaceProperties adapterProperties)
        {
            string result = string.Empty;
            try
            {
                result += FormatIPAddressInformationCollection(adapterProperties.AnycastAddresses, "  Anycast address:                     {0} (Transient: {1}; DNS eligible: {2})\n");
            }
            catch (PlatformNotSupportedException)
            {
            }

            result += FormatIPAddressCollection(adapterProperties.DhcpServerAddresses, "  DHCP server:                         {0}\n");
            result += FormatIPAddressCollection(adapterProperties.DnsAddresses, "  DNS server:                          {0}\n");
            result += $"  DNS suffix:                          {adapterProperties.DnsSuffix}\n";
            result += FormatGatewayIPAddressInformationCollection(adapterProperties.GatewayAddresses);
            result += $"  DNS enabled:                         {adapterProperties.IsDnsEnabled}\n";
            result += $"  Dynamic DNS enabled:                 {adapterProperties.IsDnsEnabled}\n";
            result += FormatMulticastIPAddressInformationCollection(adapterProperties.MulticastAddresses);
            result += FormatUnicastIPAddressInformationCollection(adapterProperties.UnicastAddresses);
            result += FormatIPAddressCollection(adapterProperties.WinsServersAddresses, "  WINS server:                         {0}\n");

            return result;
        }

        private static string FormatIPInterfaceStatistics(IPInterfaceStatistics statistics)
        {
            string result = string.Empty;
            result += "  Statistics:\n";
            result += $"    Bytes received:                    {statistics.BytesReceived}\n";
            result += $"    Bytes sent:                        {statistics.BytesSent}\n";
            result += $"    Incoming packets discarded:        {statistics.IncomingPacketsDiscarded}\n";
            result += $"    Incoming packets with errors:      {statistics.IncomingPacketsWithErrors}\n";
            result += $"    Non-unicast packets received:      {statistics.NonUnicastPacketsReceived}\n";
            result += $"    Outgoing packets discarded:        {statistics.OutgoingPacketsDiscarded}\n";
            result += $"    Outgoing packets with errors:      {statistics.OutgoingPacketsWithErrors}\n";
            result += $"    Output queue length:               {statistics.OutputQueueLength}\n";
            result += $"    Unicast packets received:          {statistics.UnicastPacketsReceived}\n";
            result += $"    Unicast packets sent:              {statistics.UnicastPacketsSent}\n";
            try
            {
                result += $"    Incoming unknown protocol packets: {statistics.IncomingUnknownProtocolPackets}\n";
                result += $"    Non-unicast packets sent:          {statistics.NonUnicastPacketsSent}\n";
            }
            catch (PlatformNotSupportedException)
            {
            }

            return result;
        }

        private static string FormatIPv4InterfaceStatistics(IPv4InterfaceStatistics statistics)
        {
            string result = string.Empty;
            result += "  IPv4 Statistics:\n";
            result += $"    Bytes received:                    {statistics.BytesReceived}\n";
            result += $"    Bytes sent:                        {statistics.BytesSent}\n";
            result += $"    Incoming packets discarded:        {statistics.IncomingPacketsDiscarded}\n";
            result += $"    Incoming packets with errors:      {statistics.IncomingPacketsWithErrors}\n";
            result += $"    Non-unicast packets received:      {statistics.NonUnicastPacketsReceived}\n";
            result += $"    Outgoing packets discarded:        {statistics.OutgoingPacketsDiscarded}\n";
            result += $"    Outgoing packets with errors:      {statistics.OutgoingPacketsWithErrors}\n";
            result += $"    Output queue length:               {statistics.OutputQueueLength}\n";
            result += $"    Unicast packets received:          {statistics.UnicastPacketsReceived}\n";
            result += $"    Unicast packets sent:              {statistics.UnicastPacketsSent}\n";
            try
            {
                result += $"    Incoming unknown protocol packets: {statistics.IncomingUnknownProtocolPackets}\n";
                result += $"    Non-unicast packets sent:          {statistics.NonUnicastPacketsSent}\n";
            }
            catch (PlatformNotSupportedException)
            {
            }

            return result;
        }

        private static string FormatNetworkInterface(NetworkInterface adapter)
        {
            string result = string.Empty;
            result += $"Interface:                             {adapter.Name}\n";
            result += $"  Description:                         {adapter.Description}\n";
            result += $"  ID:                                  {adapter.Id}\n";
            result += $"  Type:                                {adapter.NetworkInterfaceType}\n";
            result += $"  Operational status:                  {adapter.OperationalStatus}\n";
            result += $"  Supports multicast:                  {adapter.SupportsMulticast}\n";
            result += $"  Physical address:                    {adapter.GetPhysicalAddress().ToString()}\n";
            result += $"  Supports IPv4:                       {adapter.Supports(NetworkInterfaceComponent.IPv4)}\n";
            result += $"  Supports IPv6:                       {adapter.Supports(NetworkInterfaceComponent.IPv6)}\n";
            try
            {
                result += $"  Receive only:                        {adapter.IsReceiveOnly}\n";
                result += $"  Speed:                               {adapter.Speed}\n";
            }
            catch (PlatformNotSupportedException)
            {
            }

            if (adapter.NetworkInterfaceType != NetworkInterfaceType.Loopback)
            {
                IPInterfaceProperties properties = adapter.GetIPProperties();
                result += FormatIPInterfaceProperties(properties);
                result += FormatIPInterfaceStatistics(adapter.GetIPStatistics());
                if (adapter.Supports(NetworkInterfaceComponent.IPv4))
                {
                    result += FormatIPv4InterfaceProperties(properties.GetIPv4Properties());
                    result += FormatIPv4InterfaceStatistics(adapter.GetIPv4Statistics());
                }

                if (adapter.Supports(NetworkInterfaceComponent.IPv6))
                {
                    result += FormatIPv6InterfaceProperties(properties.GetIPv6Properties());
                }
            }

            return result;
        }

        private static string FormatInterfaces()
        {
            string result = string.Empty;
            result += FormatIPGlobalProperties();
            NetworkInterface[] nics = NetworkInterface.GetAllNetworkInterfaces();
            if (nics == null || nics.Length < 1)
            {
                result += "  No network interfaces found\n";
            }
            else
            {
                result += $"Number of interfaces:                  {nics.Length}\n";
                foreach (NetworkInterface adapter in nics)
                {
                    result += FormatNetworkInterface(adapter);
                }
            }

            return result;
        }

        private static bool Useful(NetworkInterface adapter)
        {
            if (adapter.NetworkInterfaceType == NetworkInterfaceType.Loopback)
            {
                return false;
            }

            if (adapter.OperationalStatus != OperationalStatus.Up)
            {
                return false;
            }

            if (!adapter.Supports(NetworkInterfaceComponent.IPv4))
            {
                return false;
            }

            return true;
        }

        private static List<IPAddress> EnumerateBroadcastAddresses()
        {
            List<IPAddress> broadcastAddresses = new List<IPAddress>();
            NetworkInterface[] nics = NetworkInterface.GetAllNetworkInterfaces();
            if (nics != null && nics.Length > 0)
            {
                foreach (NetworkInterface adapter in nics)
                {
                    if (!Useful(adapter))
                    {
                        continue;
                    }

                    IPInterfaceProperties properties = adapter.GetIPProperties();
                    foreach (UnicastIPAddressInformation addressInformation in properties.UnicastAddresses)
                    {
                        IPAddress address = addressInformation.Address;
                        if (address.AddressFamily == AddressFamily.InterNetwork)
                        {
                            uint ip = BitConverter.ToUInt32(addressInformation.Address.GetAddressBytes(), 0);
                            uint mask = BitConverter.ToUInt32(addressInformation.IPv4Mask.GetAddressBytes(), 0);
                            uint broadcast = ip | ~mask;
                            IPAddress broadcastAddress = new IPAddress(BitConverter.GetBytes(broadcast));
                            broadcastAddresses.Add(broadcastAddress);
                        }
                    }
                }

                if (broadcastAddresses.Count != 0)
                {
                    return broadcastAddresses;
                }
            }

            broadcastAddresses.Add(IPAddress.Broadcast);

            return broadcastAddresses;
        }

        private static IPAddress MatchingOwnAddress(IPAddress address)
        {
            uint ip = BitConverter.ToUInt32(address.GetAddressBytes(), 0);
            NetworkInterface[] nics = NetworkInterface.GetAllNetworkInterfaces();
            if (nics != null && nics.Length > 0)
            {
                foreach (NetworkInterface adapter in nics)
                {
                    if (!Useful(adapter))
                    {
                        continue;
                    }

                    IPInterfaceProperties properties = adapter.GetIPProperties();
                    foreach (UnicastIPAddressInformation addressInformation in properties.UnicastAddresses)
                    {
                        IPAddress ownAddress = addressInformation.Address;
                        if (ownAddress.AddressFamily == AddressFamily.InterNetwork)
                        {
                            uint ipOwn = BitConverter.ToUInt32(addressInformation.Address.GetAddressBytes(), 0);
                            uint maskOwn = BitConverter.ToUInt32(addressInformation.IPv4Mask.GetAddressBytes(), 0);
                            uint subnetOwn = ipOwn & maskOwn;
                            uint subnet = ip & maskOwn;
                            if (subnet == subnetOwn)
                            {
                                return ownAddress;
                            }
                        }
                    }
                }
            }

            return null;
        }
    }
}
