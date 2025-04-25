import socket

IP = '127.0.0.1'
port = 66

# Build socket between server and client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, port))

# End connection
client.socket.close()
