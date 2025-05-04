import socket
import threading

tuple_space = []

def handle_client(client_socket, addr):
    print(f"New client connected from {addr}")

    try:
        message = client_socket.recv(1024).decode('utf-8')
        parts = message.split()
        size = parts[0]
        operation = parts[1]
        key = parts[2]
        value = ' '.join(parts[3:])

        if operation == "R":
            v = READ(key)
            if v:
                # Obtain the correct size for the response
                old_response = f"OK ({key}, {v}) read"
                old_formatted_length = "{:03d}".format(len(old_response))
                old_message = f"{old_formatted_length} {old_response}"
                formatted_length = "{:03d}".format(len(old_message))
                response = f"{formatted_length} {old_response}"
            else:
                response = f"ERR {key} does not exist"
            client_socket.sendall(response.encode('utf-8'))


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
     
def GET(k):
    for item in tuple_space:
        if item[0] == k:
            tuple_space.remove(item)
            return item[1]
    return None

def PUT(k, v):
    for item in tuple_space:
        if item[0] == k:
            return 1
    tuple_space.append((k, v))
    return 0
     
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

