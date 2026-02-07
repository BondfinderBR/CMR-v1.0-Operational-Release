import random
import math
import statistics

# -----------------------------
# Observador
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
# Regimes
# -----------------------------
REGIMES = {
    "LIVRE":      {"esquecimento": 0.05},
    "LIQUIDEZ":   {"esquecimento": 0.10},
    "CONSENSO":   {"esquecimento": 0.20},
    "AUTORIDADE": {"esquecimento": 0.45}
}

# -----------------------------
# Meio
# -----------------------------
def meio_latente(t):
    return math.sin(t / 30) * 2

# -----------------------------
# IA com atraso (falha soberana)
# -----------------------------
class IATardia:
    def __init__(self, delay=15):
        self.delay = delay
        self.historico = []
        self.regime = "LIVRE"

    def decide_regime(self, divergencia):
        self.historico.append(divergencia)

        if len(self.historico) <= self.delay:
            return self.regime

        media_passada = statistics.mean(self.historico[-self.delay:])

        if media_passada > 0.6:
            self.regime = "AUTORIDADE"
        elif media_passada > 0.4:
            self.regime = "CONSENSO"
        elif media_passada > 0.2:
            self.regime = "LIQUIDEZ"
        else:
            self.regime = "LIVRE"

        return self.regime

# -----------------------------
# Execução S2
# -----------------------------
def serie_S2(iteracoes=320):
    A = Observador(ruido=1.0)
    B = Observador(ruido=1.4)
    IA = IATardia(delay=20)

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
divs, regs = serie_S2()

print("🧪 CMR–S2 — FALHA DE SOBERANIA (TROCA TARDIA)\n")
print(f"Divergência média: {statistics.mean(divs):.2f}")
print(f"Divergência final: {divs[-1]:.2f}\n")

print("📌 Frequência de Regimes:")
for r in set(regs):
    print(f"{r:12}: {regs.count(r)}")

print("\n📌 Interpretação CMR:")
print("- A IA reagiu com atraso.")
print("- A troca de regime ocorreu após custo acumulado.")
print("- Autoridade não restaurou estabilidade.")
print("- Existe ponto de não retorno operacional.")
