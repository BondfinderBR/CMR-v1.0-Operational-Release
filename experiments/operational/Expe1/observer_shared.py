#!/usr/bin/env python3

import sys
import json
import time
import statistics
import csv
import os

# ===============================
# ARGUMENTOS
# ===============================
# argv[1] = label (A ou B)
# argv[2] = memory window (int)
# argv[3] = samples (int)
# argv[4] = interval_ms (int)
# argv[5] = output csv path

label = sys.argv[1]
WINDOW = int(sys.argv[2])
SAMPLES = int(sys.argv[3])
INTERVAL = int(sys.argv[4]) / 1000.0
OUTFILE = sys.argv[5]

STATE_FILE = "shared_state.json"

# ===============================
# FUNÇÃO DE LEITURA SEGURA
# ===============================
def read_state():
    """
    Lê o estado do meio causal comum.
    Garante que nunca retorna JSON inválido.
    Não altera semanticamente o experimento.
    """
    while True:
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
            return data
        except (json.JSONDecodeError, FileNotFoundError):
            # Espera mínima para evitar busy-wait
            time.sleep(0.001)

# ===============================
# EXECUÇÃO
# ===============================
history = []

with open(OUTFILE, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["index", "event", "perceived"])

    for i in range(SAMPLES):
        state = read_state()
        value = int(state["event"])

        history.append(value)

        # Integração temporal (memória)
        if WINDOW > 0 and len(history) >= WINDOW:
            base = statistics.mean(history[-WINDOW:])
        else:
            base = statistics.mean(history)

        # Materialização local do observador
        perceived = 1 if value > base else -1

        writer.writerow([i, value, perceived])

        time.sleep(INTERVAL)

print(f"[OBS {label}] finished — samples={SAMPLES}, memory={WINDOW}")
