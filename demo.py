import time
import threading
from main import OSIServer, OSIClient

def run_demo():
    print("="*50)
    print("OSI MODEL DEMONSTRATION")
    print("="*50)
    print("\nThis demo will start a server and client that communicate")
    print("through all 7 layers of the OSI model.")
    print("\nServer will listen on 127.0.0.1:8000")
    print("Client will send a request and display the response")
    print("="*50)
    
    # Start server in a separate thread
    print("\nStarting OSI Server...")
    server = OSIServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    
    # Give the server time to start
    time.sleep(2)
    
    # Start client
    print("\nStarting OSI Client...")
    client = OSIClient()
    client.start()
    
    # Wait for client to finish
    time.sleep(2)
    
    # Stop server
    print("\nShutting down server...")
    server.stop()
    
    print("\n" + "="*50)
    print("DEMONSTRATION COMPLETE")
    print("="*50)

if __name__ == "__main__":
    run_demo()
