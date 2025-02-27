import struct
import random

class DataLinkLayer:
    """Simulates the data link layer with MAC addressing and frame handling."""
    
    def __init__(self, mac_address=None):
        """Initialize with a MAC address or generate a random one."""
        if mac_address is None:
            # Generate a random MAC address if none is provided
            self.mac_address = ':'.join([f'{random.randint(0, 255):02x}' for _ in range(6)])
        else:
            self.mac_address = mac_address
        print(f"[Data Link] Initialized with MAC: {self.mac_address}")
        
        # For simplicity, we'll use a predefined broadcast MAC
        self.broadcast_mac = 'ff:ff:ff:ff:ff:ff'
        
    def create_frame(self, data, dest_mac):
        """Create a frame with header and data."""
        # Convert MAC addresses to binary
        src_mac_bin = self._mac_to_binary(self.mac_address)
        dest_mac_bin = self._mac_to_binary(dest_mac)
        
        # Create a simple frame structure:
        # [Dest MAC (6 bytes)][Source MAC (6 bytes)][Frame Type (2 bytes)][Data][CRC (4 bytes)]
        frame_type = struct.pack('!H', 0x0800)  # IPv4 EtherType
        
        # Combine all parts except CRC
        frame_without_crc = dest_mac_bin + src_mac_bin + frame_type + data
        
        # Calculate CRC (simplified in this implementation)
        crc = self._calculate_crc(frame_without_crc)
        
        # Complete frame
        frame = frame_without_crc + crc
        
        print(f"[Data Link] Created frame: {len(frame)} bytes (src: {self.mac_address}, dest: {dest_mac})")
        return frame
        
    def process_frame(self, frame):
        """Process a received frame, validate and extract data."""
        if len(frame) < 18:  # Minimum frame size (headers + crc)
            print("[Data Link] Invalid frame: too small")
            return None
            
        # Extract parts of the frame
        dest_mac_bin = frame[:6]
        src_mac_bin = frame[6:12]
        frame_type = struct.unpack('!H', frame[12:14])[0]
        data = frame[14:-4]
        received_crc = frame[-4:]
        
        # Convert binary MACs to string format
        dest_mac = self._binary_to_mac(dest_mac_bin)
        src_mac = self._binary_to_mac(src_mac_bin)
        
        # Check if the frame is addressed to us or is a broadcast
        if dest_mac != self.mac_address and dest_mac != self.broadcast_mac:
            print(f"[Data Link] Frame not for us. Dest: {dest_mac}")
            return None
            
        # Verify CRC
        calculated_crc = self._calculate_crc(frame[:-4])
        if calculated_crc != received_crc:
            print("[Data Link] CRC check failed")
            return None
            
        print(f"[Data Link] Processed frame from {src_mac}, type: 0x{frame_type:04x}")
        return data
        
    def _mac_to_binary(self, mac_str):
        """Convert a MAC address string to binary representation."""
        return bytes.fromhex(mac_str.replace(':', ''))
        
    def _binary_to_mac(self, mac_bin):
        """Convert binary MAC to string format."""
        return ':'.join([f'{b:02x}' for b in mac_bin])
        
    def _calculate_crc(self, data):
        """Calculate a simple CRC-32 for the data."""
        # Using a simplified CRC calculation for demonstration
        crc = 0
        for byte in data:
            crc = (crc + byte) & 0xFFFFFFFF
        return struct.pack('!I', crc)
