import random
import math
import statistics

# =====================================
# MEIO LATENTE (estável)
# =====================================
def valor_latente(t):
    return 100 + math.sin(t / 40) * 4


# =====================================
# OBSERVADOR CMR
# =====================================
class Observador:
    def __init__(self, ruido=3.0, memoria=12, lambd=0.12):
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

    def mistura(self, outro, peso):
        if self.buffer and outro.buffer:
            self.buffer[0] = (
                (1 - peso) * self.buffer[0] +
                peso * outro.buffer[0]
            )

    def ancora_externa(self, valor, peso=0.6):
        if self.buffer:
            self.buffer[0] = (
                (1 - peso) * self.buffer[0] +
                peso * valor
            )

    def estimativa(self):
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z


# =====================================
# SÉRIE K4 + K5 + K6
# =====================================
def mercado_regimes(iteracoes=420):
    A = Observador(ruido=3.0)
    B = Observador(ruido=4.0)

    divergencias = []
    precos = []
    regimes = []

    for t in range(iteracoes):
        v = valor_latente(t)

        A.observa(v)
        B.observa(v)

        # -----------------------------
        # K4 — Liquidez Relacional
        # -----------------------------
        if 80 <= t < 160:
            liquidez = 0.35
            A.mistura(B, liquidez)
            B.mistura(A, liquidez)
            regime = "Liquidez"

        # -----------------------------
        # K5 — Autoridade Externa
        # -----------------------------
        elif 160 <= t < 260:
            autoridade = 102  # âncora narrativa externa
            A.ancora_externa(autoridade)
            B.ancora_externa(autoridade)
            regime = "Autoridade"

        # -----------------------------
        # K6 — Troca de Regime
        # -----------------------------
        elif t >= 260:
            # custo de consenso supera custo de divergência
            if abs(A.estimativa() - B.estimativa()) < 1.0:
                A.mistura(B, 0.1)
                B.mistura(A, 0.1)
                regime = "Consenso Forçado"
            else:
                regime = "Fragmentação"

        else:
            regime = "Livre"

        pA = A.estimativa()
        pB = B.estimativa()

        precos.append((pA + pB) / 2)
        divergencias.append(abs(pA - pB))
        regimes.append(regime)

    return precos, divergencias, regimes


# =====================================
# EXECUÇÃO
# =====================================
precos, divs, regimes = mercado_regimes()

print("🧪 CMR–K4+K5+K6 — REGIMES DE MERCADO RELACIONAL\n")
print(f"Divergência média total: {statistics.mean(divs):.2f}")
print(f"Divergência mínima:      {min(divs):.2f}")
print(f"Divergência final:       {divs[-1]:.2f}")
print(f"Preço final:             {precos[-1]:.2f}")

print("\n📌 Frequência de Regimes:")
for r in sorted(set(regimes)):
    print(f"{r:18s}: {regimes.count(r)}")

print("\n📌 Interpretação CMR:")
print("- K4: Liquidez absorve divergência sem eliminar erro.")
print("- K5: Autoridade cria consenso artificial.")
print("- K6: O sistema troca de regime quando consenso fica caro.")
print("- Estabilidade não é verdade; é custo operacional mínimo.")
