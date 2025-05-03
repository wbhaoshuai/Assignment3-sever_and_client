import socket

def start_server():
    host = 'localhost'
    port = 51234

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Reuse address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to the port
    server_socket.bind((host, port))
    server_socket.listen(10)

    print("Server is running and waiting for client connection...")