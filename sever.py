import socket
import threading

tuple_space = []

def handle_client(client_socket, addr):
    print(f"New client connected from {addr}")

    try:
        # Something server need to handle
        print("")
    except Exception as e:
        print(f"Error in handeling client {addr}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {addr} has been closed")

def READ(k):
     for item in tuple_space:
        if item[0] == k:
            return item[1]
        return None
     
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

    print("Server is running and ready to accept multiple clients...")

    try: 
        while True:
            # Accept a client connection
            client_socket, addr = server_socket.accept()

            # Establish a thread to handle the requests from the client
            client_thread = threading.Thread(target = handle_client, args = (client_socket, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()

