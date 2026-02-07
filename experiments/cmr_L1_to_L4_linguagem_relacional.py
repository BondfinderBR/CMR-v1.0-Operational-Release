import random
import math
import statistics

# -----------------------------
# Conceito latente (meio estável)
# -----------------------------
def conceito_latente(t):
    return 1.0  # conceito estável (ex: "liberdade")

# -----------------------------
# Observador semântico
# -----------------------------
class ObservadorSemantico:
    def __init__(self, ruido=0.6, memoria=12, lambd=0.15):
        self.ruido = ruido
        self.memoria = memoria
        self.lambd = lambd
        self.buffer = []

    def observa(self, v):
        o = v + random.gauss(0, self.ruido)
        self.buffer.insert(0, o)
        if len(self.buffer) > self.memoria:
            self.buffer.pop()
        return o

    def mistura(self, outro, peso=0.5):
        if outro.buffer:
            self.buffer[0] = (1 - peso) * self.buffer[0] + peso * outro.buffer[0]

    def esquece(self, taxa=0.4):
        self.buffer = [
            x * (1 - taxa) + random.gauss(0, self.ruido)
            for x in self.buffer
        ]

    def significado(self):
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

# -----------------------------
# Execução L1 → L4
# -----------------------------
def serie_L(iteracoes=400,
            inicio_alinhamento=80,
            fim_alinhamento=200,
            inicio_esquecimento=240):

    A = ObservadorSemantico(ruido=0.6)
    B = ObservadorSemantico(ruido=0.8)

    divergencias = []

    for t in range(iteracoes):
        v = conceito_latente(t)

        A.observa(v)
        B.observa(v)

        # L2/L3 — alinhamento narrativo
        if inicio_alinhamento <= t <= fim_alinhamento:
            A.mistura(B)
            B.mistura(A)

        # L4 — esquecimento
        if t >= inicio_esquecimento:
            A.esquece()
            B.esquece()

        sA = A.significado()
        sB = B.significado()
        divergencias.append(abs(sA - sB))

    return divergencias

# -----------------------------
# Execução
# -----------------------------
divs = serie_L()

print("🧪 CMR–L — LINGUAGEM RELACIONAL\n")
print(f"Divergência média total: {statistics.mean(divs):.2f}")
print(f"Divergência mínima:      {min(divs):.2f}")
print(f"Divergência final:       {divs[-1]:.2f}")

print("\n📌 Interpretação CMR:")
print("- O conceito latente permaneceu estável.")
print("- O consenso reduziu divergência temporariamente.")
print("- O esquecimento fragmentou o significado.")
print("- O colapso foi semântico, não físico.")
