import socket
import struct
import random
import time

class PhysicalLayer:
    """Simulates the physical transmission of bits over a medium."""
    
    def __init__(self, is_server=False, host='127.0.0.1', port=8000):
        self.is_server = is_server
        self.host = host
        self.port = port
        self.socket = None
        self.connection = None
        self.client_address = None
    
    def initialize(self):
        """Initialize the socket connection based on server/client role."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.is_server:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            print(f"[Physical] Server listening on {self.host}:{self.port}")
            self.connection, self.client_address = self.socket.accept()
            print(f"[Physical] Connection established with {self.client_address}")
        else:
            print(f"[Physical] Client connecting to {self.host}:{self.port}")
            self.socket.connect((self.host, self.port))
            self.connection = self.socket
            
    def send_bits(self, data):
        """Simulate sending bits over the wire."""
        # Convert data to a binary format for transmission
        size = len(data)
        # Send the size of the data first
        self.connection.sendall(struct.pack('!I', size))
        # Send the actual data
        self.connection.sendall(data)
        
        print(f"[Physical] Transmitted {size} bytes")
        # Simulate physical delay
        time.sleep(0.01)
        return True
        
    def receive_bits(self):
        """Simulate receiving bits from the wire."""
        # First receive the size of incoming data
        size_data = self.connection.recv(4)
        if not size_data:
            return None
        
        size = struct.unpack('!I', size_data)[0]
        
        # Now receive the actual data
        chunks = []
        bytes_received = 0
        while bytes_received < size:
            chunk = self.connection.recv(min(size - bytes_received, 4096))
            if not chunk:
                raise RuntimeError("Socket connection broken")
            chunks.append(chunk)
            bytes_received += len(chunk)
        
        data = b''.join(chunks)
        print(f"[Physical] Received {len(data)} bytes")
        return data
        
    def close(self):
        """Close the connection."""
        if self.connection:
            self.connection.close()
        if self.socket:
            self.socket.close()
        print("[Physical] Connection closed")
