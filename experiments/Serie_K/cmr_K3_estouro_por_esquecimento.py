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

    def mistura_memoria(self, outro, peso=0.4):
        if outro.buffer:
            self.buffer[0] = (
                (1 - peso) * self.buffer[0] +
                peso * outro.buffer[0]
            )

    def esquece(self, taxa=0.3):
        if self.buffer:
            self.buffer = [
                x * (1 - taxa) + random.gauss(0, self.ruido)
                for x in self.buffer
            ]

    def estimativa(self):
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

# -----------------------------
# Mercado com bolha + esquecimento
# -----------------------------
def mercado_com_estouro(iteracoes=400,
                        inicio_bolha=120,
                        fim_bolha=260,
                        inicio_esquecimento=260):
    A = Observador(ruido=3.0)
    B = Observador(ruido=4.0)

    divergencias = []
    precos = []

    for t in range(iteracoes):
        v = valor_latente(t)

        A.observa(v)
        B.observa(v)

        # alinhamento narrativo (bolha)
        if inicio_bolha <= t <= fim_bolha:
            A.mistura_memoria(B)
            B.mistura_memoria(A)

        # esquecimento acelerado
        if t >= inicio_esquecimento:
            A.esquece()
            B.esquece()

        pA = A.estimativa()
        pB = B.estimativa()

        precos.append((pA + pB) / 2)
        divergencias.append(abs(pA - pB))

    return precos, divergencias

# -----------------------------
# Execução
# -----------------------------
precos, divs = mercado_com_estouro()

print("🧪 CMR–K3 — ESTOURO POR ESQUECIMENTO\n")
print(f"Divergência média total: {statistics.mean(divs):.2f}")
print(f"Divergência mínima:      {min(divs):.2f}")
print(f"Divergência final:       {divs[-1]:.2f}")
print(f"Preço final:             {precos[-1]:.2f}")

print("\n📌 Interpretação CMR:")
print("- Não houve choque externo.")
print("- O meio permaneceu estável.")
print("- A perda de memória rompeu o consenso.")
print("- O estouro é um evento cognitivo, não físico.")
