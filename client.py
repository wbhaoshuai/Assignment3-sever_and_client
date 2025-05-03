import socket
import threading
import time

def main():
    clients = []
    for i in range(10):
        t = threading.Thread(target = client_task, args = (f"client-{i+1}",))
        clients.append(t)
        t.start()
        time.sleep(0.1)

    for t in clients:
        t.join()
