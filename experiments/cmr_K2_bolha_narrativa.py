import random
import math
import statistics

# -----------------------------
# Meio estável
# -----------------------------
def valor_latente(t):
    return 100 + math.sin(t / 30) * 5

# -----------------------------
# Observador
# -----------------------------
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

    def mistura_memoria(self, outro, peso=0.3):
        if outro.buffer:
            self.buffer[0] = (
                (1 - peso) * self.buffer[0] +
                peso * outro.buffer[0]
            )

    def estimativa(self):
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

# -----------------------------
# Mercado com narrativa
# -----------------------------
def mercado_com_bolha(iteracoes=400, inicio_bolha=150, fim_bolha=300):
    A = Observador(ruido=3.0)
    B = Observador(ruido=4.0)

    precos = []
    divergencias = []

    for t in range(iteracoes):
        v = valor_latente(t)

        A.observa(v)
        B.observa(v)

        # fase de alinhamento narrativo
        if inicio_bolha <= t <= fim_bolha:
            A.mistura_memoria(B, peso=0.4)
            B.mistura_memoria(A, peso=0.4)

        pA = A.estimativa()
        pB = B.estimativa()

        preco = (pA + pB) / 2
        precos.append(preco)
        divergencias.append(abs(pA - pB))

    return precos, divergencias

# -----------------------------
# Execução
# -----------------------------
precos, divs = mercado_com_bolha()

print("🧪 CMR–K2 — BOLHA NARRATIVA\n")
print(f"Divergência média: {statistics.mean(divs):.2f}")
print(f"Divergência mínima: {min(divs):.2f}")
print(f"Divergência final: {divs[-1]:.2f}")
print(f"Preço final: {precos[-1]:.2f}")

print("\n📌 Interpretação CMR:")
print("- O meio permaneceu estável.")
print("- A divergência caiu artificialmente.")
print("- O preço se descola sem ruído externo.")
print("- Bolhas são regimes de baixa divergência.")
