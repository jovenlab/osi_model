import struct
import time
import uuid

class SessionLayer:
    """Simulates the session layer with connection management."""
    
    def __init__(self):
        """Initialize session management."""
        self.session_id = str(uuid.uuid4())
        self.established = False
        self.sequence = 0
        self.last_activity = time.time()
        
        print(f"[Session] Initialized with session ID: {self.session_id}")
        
    def create_session_data(self, data, session_type=0):
        """Wrap data in session layer information.
        
        Session types:
        0 = Data
        1 = Session establish request
        2 = Session establish response
        3 = Session close
        """
        if session_type == 1:
            # Session establishment
            print("[Session] Requesting session establishment")
            self.sequence = 0
            
        elif session_type == 2:
            # Session establishment response
            print("[Session] Responding to session establishment")
            self.established = True
            
        elif session_type == 3:
            # Session close
            print("[Session] Closing session")
            self.established = False
            
        else:
            # Normal data
            if not self.established:
                print("[Session] Warning: Sending data without established session")
            self.sequence += 1
            
        # Update last activity time
        self.last_activity = time.time()
        
        # Create session header
        # Format: Session ID (36 bytes), Session Type (1 byte), Sequence (4 bytes), Timestamp (8 bytes)
        header = self.session_id.encode('utf-8')
        header += struct.pack('!BI', session_type, self.sequence)
        header += struct.pack('!d', self.last_activity)
        
        # Complete session data
        session_data = header + data
        
        print(f"[Session] Created session data: {len(session_data)} bytes (type: {session_type}, seq: {self.sequence})")
        return session_data
        
    def process_session_data(self, session_data):
        """Process session layer data and manage session state."""
        if len(session_data) < 49:  # Minimum session header size
            print("[Session] Invalid session data: too small")
            return None
            
        # Extract session information
        session_id = session_data[:36].decode('utf-8')
        session_type, sequence = struct.unpack('!BI', session_data[36:41])
        timestamp = struct.unpack('!d', session_data[41:49])[0]
        
        # Extract actual data
        data = session_data[49:]
        
        # Process based on session type
        if session_type == 1:
            # Session establishment request
            print(f"[Session] Received session establishment request: {session_id}")
            # In a real implementation, we might validate the session or negotiate parameters
            self.session_id = session_id  # Accept the proposed session ID
            self.established = True
            
        elif session_type == 2:
            # Session establishment response
            print(f"[Session] Session established: {session_id}")
            self.session_id = session_id
            self.established = True
            
        elif session_type == 3:
            # Session close
            print(f"[Session] Session closed: {session_id}")
            self.established = False
            
        else:
            # Normal data
            if not self.established:
                print("[Session] Warning: Received data without established session")
            
            # Check for sequence continuity
            if self.sequence + 1 != sequence and self.sequence != 0:
                print(f"[Session] Sequence mismatch. Expected {self.sequence + 1}, got {sequence}")
            
            self.sequence = sequence
            
        # Update last activity time
        self.last_activity = time.time()
        
        print(f"[Session] Processed session data (type: {session_type}, seq: {sequence})")
        return data
