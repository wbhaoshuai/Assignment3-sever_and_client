import socket
import threading
import time

def client_task(name, pathname):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 51234))

        try:
            # Open the file for reading
            with open(pathname, 'r', encoding='utf-8') as file:
                line = file.readline()
                while line:
                    # Remove line breaks at the end of each line
                    line = line.strip()
                    # Split each line by space (up to 1 split)
                    parts = line.split(' ', 1)
                    operation = parts[0]
                    content = parts[1]
                    if len(parts) == 2:
                        # Check if k and v length exceeds 970
                        if len(content) > 970:
                            print(f"Error: The content of line '{line}' exceeds 970 characters. Ignoring this entry.")
                            line = file.readline()
                            continue
                        # Map to a single character based on operators
                        if operation == 'GET':
                            op_char = 'G'
                        elif operation == 'READ':
                            op_char = 'R'
                        elif operation == 'PUT':
                            op_char = 'P'
                    newline = f"{op_char} {content}"
                    old_formatted_length = "{:03d}".format(len(newline))
                    old_message = f"{old_formatted_length} {newline}"
                    formatted_length = "{:03d}".format(len(old_message))
                    message = f"{formatted_length} {newline}"
                    
                    # send a message
                    client_socket.sendall(message.encode('utf-8'))

                    # Waiting for receiving response
                    response = client_socket.recv(1024).decode('utf-8')
                    if response:
                        # formats resonse and outputs it
                        response_content = response[4:]
                        output = f"{operation} {content}: {response_content}"
                        print(output)
                        # Received valid response, continue processing the next line
                        line = file.readline()
                    else:
                         print("No valid response received.")
            stop_message = "Stop"
            client_socket.sendall(stop_message.encode('utf-8'))


        except FileNotFoundError:
            print("File not found, please check the file path.")       
    except Exception as e:
        print(f"Error for {name}: {e}")
    finally:
        client_socket.close()


def main():
    clients = []
    for i in range(10):
        t = threading.Thread(target = client_task, args = (f"client-{i+1}", f"client_{i + 1}.txt"))
        clients.append(t)
        t.start()
        time.sleep(0.1)

    for t in clients:
        t.join()
    # t = threading.Thread(target = client_task, args = (f"client-1", f"client_1.txt"))
    # t.start()
    # t.join()

if __name__ == "__main__":
   main()
