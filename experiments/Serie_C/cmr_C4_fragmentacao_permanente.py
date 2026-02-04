import random
import math

# ---------- Meio ----------
def meio_fragil():
    # meio sem baseline forte
    return random.gauss(0, 2.5)

# ---------- Observador ----------
class Observador:
    def __init__(self, k, lambd, vies):
        self.k = k
        self.lambd = lambd
        self.vies = vies
        self.buffer = []

    def observa(self):
        o = meio_fragil() + self.vies
        self.buffer.insert(0, o)
        if len(self.buffer) > self.k:
            self.buffer.pop()

        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        psi = sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

        return 1 if psi >= 0 else -1

    def reset(self):
        self.buffer = []

# ---------- Métricas ----------
def instabilidade(seq):
    return sum(seq[i] != seq[i-1] for i in range(1, len(seq))) / len(seq)

def divergencia(a, b):
    return sum(x != y for x, y in zip(a, b)) / len(a)

# ---------- Experimento C4 ----------
def experimento_C4(amostras=300):
    A = Observador(k=30, lambd=0.05, vies=+0.8)
    B = Observador(k=30, lambd=0.05, vies=-0.8)

    seqA, seqB = [], []

    # Fase 1 — evolução normal
    for _ in range(amostras):
        seqA.append(A.observa())
        seqB.append(B.observa())

    instA = instabilidade(seqA)
    instB = instabilidade(seqB)
    div_pre = divergencia(seqA, seqB)

    # Fase 2 — reset forçado
    A.reset()
    B.reset()
    seqA_r, seqB_r = [], []

    for _ in range(amostras):
        seqA_r.append(A.observa())
        seqB_r.append(B.observa())

    div_pos = divergencia(seqA_r, seqB_r)
    Fp = div_pos - div_pre

    return {
        "instA": instA,
        "instB": instB,
        "div_pre": div_pre,
        "div_pos": div_pos,
        "Fp": Fp
    }

# ---------- Execução ----------
r = experimento_C4()

print("\n🧪 CMR–C4 — FRAGMENTAÇÃO PERMANENTE\n")
print(f"Instabilidade A: {r['instA']:.3f}")
print(f"Instabilidade B: {r['instB']:.3f}")
print(f"Divergência pré-reset: {r['div_pre']:.3f}")
print(f"Divergência pós-reset: {r['div_pos']:.3f}")
print(f"Índice de Fragmentação (Fp): {r['Fp']:.3f}")

if r["Fp"] >= 0:
    print("\n❌ Fragmentação Permanente Confirmada")
else:
    print("\n⚠️ Reconvergência possível")
