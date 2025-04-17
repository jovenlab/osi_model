import json
import socket
import uuid

# Get local IP and MAC address
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                    for ele in range(0, 48, 8)][::-1])
    return mac
    
# Physical Layer
class PhysicalLayer:
    def send(self, data):
        print("[Physical Layer] Sending data as bits")
        bits = ''.join(format(ord(char), '08b') for char in data)
        return bits

    def receive(self, bits):
        print("[Physical Layer] Receiving data from bits")
        chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
        return ''.join(chars)

# Data Link Layer
class DataLinkLayer:
    def send(self, bits, mac_address):
        print(f"[Data Link Layer] Creating frame with MAC address: {mac_address}")
        frame = {'MAC': mac_address, 'Data': bits}
        return frame

    def receive(self, frame):
        print(f"[Data Link Layer] Extracting data from frame with MAC address: {frame['MAC']}")
        return frame['Data']

# Network Layer
class NetworkLayer:
    def send(self, frame, ip_address):
        print(f"[Network Layer] Creating packet with IP address: {ip_address}")
        packet = {'IP': ip_address, 'Frame': frame}
        return packet

    def receive(self, packet):
        print(f"[Network Layer] Extracting frame from packet with IP address: {packet['IP']}")
        return packet['Frame']

# Transport Layer
class TransportLayer:
    def send(self, packet, seq_num):
        print(f"[Transport Layer] Adding sequence number: {seq_num}")
        segment = {'Seq': seq_num, 'Packet': packet}
        return segment

    def receive(self, segment):
        print(f"[Transport Layer] Extracting packet from segment with sequence number: {segment['Seq']}")
        return segment['Packet']

# Session Layer
class SessionLayer:
    def send(self, segment, session_id):
        print(f"[Session Layer] Managing session with ID: {session_id}")
        session = {'SessionID': session_id, 'Segment': segment}
        return session

    def receive(self, session):
        print(f"[Session Layer] Extracting segment from session with ID: {session['SessionID']}")
        return session['Segment']

# Presentation Layer
class PresentationLayer:
    def send(self, session):
        print("[Presentation Layer] Encoding session data")
        encoded = json.dumps(session)
        return encoded

    def receive(self, encoded):
        print("[Presentation Layer] Decoding session data")
        session = json.loads(encoded)
        return session

# Application Layer
class ApplicationLayer:
    def send(self, message):
        print("[Application Layer] Creating HTTP-like request")
        request = {'HTTP_Request': message}
        return request

    def receive(self, request):
        print("[Application Layer] Extracting message from request")
        return request['HTTP_Request']

# Simulate communication
if __name__ == "__main__":
    message = "Hello, OSI Model!"
    mac_address = get_mac_address()
    ip_address = get_local_ip()
    seq_num = "1"
    session_id = "12345"

    # Instantiate each layer
    app = ApplicationLayer()
    pres = PresentationLayer()
    sess = SessionLayer()
    trans = TransportLayer()
    net = NetworkLayer()
    data_link = DataLinkLayer()
    phys = PhysicalLayer()

    print("\nStarting OSI Model Simulation...\n")
    print(f"Local IP Address: {ip_address}")
    print(f"Local MAC Address: {mac_address}\n")

    # Sending
    app_data = app.send(message)
    pres_data = pres.send(app_data)
    sess_data = sess.send(pres_data, session_id)
    trans_data = trans.send(sess_data, seq_num)
    net_data = net.send(trans_data, ip_address)
    link_data = data_link.send(json.dumps(net_data), mac_address)
    phys_data = phys.send(json.dumps(link_data))

    print("\n--- Data Sent ---\n")

    # Receiving
    received_bits = phys.receive(phys_data)
    received_frame = json.loads(received_bits)
    received_link_data = data_link.receive(received_frame)
    received_packet = json.loads(received_link_data)
    received_segment = net.receive(received_packet)
    received_session = trans.receive(received_segment)
    received_pres = sess.receive(received_session)
    received_app = pres.receive(received_pres)
    received_message = app.receive(received_app)

    print("\n--- Data Received ---\n")
    print("Received message:", received_message)
    print("OSI Model Simulation Complete!")