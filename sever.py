import socket
import threading
import time
tuple_space = []
lock = threading.Lock()
total_size = 0
total_tuple_size =0
total_key_size = 0
total_value_size = 0
total_client = 0
total_number_operations = 0
total_READs = 0
total_GETs = 0
total_PUTs = 0
total_errors = 0


def handle_client(client_socket, addr):
    global total_size, total_tuple_size, total_key_size, total_value_size, total_client, total_number_operations, total_READs, total_GETs, total_PUTs, total_errors
    print(f"New client connected from {addr}")
    total_client += 1

    try:
        while(True):
            message = client_socket.recv(1024).decode('utf-8')
            if(message == "Stop"):
                break
            total_number_operations += 1
            parts = message.split()
            operation = parts[1]
            key = parts[2]
            value = ' '.join(parts[3:])

            lock.acquire()
            try:
                if operation == "R":
                    v = READ(key)
                    total_READs += 1
                    if v:
                        old_response = f"OK ({key}, {v}) read"
                        response = format_response(old_response)
                    else:
                        old_response = f"ERR {key} does not exist"
                        response = format_response(old_response)
                        total_errors += 1
                elif operation == "G":
                    v = GET(key)
                    total_GETs += 1
                    if v:
                        old_response = f"OK ({key}, {v}) removed"
                        response = format_response(old_response)
                        total_key_size -= len(key)
                        total_value_size -= len(v)
                    else:
                        old_response = f"ERR {key} does not exist"
                        response = format_response(old_response)
                        total_errors += 1
                elif operation == "P":
                    e = PUT(key, value)
                    total_PUTs += 1
                    if not e:
                        old_response = f"OK ({key}, {value}) added"
                        response = format_response(old_response)
                        total_key_size += len(key)
                        total_value_size += len(value)
                    else:
                        old_response = f"ERR {key} already exists"
                        response = format_response(old_response)
                        total_errors += 1
            finally:
                lock.release()
            client_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error in handeling client {addr}: {e}")
        total_errors += 1
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

def format_response(old_response):
    old_formatted_length = "{:03d}".format(len(old_response))
    old_message = f"{old_formatted_length} {old_response}"
    formatted_length = "{:03d}".format(len(old_message))
    response = f"{formatted_length} {old_response}"
    return response

def sever_output():
    global total_size, total_tuple_size, total_key_size, total_value_size, total_client, total_number_operations, total_READs, total_GETs, total_PUTs, total_errors
    while True:
        time.sleep(10)
        print("-----------------------------------------------------------------")
        print(f"Number of tuples in the tuple space: {len(tuple_space)}")
        for item in tuple_space:
            item_str = str(item)
            total_size += len(item_str)
        print(f"The average tuple size: {total_size/len(tuple_space)}")
        print(f"The average key size: {total_key_size/len(tuple_space)}")
        print(f"The average value size: {total_value_size/len(tuple_space)}")
        print(f"The total number of clients which have connected (finished or not) so far: {total_client}")
        print(f"The total number of operations: {total_number_operations}")
        print(f"The total number of READS: {total_READs}")
        print(f"The total number of GET: {total_GETs}")
        print(f"The total number of PUTs: {total_PUTs}")
        print("")


     
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

    output_thread = threading.Thread(target = sever_output, args = ())
    output_thread.start()
    start_server()


