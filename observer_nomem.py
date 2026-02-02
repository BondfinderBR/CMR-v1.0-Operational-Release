# observer_nomem.py
import socket, time, statistics

SERVER = ("ip.do.servidor", 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

samples = []

for _ in range(200):
    t0 = time.time()
    sock.sendto(b"ping", SERVER)
    try:
        data, _ = sock.recvfrom(1024)
        rtt = time.time() - t0
        samples.append(rtt)
    except:
        pass
    time.sleep(0.05)

mean = statistics.mean(samples)

events = [1 if x > mean else -1 for x in samples]
print(events)
