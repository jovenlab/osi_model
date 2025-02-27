import json
import time
import uuid

class ApplicationLayer:
    """Simulates the application layer with HTTP-like functionality."""
    
    def __init__(self):
        """Initialize application layer."""
        print("[Application] Initialized")
        
    def create_request(self, method, resource, headers=None, body=None):
        """Create an HTTP-like request."""
        if headers is None:
            headers = {}
            
        # Add standard headers
        headers['Request-ID'] = str(uuid.uuid4())
        headers['Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        
        # Create request object
        request = {
            'type': 'request',
            'method': method,
            'resource': resource,
            'headers': headers,
            'body': body
        }
        
        print(f"[Application] Created request: {method} {resource}")
        return request
        
    def create_response(self, status, status_message, headers=None, body=None):
        """Create an HTTP-like response."""
        if headers is None:
            headers = {}
            
        # Add standard headers
        headers['Response-ID'] = str(uuid.uuid4())
        headers['Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        
        # Create response object
        response = {
            'type': 'response',
            'status': status,
            'status_message': status_message,
            'headers': headers,
            'body': body
        }
        
        print(f"[Application] Created response: {status} {status_message}")
        return response
        
    def process_message(self, message):
        """Process a received message (request or response)."""
        if not isinstance(message, dict):
            print(f"[Application] Invalid message format: {type(message)}")
            return None
            
        message_type = message.get('type')
        
        if message_type == 'request':
            print(f"[Application] Received request: {message.get('method')} {message.get('resource')}")
            # In a real implementation, we would handle the request and generate a response
            return self.create_response(200, "OK", body={"message": "Request processed successfully"})
            
        elif message_type == 'response':
            print(f"[Application] Received response: {message.get('status')} {message.get('status_message')}")
            # In a real implementation, we would handle the response based on its status
            return message
            
        else:
            print(f"[Application] Unknown message type: {message_type}")
            return None
