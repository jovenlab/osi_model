import time
import struct
import pickle
import json
import random
import sys
import threading

from physical_layer import PhysicalLayer
from data_link_layer import DataLinkLayer
from network_layer import NetworkLayer
from transport_layer import TransportLayer
from session_layer import SessionLayer
from presentation_layer import PresentationLayer
from application_layer import ApplicationLayer

class OSIServer:
    """Implements a server using the OSI model layers."""
    
    def __init__(self, host='127.0.0.1', port=8000):
        """Initialize all OSI layers."""
        # Create all layers
        self.physical = PhysicalLayer(is_server=True, host=host, port=port)
        self.data_link = DataLinkLayer(mac_address="aa:bb:cc:dd:ee:ff")
        self.network = NetworkLayer(ip_address="192.168.1.1")
        self.transport = TransportLayer()
        self.session = SessionLayer()
        self.presentation = PresentationLayer()
        self.application = ApplicationLayer()
        
        # Server is running flag
        self.running = False
        
    def start(self):
        """Start the server and listen for incoming connections."""
        print("Starting OSI Model Server...")
        
        try:
            # Initialize physical layer
            self.physical.initialize()
            
            # Set server as running
            self.running = True
            
            # Handle communication in a loop
            while self.running:
                # Receive data up through the OSI stack
                received_data = self.receive_all()
                
                if received_data:
                    print("\n[Server] Received application data")
                    
                    # Process the application data
                    if isinstance(received_data, dict) and received_data.get('type') == 'request':
                        # Create a response
                        response = self.application.create_response(
                            200, "OK", 
                            body={"message": "Hello from server", "received": received_data.get('body')}
                        )
                        
                        # Send the response
                        print("\n[Server] Sending response")
                        self.send_all(response)
                    
                time.sleep(0.1)  # Prevent tight loop
                
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop()
            
    def stop(self):
        """Stop the server."""
        self.running = False
        self.physical.close()
        print("Server stopped")
        
    def send_all(self, data):
        """Send data down through all OSI layers."""
        # Layer 7: Application - Already handled
        print(f"[Server] Application data: {type(data)}")
        
        # Layer 6: Presentation - Convert to transmittable format
        presentation_data = self.presentation.prepare_data(data)
        
        # Layer 5: Session - Manage communication session
        session_data = self.session.create_session_data(presentation_data)
        
        # Layer 4: Transport - Create segment with port information
        segment = self.transport.create_segment(session_data, 8080)
        
        # Layer 3: Network - Create packet with IP addressing
        packet = self.network.create_packet(segment, "192.168.1.2")
        
        # Layer 2: Data Link - Create frame with MAC addressing
        frame = self.data_link.create_frame(packet, "bb:aa:cc:11:22:33")
        
        # Layer 1: Physical - Transmit bits
        success = self.physical.send_bits(frame)
        
        return success
        
    def receive_all(self):
        """Receive data up through all OSI layers."""
        # Layer 1: Physical - Receive bits
        frame = self.physical.receive_bits()
        if frame is None:
            return None
            
        # Layer 2: Data Link - Extract packet from frame
        packet = self.data_link.process_frame(frame)
        if packet is None:
            return None
            
        # Layer 3: Network - Extract segment from packet
        segment = self.network.process_packet(packet)
        if segment is None:
            return None
            
        # Layer 4: Transport - Extract session data from segment
        session_data = self.transport.process_segment(segment)
        if session_data is None:
            return None
            
        # Layer 5: Session - Extract presentation data and manage session
        presentation_data = self.session.process_session_data(session_data)
        if presentation_data is None:
            return None

# Layer 6: Presentation - Convert to application format
        application_data = self.presentation.process_data(presentation_data)
        if application_data is None:
            return None
            
        # Layer 7: Application - Process message
        result = self.application.process_message(application_data)
        
        return result

