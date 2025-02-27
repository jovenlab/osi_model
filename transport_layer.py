import struct
import random
import time

class TransportLayer:
    """Simulates the transport layer with TCP-like functionality."""
    
    def __init__(self):
        """Initialize transport layer with port handling and sequence tracking."""
        # For simplicity, we'll use fixed ports
        self.src_port = random.randint(49152, 65535)  # Ephemeral port
        self.sequence_num = random.randint(0, 4294967295)  # Initial sequence number
        self.received_segments = {}  # Buffer for out-of-order segments
        
        print(f"[Transport] Initialized with source port: {self.src_port}")
        
    def create_segment(self, data, dest_port, flags=0):
        """Create a transport layer segment (TCP-like)."""
        # Increment sequence number
        self.sequence_num = (self.sequence_num + 1) % 4294967296
        
        # TCP header fields
        acknowledgment_num = 0
        data_offset = 5 << 4  # 5 32-bit words (20 bytes)
        window_size = 65535
        urgent_pointer = 0
        
        # Create TCP header
        # Format: Source Port (2 bytes), Destination Port (2 bytes),
        # Sequence Number (4 bytes), Acknowledgment Number (4 bytes),
        # Data Offset & Flags (2 bytes), Window Size (2 bytes),
        # Checksum (2 bytes), Urgent Pointer (2 bytes)
        header = struct.pack('!HHIIBBHHH', 
                            self.src_port, dest_port,
                            self.sequence_num, acknowledgment_num,
                            data_offset, flags, window_size,
                            0, urgent_pointer)  # Checksum initially 0
        
        # Calculate checksum (simplified)
        checksum = self._calculate_checksum(header + data)
        
        # Update header with checksum
        header = struct.pack('!HHIIBBHHH', 
                            self.src_port, dest_port,
                            self.sequence_num, acknowledgment_num,
                            data_offset, flags, window_size,
                            checksum, urgent_pointer)
        
        # Complete segment
        segment = header + data
        
        print(f"[Transport] Created segment: {len(segment)} bytes (src port: {self.src_port}, dest port: {dest_port}, seq: {self.sequence_num})")
        return segment
        
    def process_segment(self, segment):
        """Process a received segment, validate and extract data."""
        if len(segment) < 20:  # Minimum TCP header size
            print("[Transport] Invalid segment: too small")
            return None
            
        # Extract header information
        src_port, dest_port, seq_num, ack_num, data_offset_flags, window = struct.unpack('!HHIIBBH', segment[:14])
        data_offset = (data_offset_flags >> 4) * 4
        flags = data_offset_flags & 0x3F
        
        # Verify this segment is for our port
        # In a real implementation, we would check against open/bound ports
        
        # Calculate and verify checksum
        # In a real implementation, we would verify the checksum here
        
        # Extract data
        data = segment[data_offset:]
        
        # In a real implementation, we would handle sequence numbers,
        # acknowledgments, and window sizes properly
        
        print(f"[Transport] Processed segment from port {src_port}, sequence: {seq_num}")
        return data
        
    def _calculate_checksum(self, data):
        """Calculate transport layer checksum."""
        # This is a simplified implementation
        if len(data) % 2 == 1:
            data += b'\0'
        words = struct.unpack('!' + 'H' * (len(data) // 2), data)
        checksum = sum(words) & 0xFFFF
        return checksum ^ 0xFFFF  # One's complement
