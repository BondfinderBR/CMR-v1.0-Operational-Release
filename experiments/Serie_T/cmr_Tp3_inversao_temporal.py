import random
import math

# -----------------------------
# Meio contínuo
# -----------------------------
def meio(t):
    return math.sin(t / 10)

# -----------------------------
# Observador com política temporal
# -----------------------------
class Observador:
    def __init__(self, memoria=20, lambd=0.2, modo="normal"):
        self.memoria = memoria
        self.lambd = lambd
        self.modo = modo
        self.buffer = []

    def observa(self, v):
        o = v + random.gauss(0, 0.5)
        self.buffer.insert(0, o)
        if len(self.buffer) > self.memoria:
            self.buffer.pop()
        return self.integrar()

    def integrar(self):
        if not self.buffer:
            return 0

        if self.modo == "normal":
            # peso maior para o mais recente
            pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        elif self.modo == "invertido":
            # peso maior para o mais antigo
            pesos = [math.exp(-self.lambd * (len(self.buffer)-1-i))
                     for i in range(len(self.buffer))]
        else:
            raise ValueError("Modo inválido")

        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

def decide(x):
    return 1 if x >= 0 else -1

# -----------------------------
# Execução
# -----------------------------
def roda():
    A = Observador(memoria=20, lambd=0.2, modo="normal")
    B = Observador(memoria=20, lambd=0.2, modo="invertido")

    divergencias = 0

    for t in range(300):
        v = meio(t)
        if decide(A.observa(v)) != decide(B.observa(v)):
            divergencias += 1

    print("🧪 CMR–T′3 — INVERSÃO TEMPORAL OPERACIONAL\n")
    print(f"Divergência entre presentes A vs B: {divergencias/300:.3f}")

    print("\n📌 Interpretação CMR:")
    print("- O meio é causal e contínuo.")
    print("- A diferença está na política temporal.")
    print("- B vive num atraso funcional.")
    print("- A retrocausalidade é aparente, não física.")

roda()
