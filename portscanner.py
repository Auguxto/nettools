from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue
from threading import Thread
import requests

target = str(input("Qual o IP: "))
queue = Queue()
open_ports = []

http_services = []

def portscan(port):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f"[+] Discovered port service: {port}")
            open_ports.append(port)
            url = f"http://{target}:{port}"
            try:
                requests.get(url)
            except requests.ConnectionError:
                pass
            else:
                http_services.append(url)
                print("[+] Discovered http service:", url)

port_list = range(1, 65535)
fill_queue(port_list)

thread_list = []

for t in range(10000):
    thread = Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print(f"Open ports are: {open_ports}")