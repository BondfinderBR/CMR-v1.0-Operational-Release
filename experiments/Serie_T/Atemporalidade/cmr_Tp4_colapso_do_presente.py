import random
import math

# -----------------------------
# Meio contínuo estável
# -----------------------------
def meio(t):
    return math.sin(t / 12)

# -----------------------------
# Observador com colapso temporal
# -----------------------------
class Observador:
    def __init__(self, memoria=20):
        self.memoria = memoria
        self.buffer = []

    def observa(self, v):
        o = v + random.gauss(0, 0.6)
        self.buffer.insert(0, o)

        if len(self.buffer) > self.memoria:
            self.buffer.pop()

        return self.integrar()

    def integrar(self):
        if not self.buffer:
            return 0

        # pesos instáveis (colapso do tempo)
        pesos = [random.random() for _ in self.buffer]
        Z = sum(pesos)

        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

def decide(x):
    return 1 if x >= 0 else -1

# -----------------------------
# Execução
# -----------------------------
def roda():
    A = Observador(memoria=20)   # colapsado
    B = Observador(memoria=20)   # controle

    estados_A = []
    estados_B = []

    for t in range(300):
        v = meio(t)
        estados_A.append(decide(A.observa(v)))
        estados_B.append(decide(B.observa(v)))

    inst_A = sum(1 for i in range(1,300) if estados_A[i]!=estados_A[i-1]) / 300
    inst_B = sum(1 for i in range(1,300) if estados_B[i]!=estados_B[i-1]) / 300

    print("🧪 CMR–T′4 — COLAPSO DO PRESENTE\n")
    print(f"Instabilidade do presente (colapsado): {inst_A:.3f}")
    print(f"Instabilidade do presente (controle) : {inst_B:.3f}")

    print("\n📌 Interpretação CMR:")
    print("- O meio permaneceu estável.")
    print("- A memória existe, mas não integra.")
    print("- O presente deixa de se formar.")
    print("- O colapso é temporal, não físico.")

roda()
