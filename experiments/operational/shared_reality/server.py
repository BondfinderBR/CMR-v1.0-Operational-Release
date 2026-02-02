# server.py
import time
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 9999))

while True:
    data, addr = sock.recvfrom(1024)
    now = time.time()
    sock.sendto(str(now).encode(), addr)
