import socket
import threading
import time

def client_task(name):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 51234))

        # something client need todo
        
    except Exception as e:
        print(f"Error for {name}: {e}")
    finally:
        client_socket.close()


def main():
    clients = []
    for i in range(10):
        t = threading.Thread(target = client_task, args = (f"client-{i+1}",))
        clients.append(t)
        t.start()
        time.sleep(0.1)

    for t in clients:
        t.join()
