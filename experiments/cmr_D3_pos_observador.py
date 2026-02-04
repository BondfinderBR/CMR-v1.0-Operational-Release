# CMR–D3 — Pós-Observador
# Realidade funcional sem observador, sem decisão, sem verdade
# Autor: Flávio Oliveira

import random
import math
import statistics

# ===============================
# MEIO
# ===============================

def meio():
    # meio ruidoso, sem significado
    return random.gauss(0, 2.0)

# ===============================
# MEMÓRIA AUTOMÁTICA
# ===============================

class Memoria:
    def __init__(self, k=30, lambd=0.1):
        self.k = k
        self.lambd = lambd
        self.buffer = []
        self.estados = []

    def atualiza(self, valor):
        self.buffer.insert(0, valor)
        if len(self.buffer) > self.k:
            self.buffer.pop()

        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)

        estado = sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z
        self.estados.append(estado)

# ===============================
# MÉTRICAS
# ===============================

def variancia(seq):
    if len(seq) < 2:
        return 0
    return statistics.variance(seq)

def estabilidade(seq):
    # estabilidade = quão pouco o estado varia ao longo do tempo
    diffs = [abs(seq[i] - seq[i-1]) for i in range(1, len(seq))]
    return statistics.mean(diffs)

# ===============================
# EXPERIMENTO D3
# ===============================

def experimento_D3(passos=500):
    M = Memoria(k=40, lambd=0.05)

    for _ in range(passos):
        M.atualiza(meio())

    var = variancia(M.estados)
    est = estabilidade(M.estados)

    print("\n🕳️ CMR–D3 — PÓS-OBSERVADOR\n")
    print(f"Variância do estado: {var:.3f}")
    print(f"Estabilidade dinâmica: {est:.3f}")

    if est < 0.5:
        print("\n✅ Realidade funcional emergiu sem observador")
    else:
        print("\n⚠️ Sistema instável — sem regime funcional")

# ===============================
# EXECUÇÃO
# ===============================

if __name__ == "__main__":
    experimento_D3()
