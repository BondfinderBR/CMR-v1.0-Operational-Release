import random
import math

# -----------------------------
# Funções básicas
# -----------------------------

def decide(x):
    return 1 if x >= 0 else -1

def instabilidade(seq):
    mudanças = sum(1 for i in range(1, len(seq)) if seq[i] != seq[i-1])
    return mudanças / len(seq)

# -----------------------------
# Meio Anti-Cristalização
# -----------------------------

class MeioAntiCristalizacao:
    def __init__(self, ruido_base=0.8, alpha=2.5):
        self.ruido_base = ruido_base
        self.alpha = alpha
        self.estado_latente = random.choice([-1, 1])

    def observar(self, estabilidade):
        ruido = random.gauss(0, self.ruido_base + self.alpha * estabilidade)
        return self.estado_latente + ruido

# -----------------------------
# Observador com memória
# -----------------------------

class Observador:
    def __init__(self, k=25, lambd=0.1):
        self.k = k
        self.lambd = lambd
        self.buffer = []
        self.realidade = []

    def memoria(self):
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

    def passo(self, leitura):
        self.buffer.insert(0, leitura)
        if len(self.buffer) > self.k:
            self.buffer.pop()
        psi = self.memoria()
        r = decide(psi)
        self.realidade.append(r)
        return r

# -----------------------------
# Experimento E1
# -----------------------------

def experimento_E1(passos=300):
    meio = MeioAntiCristalizacao()
    obs = Observador()

    estabilidade_hist = []

    for t in range(passos):
        if len(obs.realidade) < 5:
            estabilidade = 0.0
        else:
            estabilidade = 1 - instabilidade(obs.realidade[-50:])

        estabilidade_hist.append(estabilidade)
        leitura = meio.observar(estabilidade)
        obs.passo(leitura)

    I = instabilidade(obs.realidade)
    S = 1 - I

    return I, S, estabilidade_hist

# -----------------------------
# Execução
# -----------------------------

I, S, hist = experimento_E1()

print("\n🧪 CMR–E1 — MEIO ANTI-CRISTALIZAÇÃO\n")
print(f"Instabilidade final: {I:.3f}")
print(f"Estabilidade final : {S:.3f}")
print(f"Estabilidade média : {sum(hist)/len(hist):.3f}")

if S < 0.95:
    print("✅ Cristalização evitada")
else:
    print("⚠️ Estabilidade excessiva detectada")
