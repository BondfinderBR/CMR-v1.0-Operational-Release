import random
import math
import statistics

# -----------------------------
# Meio causal estável com mudança
# -----------------------------
def meio(t):
    if t < 50:
        return 100
    else:
        return 120  # mudança real do meio


# -----------------------------
# Observador
# -----------------------------
class Observador:
    def __init__(self, ruido=2.0, memoria=15, lambd=0.15):
        self.ruido = ruido
        self.memoria = memoria
        self.lambd = lambd
        self.buffer = []

    def observa(self, valor):
        o = valor + random.gauss(0, self.ruido)
        self.buffer.insert(0, o)
        if len(self.buffer) > self.memoria:
            self.buffer.pop()
        return o

    def estimativa(self):
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z


# -----------------------------
# Métrica CMR — Tempo de Reconvergência
# -----------------------------
def tempo_reconvergencia(series, alvo, epsilon=2.0):
    for t, v in enumerate(series):
        if abs(v - alvo) < epsilon:
            return t
    return None


# -----------------------------
# Experimento
# -----------------------------
def experimento():
    obs_A = Observador(memoria=20, lambd=0.12)   # presente funcional
    obs_B = Observador(memoria=5, lambd=0.45)    # presente fantasma

    estimativas_A = []
    estimativas_B = []

    for t in range(100):
        v = meio(t)
        obs_A.observa(v)
        obs_B.observa(v)

        estimativas_A.append(obs_A.estimativa())
        estimativas_B.append(obs_B.estimativa())

    alvo = 120

    tA = tempo_reconvergencia(estimativas_A[50:], alvo)
    tB = tempo_reconvergencia(estimativas_B[50:], alvo)

    return tA, tB


# -----------------------------
# Execução
# -----------------------------
tA, tB = experimento()

print("🧪 CMR–T′5b — PRESENTE FUNCIONAL vs FANTASMA\n")

print(f"Tempo de reconvergência Observador A: {tA}")
print(f"Tempo de reconvergência Observador B: {tB}")

print("\n📌 Interpretação CMR:")
if tA is not None and tB is None:
    print("- Observador A possui presente funcional.")
    print("- Observador B responde, mas nunca reconverge.")
    print("- O presente de B é fantasma.")
elif tA is None and tB is None:
    print("- Nenhum observador possui presente funcional.")
else:
    print("- Ambos possuem presente funcional em regimes distintos.")
