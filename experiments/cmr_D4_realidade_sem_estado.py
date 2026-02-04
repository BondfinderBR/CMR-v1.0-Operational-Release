# CMR–D4 — Realidade sem Estado
# Processo puro sem convergência
# Autor: Flávio Oliveira

import random
import math
import statistics

# ===============================
# MEIO (altamente variável)
# ===============================

def meio():
    return random.gauss(0, 5.0)

# ===============================
# PROCESSO SEM ESTADO
# ===============================

class Processo:
    def __init__(self, k=5, lambd=0.8):
        self.k = k
        self.lambd = lambd
        self.buffer = []
        self.trajetoria = []

    def passo(self):
        v = meio()
        self.buffer.insert(0, v)
        if len(self.buffer) > self.k:
            self.buffer.pop()

        # integração agressiva (sem convergência)
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)

        estado = sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z
        self.trajetoria.append(estado)

# ===============================
# MÉTRICAS
# ===============================

def variancia(seq):
    if len(seq) < 2:
        return 0
    return statistics.variance(seq)

def deriva(seq):
    # mede ausência de platô
    diffs = [abs(seq[i] - seq[i-1]) for i in range(1, len(seq))]
    return statistics.mean(diffs)

# ===============================
# EXPERIMENTO D4
# ===============================

def experimento_D4(passos=800):
    P = Processo(k=5, lambd=0.9)

    for _ in range(passos):
        P.passo()

    var = variancia(P.trajetoria)
    der = deriva(P.trajetoria)

    print("\n🕳️ CMR–D4 — REALIDADE SEM ESTADO\n")
    print(f"Variância da trajetória: {var:.3f}")
    print(f"Deriva média (sem platô): {der:.3f}")

    if var < 50 and der > 0.2:
        print("\n✅ Processo funcional sem estado estável")
    else:
        print("\n⚠️ Colapso ou instabilidade extrema")

# ===============================
# EXECUÇÃO
# ===============================

if __name__ == "__main__":
    experimento_D4()
