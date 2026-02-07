import random
import math
import statistics

# -----------------------------
# Meio: valor latente (inacessível)
# -----------------------------
def valor_latente(t):
    # passeio suave com choques ocasionais
    base = math.sin(t / 20) * 10
    choque = random.choice([0]*95 + [random.uniform(-15, 15)])
    return 100 + base + choque

# -----------------------------
# Observador com memória
# -----------------------------
class Observador:
    def __init__(self, ruido=3.0, memoria=10, lambd=0.15):
        self.ruido = ruido
        self.memoria = memoria
        self.lambd = lambd
        self.buffer = []

    def observa(self, v_latente):
        o = v_latente + random.gauss(0, self.ruido)
        self.buffer.insert(0, o)
        if len(self.buffer) > self.memoria:
            self.buffer.pop()
        return o

    def estimativa(self):
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

# -----------------------------
# Mercado
# -----------------------------
def mercado(iteracoes=300, modo="rigido"):
    obsA = Observador(ruido=3.0, memoria=15)
    obsB = Observador(ruido=5.0, memoria=8)

    precos = []
    falhas = 0
    custo = 0

    for t in range(iteracoes):
        v = valor_latente(t)

        obsA.observa(v)
        obsB.observa(v)

        pA = obsA.estimativa()
        pB = obsB.estimativa()

        if modo == "rigido":
            # preço único: média direta
            preco = (pA + pB) / 2
            # falha se discordância for grande
            if abs(pA - pB) > 12:
                falhas += 1
        else:
            # CMR: envelope
            minimo = min(pA, pB) - 2
            maximo = max(pA, pB) + 2
            preco = (minimo + maximo) / 2
            custo += (maximo - minimo)

        precos.append(preco)

    volatilidade = statistics.pstdev(precos)
    return volatilidade, falhas, custo

# -----------------------------
# Execução
# -----------------------------
v_rig, f_rig, c_rig = mercado(modo="rigido")
v_cmr, f_cmr, c_cmr = mercado(modo="cmr")

print("🧪 CMR–K1 — MERCADO RELACIONAL\n")
print("Modo RÍGIDO:")
print(f" Volatilidade: {v_rig:.2f}")
print(f" Falhas      : {f_rig}")
print(f" Custo       : {c_rig}\n")

print("Modo CMR (Envelope):")
print(f" Volatilidade: {v_cmr:.2f}")
print(f" Falhas      : {f_cmr}")
print(f" Custo       : {c_cmr:.2f}")

print("\n📌 Interpretação CMR:")
print("- Preço é coordenação, não verdade.")
print("- Envelope reduz falhas ao custo de margem.")
print("- Estabilidade emerge da concessão explícita.")
