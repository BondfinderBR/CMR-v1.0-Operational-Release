# observer.py
import sys, json, time, socket, statistics, csv

label = sys.argv[1]
config_path = sys.argv[2]
outfile = sys.argv[3]

with open(config_path) as f:
    cfg = json.load(f)

SERVER = (cfg["server"]["ip"], cfg["server"]["port"])
N = cfg["observer"]["samples"]
INTERVAL = cfg["observer"]["interval_ms"] / 1000
WINDOW = cfg["observer"]["memory_window"]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

samples = []

for _ in range(N):
    t0 = time.time()
    sock.sendto(b"ping", SERVER)
    try:
        sock.recvfrom(1024)
        rtt = time.time() - t0
        samples.append(rtt)
    except:
        pass
    time.sleep(INTERVAL)

events = []
for i, x in enumerate(samples):
    if WINDOW > 0:
        base = statistics.mean(samples[max(0, i-WINDOW):i+1])
    else:
        base = statistics.mean(samples)
    events.append(1 if x > base else -1)

with open(outfile, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["index", "event"])
    for i,e in enumerate(events):
        writer.writerow([i,e])
