import socket

# Set up the DNS server
DNS_IP_ADDRESS = '127.0.0.1'
DNS_PORT = 53

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((DNS_IP_ADDRESS, DNS_PORT))

print(f"DNS server listening on {DNS_IP_ADDRESS}:{DNS_PORT}...")

# A simple DNS response
dns_response = b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x2a\x00\x04\x7f\x00\x00\x01'

# Wait for incoming DNS queries
while True:
    data, address = server_socket.recvfrom(1024)
    print(f"Received DNS query from {address}")

    # Send the DNS response back to the client
    server_socket.sendto(dns_response, address)
