# CMR–C4β — Fragmentação Permanente (Meio Incompatível)
# Autor: Flávio Oliveira
# Objetivo: Demonstrar fragmentação irreversível quando o meio deixa de ser compartilhado

import random
import math

# ===============================
# MEIO INCOMPATÍVEL
# ===============================

def meio(vies):
    """
    Meio físico com viés estrutural.
    Observadores acessam distribuições diferentes.
    """
    return random.gauss(vies, 2.5)

# ===============================
# OBSERVADOR
# ===============================

class Observador:
    def __init__(self, k=30, lambd=0.05, vies=0.0):
        self.k = k
        self.lambd = lambd
        self.vies = vies
        self.buffer = []
        self.realidade = []

    def observa(self, valor):
        self.buffer.insert(0, valor)
        if len(self.buffer) > self.k:
            self.buffer.pop()

        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)

        psi = sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z
        r = 1 if psi >= 0 else -1
        self.realidade.append(r)

    def instabilidade(self):
        if len(self.realidade) < 2:
            return 0
        mud = sum(
            1 for i in range(1, len(self.realidade))
            if self.realidade[i] != self.realidade[i-1]
        )
        return mud / len(self.realidade)

    def reset(self):
        self.buffer = []

# ===============================
# MÉTRICAS
# ===============================

def divergencia(A, B):
    return sum(
        1 for a, b in zip(A.realidade, B.realidade) if a != b
    ) / min(len(A.realidade), len(B.realidade))

# ===============================
# EXPERIMENTO C4β
# ===============================

def experimento_C4B(amostras=300):
    A = Observador(k=30, lambd=0.05, vies=+0.8)
    B = Observador(k=30, lambd=0.05, vies=-0.8)

    # Fase 1 — Antes do reset
    for _ in range(amostras):
        A.observa(meio(+0.6))
        B.observa(meio(-0.6))

    div_pre = divergencia(A, B)

    # Reset de memória
    A.reset()
    B.reset()

    # Fase 2 — Pós-reset
    for _ in range(amostras):
        A.observa(meio(+0.6))
        B.observa(meio(-0.6))

    div_pos = divergencia(A, B)

    Fp = div_pre - div_pos

    print("\n🧪 CMR–C4β — FRAGMENTAÇÃO PERMANENTE (MEIO INCOMPATÍVEL)\n")
    print(f"Instabilidade A: {A.instabilidade():.3f}")
    print(f"Instabilidade B: {B.instabilidade():.3f}")
    print(f"Divergência pré-reset: {div_pre:.3f}")
    print(f"Divergência pós-reset: {div_pos:.3f}")
    print(f"Índice de Fragmentação (Fp): {Fp:.3f}")

    if Fp >= 0:
        print("🚫 Fragmentação permanente confirmada")
    else:
        print("⚠️ Reconvergência ainda possível")

# ===============================
# EXECUÇÃO
# ===============================

if __name__ == "__main__":
    experimento_C4B()