# main.py - Client implementation
class OSIClient:
    """Implements a client using the OSI model layers."""
    
    def __init__(self, host='127.0.0.1', port=8000):
        """Initialize all OSI layers."""
        # Create all layers
        self.physical = PhysicalLayer(is_server=False, host=host, port=port)
        self.data_link = DataLinkLayer(mac_address="bb:aa:cc:11:22:33")
        self.network = NetworkLayer(ip_address="192.168.1.2")
        self.transport = TransportLayer()
        self.session = SessionLayer()
        self.presentation = PresentationLayer()
        self.application = ApplicationLayer()
        
        # Client is running flag
        self.running = False
        
    def start(self):
        """Start the client and connect to the server."""
        print("Starting OSI Model Client...")
        
        try:
            # Initialize physical layer
            self.physical.initialize()
            
            # Set client as running
            self.running = True
            
            # Establish session
            self.establish_session()
            
            # Send a request to the server
            request = self.application.create_request(
                "GET", "/resource",
                body={"message": "Hello from client"}
            )
            
            print("\n[Client] Sending request")
            self.send_all(request)
            
            # Wait for response
            print("\n[Client] Waiting for response")
            response = self.receive_all()
            
            if response:
                print(f"\n[Client] Received response: {response.get('status')} {response.get('status_message')}")
                print(f"[Client] Response body: {response.get('body')}")
            
            # Close session
            self.close_session()
            
        except KeyboardInterrupt:
            print("\nClient shutting down...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop()
            
    def stop(self):
        """Stop the client."""
        self.running = False
        self.physical.close()
        print("Client stopped")
    
    def establish_session(self):
        """Establish a session with the server."""
        print("\n[Client] Establishing session")
        
        # Create a session establishment request
        session_req = self.session.create_session_data(b'', 1)  # Type 1 = Session establish
        
        # Transport layer
        segment = self.transport.create_segment(session_req, 8080)
        
        # Network layer
        packet = self.network.create_packet(segment, "192.168.1.1")
        
        # Data Link layer
        frame = self.data_link.create_frame(packet, "aa:bb:cc:dd:ee:ff")
        
        # Physical layer
        self.physical.send_bits(frame)
        
        # Wait for response
        resp_frame = self.physical.receive_bits()
        if resp_frame:
            resp_packet = self.data_link.process_frame(resp_frame)
            if resp_packet:
                resp_segment = self.network.process_packet(resp_packet)
                if resp_segment:
                    resp_session = self.transport.process_segment(resp_segment)
                    if resp_session:
                        self.session.process_session_data(resp_session)
        
        print("[Client] Session established")
    
    def close_session(self):
        """Close the session with the server."""
        print("\n[Client] Closing session")
        
        # Create a session close request
        session_close = self.session.create_session_data(b'', 3)  # Type 3 = Session close
        
        # Transport layer
        segment = self.transport.create_segment(session_close, 8080)
        
        # Network layer
        packet = self.network.create_packet(segment, "192.168.1.1")
        
        # Data Link layer
        frame = self.data_link.create_frame(packet, "aa:bb:cc:dd:ee:ff")
        
        # Physical layer
        self.physical.send_bits(frame)
        
        print("[Client] Session closed")
        
    def send_all(self, data):
        """Send data down through all OSI layers."""
        # Layer 7: Application - Already handled
        print(f"[Client] Application data: {type(data)}")
        
        # Layer 6: Presentation - Convert to transmittable format
        presentation_data = self.presentation.prepare_data(data)
        
        # Layer 5: Session - Manage communication session
        session_data = self.session.create_session_data(presentation_data)
        
        # Layer 4: Transport - Create segment with port information
        segment = self.transport.create_segment(session_data, 8080)
        
        # Layer 3: Network - Create packet with IP addressing
        packet = self.network.create_packet(segment, "192.168.1.1")
        
        # Layer 2: Data Link - Create frame with MAC addressing
        frame = self.data_link.create_frame(packet, "aa:bb:cc:dd:ee:ff")
        
        # Layer 1: Physical - Transmit bits
        success = self.physical.send_bits(frame)
        
        return success
        
    def receive_all(self):
        """Receive data up through all OSI layers."""
        # Layer 1: Physical - Receive bits
        frame = self.physical.receive_bits()
        if frame is None:
            return None
            
        # Layer 2: Data Link - Extract packet from frame
        packet = self.data_link.process_frame(frame)
        if packet is None:
            return None
            
        # Layer 3: Network - Extract segment from packet
        segment = self.network.process_packet(packet)
        if segment is None:
            return None
            
        # Layer 4: Transport - Extract session data from segment
        session_data = self.transport.process_segment(segment)
        if session_data is None:
            return None
            
        # Layer 5: Session - Extract presentation data and manage session
        presentation_data = self.session.process_session_data(session_data)
        if presentation_data is None:
            return None
            
        # Layer 6: Presentation - Convert to application format
        application_data = self.presentation.process_data(presentation_data)
        if application_data is None:
            return None
            
        # Layer 7: Application - Process message
        result = self.application.process_message(application_data)
        
        return result

# Example usage
if __name__ == "__main__":
    import sys
    import threading
    import time
    
    # Check if we should run as server or client
    mode = "both"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    # Run in combined mode (both server and client)
    if mode == "both":
        # Start server in a separate thread
        server = OSIServer()
        server_thread = threading.Thread(target=server.start)
        server_thread.daemon = True
        server_thread.start()
        
        # Wait for server to initialize
        time.sleep(1)
        
        # Start client
        client = OSIClient()
        client.start()
        
        # Wait for client to finish
        time.sleep(1)
        
        # Stop server
        server.stop()
        
    # Run as server only
    elif mode == "server":
        server = OSIServer()
        server.start()
        
    # Run as client only
    elif mode == "client":
        client = OSIClient()
        client.start()
        
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python main.py [server|client|both]")
        sys.exit(1)
