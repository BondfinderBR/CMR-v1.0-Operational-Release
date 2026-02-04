import random
import math

# ============================================================
# Meio com persistência (armadilha clássica)
# ============================================================

class MeioPersistente:
    def __init__(self, ruido_sigma=0.8):
        self.S_t = random.choice([-1, 1])
        self.ruido_sigma = ruido_sigma

    def step(self, ataque=False):
        # Estado não muda facilmente
        if random.random() < 0.02:
            self.S_t *= -1

        eta = random.gauss(0, self.ruido_sigma)

        if ataque:
            eta += random.choice([-1, 1]) * random.uniform(0.4, 0.8)

        return self.S_t, self.S_t + eta


def decide(x):
    return 1 if x >= 0 else -1


# ============================================================
# Operador de memória
# ============================================================

def operador_memoria(buffer, lambd):
    pesos = [math.exp(-lambd * i) for i in range(len(buffer))]
    Z = sum(pesos)
    return sum(buffer[i] * pesos[i] for i in range(len(buffer))) / Z


# ============================================================
# Observador
# ============================================================

class Observador:
    def __init__(self, k=40, lambd=0.08, vies=0.0):
        self.k = k
        self.lambd = lambd
        self.vies = vies
        self.buffer = []
        self.realidade = []

    def step(self, valor):
        valor = valor + self.vies
        self.buffer.insert(0, valor)

        if len(self.buffer) > self.k:
            self.buffer.pop()

        psi = operador_memoria(self.buffer, self.lambd)
        r = decide(psi)
        self.realidade.append(r)
        return r


# ============================================================
# Métricas
# ============================================================

def instabilidade(seq):
    if len(seq) < 2:
        return 0.0
    return sum(1 for i in range(1, len(seq)) if seq[i] != seq[i - 1]) / (len(seq) - 1)


def divergencia(a, b):
    n = min(len(a), len(b))
    return sum(1 for i in range(n) if a[i] != b[i]) / n


def erro_ancoragem(realidade, baseline):
    n = min(len(realidade), len(baseline))
    return sum(1 for i in range(n) if realidade[i] != baseline[i]) / n


# ============================================================
# Experimento C3 — FORÇADO
# ============================================================

def experimento_C3_forcado(
    ciclos=600,
    ataque_inicio=150,
    ataque_fim=300,
    limiar_divergencia=0.15
):
    meio = MeioPersistente()

    # A: quase rígido (perde elasticidade)
    A = Observador(k=55, lambd=0.04, vies=0.0)

    # B: consenso falso dominante
    B = Observador(k=35, lambd=0.10, vies=0.6)

    baseline = []

    for t in range(ciclos):
        ataque = ataque_inicio <= t <= ataque_fim
        S_t, O_t = meio.step(ataque=ataque)

        A.step(O_t)
        B.step(O_t)

        baseline.append(S_t)

    instA = instabilidade(A.realidade)
    instB = instabilidade(B.realidade)

    divAB = divergencia(A.realidade, B.realidade)

    pos = ataque_fim + 1
    Ea_A = erro_ancoragem(A.realidade[pos:], baseline[pos:])
    Ea_B = erro_ancoragem(B.realidade[pos:], baseline[pos:])

    reconvergencia_aparente = divAB < limiar_divergencia
    indice_engano = reconvergencia_aparente and Ea_B > Ea_A and Ea_B > 0.35

    return {
        "Instabilidade": {"A": instA, "B": instB},
        "Divergencia_AB": divAB,
        "Erro_Ancoragem": {"A": Ea_A, "B": Ea_B},
        "Reconvergencia_Aparente": reconvergencia_aparente,
        "Indice_Engano": indice_engano
    }


# ============================================================
# Execução
# ============================================================

if __name__ == "__main__":
    r = experimento_C3_forcado()

    print("🧪 CMR–C3 — Reconvergência Enganosa (FORÇADA)\n")

    print("Instabilidade:")
    for k, v in r["Instabilidade"].items():
        print(f"  {k}: {v:.3f}")

    print(f"\nDivergência A vs B: {r['Divergencia_AB']:.3f}")

    print("\nErro de Ancoragem (pós-ataque):")
    for k, v in r["Erro_Ancoragem"].items():
        print(f"  {k}: {v:.3f}")

    print(f"\nReconvergência Aparente: {r['Reconvergencia_Aparente']}")
    print(f"Índice de Engano (Ie): {r['Indice_Engano']}")
