import json
import zlib
import base64

class PresentationLayer:
    """Simulates the presentation layer with data format conversion."""
    
    def __init__(self):
        """Initialize with default formats and options."""
        self.encoding = 'utf-8'
        self.compression = True
        self.encryption = False  # Simplified for this implementation
        
        print(f"[Presentation] Initialized (encoding: {self.encoding}, compression: {self.compression})")
        
    def prepare_data(self, data):
        """Convert data from application format to binary format for lower layers."""
        # 1. Convert Python object to JSON string if it's not already binary
        if not isinstance(data, bytes):
            try:
                data = json.dumps(data).encode(self.encoding)
                print(f"[Presentation] Converted object to JSON: {len(data)} bytes")
            except (TypeError, ValueError):
                if isinstance(data, str):
                    data = data.encode(self.encoding)
                    print(f"[Presentation] Encoded string: {len(data)} bytes")
                else:
                    print(f"[Presentation] Warning: Could not convert data of type {type(data)}")
                    return None
        
        # 2. Apply compression if enabled
        if self.compression:
            data = zlib.compress(data)
            print(f"[Presentation] Compressed data: {len(data)} bytes")
        
        # 3. Apply encryption if enabled (simplified for this implementation)
        if self.encryption:
            # XOR with a fixed key (not secure, just for demonstration)
            key = b'secretkey'
            encrypted = bytearray(data)
            for i in range(len(encrypted)):
                encrypted[i] ^= key[i % len(key)]
            data = bytes(encrypted)
            print(f"[Presentation] Applied simple encryption: {len(data)} bytes")
            
        # 4. Add a simple header to indicate processing options
        options = ((1 if self.compression else 0) << 1) | (1 if self.encryption else 0)
        header = struct.pack('!B', options)
        
        # Complete prepared data
        prepared_data = header + data
        
        print(f"[Presentation] Prepared data: {len(prepared_data)} bytes")
        return prepared_data
        
    def process_data(self, prepared_data):
        """Convert data from binary format to application format."""
        if len(prepared_data) < 1:
            print("[Presentation] Invalid data: too small")
            return None
            
        # 1. Extract header and processing options
        options = prepared_data[0]
        received_compression = bool((options >> 1) & 1)
        received_encryption = bool(options & 1)
        
        # Get actual data
        data = prepared_data[1:]
        
        # 2. Decrypt if needed
        if received_encryption:
            # XOR with a fixed key (not secure, just for demonstration)
            key = b'secretkey'
            decrypted = bytearray(data)
            for i in range(len(decrypted)):
                decrypted[i] ^= key[i % len(key)]
            data = bytes(decrypted)
            print(f"[Presentation] Decrypted data: {len(data)} bytes")
            
        # 3. Decompress if needed
        if received_compression:
            try:
                data = zlib.decompress(data)
                print(f"[Presentation] Decompressed data: {len(data)} bytes")
            except zlib.error:
                print("[Presentation] Decompression failed")
                return None
                
        # 4. Convert from JSON to Python object if possible
        try:
            # First decode bytes to string
            text = data.decode(self.encoding)
            # Then try to parse as JSON
            result = json.loads(text)
            print(f"[Presentation] Parsed JSON to object")
            return result
        except (UnicodeDecodeError, json.JSONDecodeError):
            # If not valid JSON or encoding, return the binary data
            print(f"[Presentation] Returning raw binary data: {len(data)} bytes")
            return data
