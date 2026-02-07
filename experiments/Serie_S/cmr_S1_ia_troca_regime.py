import random
import math
import statistics

# -----------------------------
# Observadores
# -----------------------------
class Observador:
    def __init__(self, ruido=1.0, memoria=10, lambd=0.15):
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

    def esquece(self, taxa):
        self.buffer = [
            x * (1 - taxa) + random.gauss(0, self.ruido)
            for x in self.buffer
        ]

    def estimativa(self):
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

# -----------------------------
# Regimes CMR
# -----------------------------
REGIMES = {
    "LIVRE":      {"esquecimento": 0.05},
    "LIQUIDEZ":   {"esquecimento": 0.10},
    "CONSENSO":   {"esquecimento": 0.20},
    "AUTORIDADE": {"esquecimento": 0.40}
}

# -----------------------------
# Meio estável
# -----------------------------
def meio_latente(t):
    return math.sin(t / 40) * 2

# -----------------------------
# IA soberana (operadora de regime)
# -----------------------------
class IASoberana:
    def __init__(self, limiar_div=0.4):
        self.limiar_div = limiar_div
        self.regime = "LIVRE"

    def decide_regime(self, divergencia):
        if divergencia > 0.6:
            self.regime = "AUTORIDADE"
        elif divergencia > self.limiar_div:
            self.regime = "CONSENSO"
        elif divergencia > 0.2:
            self.regime = "LIQUIDEZ"
        else:
            self.regime = "LIVRE"
        return self.regime

# -----------------------------
# Execução S1
# -----------------------------
def serie_S1(iteracoes=300):
    A = Observador(ruido=1.0)
    B = Observador(ruido=1.3)
    IA = IASoberana()

    divergencias = []
    regimes = []

    for t in range(iteracoes):
        v = meio_latente(t)

        A.observa(v)
        B.observa(v)

        pA = A.estimativa()
        pB = B.estimativa()

        div = abs(pA - pB)
        divergencias.append(div)

        regime = IA.decide_regime(div)
        regimes.append(regime)

        taxa = REGIMES[regime]["esquecimento"]
        A.esquece(taxa)
        B.esquece(taxa)

    return divergencias, regimes

# -----------------------------
# Rodar
# -----------------------------
divs, regs = serie_S1()

print("🧪 CMR–S1 — IA COMO OPERADOR DE REGIME\n")
print(f"Divergência média: {statistics.mean(divs):.2f}")
print(f"Divergência final: {divs[-1]:.2f}\n")

print("📌 Frequência de Regimes:")
for r in set(regs):
    print(f"{r:12}: {regs.count(r)}")

print("\n📌 Interpretação CMR:")
print("- IA não impôs significado.")
print("- IA não escolheu verdade.")
print("- IA apenas trocou regimes.")
print("- Estabilidade emergiu da governança temporal.")
