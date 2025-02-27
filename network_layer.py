import struct
import random

class NetworkLayer:
    """Simulates the network layer with IP addressing and routing."""
    
    def __init__(self, ip_address=None):
        """Initialize with an IP address or generate a random one in private range."""
        if ip_address is None:
            # Generate a random IP in 192.168.0.0/16 range
            self.ip_address = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
        else:
            self.ip_address = ip_address
        
        # Initialize TTL for packets
        self.default_ttl = 64
        
        print(f"[Network] Initialized with IP: {self.ip_address}")
        
    def create_packet(self, data, dest_ip, protocol=6):  # Default protocol 6 = TCP
        """Create an IP packet."""
        # Convert IP addresses to 4-byte binary values
        src_ip_bin = self._ip_to_binary(self.ip_address)
        dest_ip_bin = self._ip_to_binary(dest_ip)
        
        # Calculate packet length (header + data)
        packet_length = 20 + len(data)  # 20 bytes for IPv4 header
        
        # Create IP header
        # Format: Version and IHL (1 byte), Type of Service (1 byte),
        # Total Length (2 bytes), Identification (2 bytes), 
        # Flags and Fragment Offset (2 bytes), TTL (1 byte),
        # Protocol (1 byte), Header Checksum (2 bytes),
        # Source IP (4 bytes), Destination IP (4 bytes)
        version_ihl = (4 << 4) | 5  # IPv4, header length 5 32-bit words
        identification = random.randint(0, 65535)
        flags_fragment = 0  # No flags, no fragmentation
        header_checksum = 0  # Simplified implementation
        
        header = struct.pack('!BBHHHBBH', 
                            version_ihl, 0, packet_length,
                            identification, flags_fragment, 
                            self.default_ttl, protocol, header_checksum)
        header += src_ip_bin + dest_ip_bin
        
        # Calculate header checksum (simplified)
        checksum = self._calculate_checksum(header)
        
        # Update header with checksum
        header = struct.pack('!BBHHHBBH', 
                            version_ihl, 0, packet_length,
                            identification, flags_fragment, 
                            self.default_ttl, protocol, checksum)
        header += src_ip_bin + dest_ip_bin
        
        # Complete packet
        packet = header + data
        
        print(f"[Network] Created packet: {packet_length} bytes (src: {self.ip_address}, dest: {dest_ip})")
        return packet
        
    def process_packet(self, packet):
        """Process a received packet, validate and extract data."""
        if len(packet) < 20:  # Minimum IPv4 header size
            print("[Network] Invalid packet: too small")
            return None
            
        # Extract header information
        version_ihl = packet[0]
        protocol = packet[9]
        received_checksum = struct.unpack('!H', packet[10:12])[0]
        src_ip_bin = packet[12:16]
        dest_ip_bin = packet[16:20]
        
        # Extract source and destination IPs
        src_ip = self._binary_to_ip(src_ip_bin)
        dest_ip = self._binary_to_ip(dest_ip_bin)
        
        # Verify this packet is for us
        if dest_ip != self.ip_address and dest_ip != "255.255.255.255":
            print(f"[Network] Packet not for us. Dest: {dest_ip}")
            return None
            
        # Calculate and verify checksum
        # In a real implementation, we would verify the checksum here
        
        # Extract the header length to find where data begins
        ihl = version_ihl & 0x0F
        header_length = ihl * 4
        
        # Extract data
        data = packet[header_length:]
        
        print(f"[Network] Processed packet from {src_ip}, protocol: {protocol}")
        return data
        
    def _ip_to_binary(self, ip_str):
        """Convert an IP address string to 4-byte binary value."""
        octets = ip_str.split('.')
        return bytes([int(octet) for octet in octets])
        
    def _binary_to_ip(self, ip_bin):
        """Convert 4-byte binary IP to string format."""
        return '.'.join([str(b) for b in ip_bin])
        
    def _calculate_checksum(self, header):
        """Calculate IP header checksum."""
        # This is a simplified implementation
        if len(header) % 2 == 1:
            header += b'\0'
        words = struct.unpack('!' + 'H' * (len(header) // 2), header)
        checksum = sum(words) & 0xFFFF
        return checksum ^ 0xFFFF  # One's complement
