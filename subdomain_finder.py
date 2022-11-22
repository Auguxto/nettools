import requests
from queue import Queue
from threading import Thread

domain = input("Qual o dominio: ")

file = open("subdomains.txt")
content = file.read()

subdomains = content.splitlines()

queue = Queue()
discovered_subdomains = []

def find_subdomains(subdomain, domain):
    url = f"http://{subdomain}.{domain}"
    try:
        requests.get(url)
    except requests.ConnectionError:
        pass
    else:
        print("[+] Discovered subdomain:", url)
        discovered_subdomains.append(url)

def worker():
    while not queue.empty():
        subdomain = queue.get()
        find_subdomains(subdomain, domain)

for subdomain in subdomains:
    queue.put(subdomain)

thread_list = []

for t in range(10):
    thread = Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print(discovered_subdomains)