import socket

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the server hostname and port
host = socket.gethostname()
port = 5053

# connection to hostname on the port.
client_socket.connect((host, port))

# receive some data from the server
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    print(data.decode())

# close the client socket
client_socket.close()
