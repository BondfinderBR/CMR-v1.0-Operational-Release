import time, random, json, os

STATE_FILE = "shared_state.json"
TMP_FILE = "shared_state.tmp"

while True:
    event = random.choice([1, -1])
    payload = {"event": event, "ts": time.time()}

    with open(TMP_FILE, "w") as f:
        json.dump(payload, f)
        f.flush()
        os.fsync(f.fileno())

    # troca atômica
    os.replace(TMP_FILE, STATE_FILE)

    time.sleep(0.05)
