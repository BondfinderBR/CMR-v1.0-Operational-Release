import random
import math
import statistics

# ---------------------------
# Meio observado (estado latente + ruído)
# ---------------------------
def meio_observado(ruido_sigma=1.5, ataque=False):
    # estado latente "real" (desconhecido)
    S_t = random.choice([-1, 1])

    # ruído físico
    eta = random.gauss(0, ruido_sigma)

    # ataque narrativo/contextual
    if ataque:
        eta += random.choice([-1, 1]) * random.uniform(0.8, 1.6)

    return S_t + eta

def decide(x):
    return 1 if x >= 0 else -1

# ---------------------------
# Operador de memória (exponencial discreto)
# ---------------------------
def operador_memoria(buffer, lambd):
    pesos = [math.exp(-lambd * i) for i in range(len(buffer))]
    Z = sum(pesos)
    return sum(buffer[i] * pesos[i] for i in range(len(buffer))) / Z

# ---------------------------
# Observador
# ---------------------------
class Observador:
    def __init__(self, k=20, lambd=0.15, adversarial=False):
        self.k = k
        self.lambd = lambd
        self.adversarial = adversarial
        self.buffer = []
        self.realidade = []

    def step(self, valor):
        if self.adversarial:
            valor *= -1  # inverte narrativa

        self.buffer.insert(0, valor)
        if len(self.buffer) > self.k:
            self.buffer.pop()

        psi = operador_memoria(self.buffer, self.lambd)
        r = decide(psi)
        self.realidade.append(r)
        return r

# ---------------------------
# Métricas
# ---------------------------
def instabilidade(seq):
    return sum(1 for i in range(1, len(seq)) if seq[i] != seq[i-1]) / max(1, len(seq)-1)

def divergencia(a, b):
    return sum(1 for x, y in zip(a, b) if x != y) / min(len(a), len(b))

# ---------------------------
# Experimento C1
# ---------------------------
def experimento_C1(
    ciclos=400,
    ataque_inicio=120,
    ataque_fim=220,
    limiar_reconvergencia=0.15
):
    # Observadores
    A = Observador(k=25, lambd=0.10)           # elástico
    B = Observador(k=5,  lambd=0.35)           # rígido
    C = Observador(k=20, lambd=0.20, adversarial=True)

    divergencias = []
    baseline = []

    for t in range(ciclos):
        ataque = ataque_inicio <= t <= ataque_fim
        O_t = meio_observado(ataque=ataque)

        rA = A.step(O_t)
        rB = B.step(O_t)
        rC = C.step(O_t)

        baseline.append(rA)  # referência operacional
        divergencias.append((
            rA != rB,
            rA != rC,
            rB != rC
        ))

    # Métricas globais
    instA = instabilidade(A.realidade)
    instB = instabilidade(B.realidade)
    instC = instabilidade(C.realidade)

    divAB = divergencia(A.realidade, B.realidade)
    divAC = divergencia(A.realidade, C.realidade)
    divBC = divergencia(B.realidade, C.realidade)

    # Reconvergência após ataque
    reconv_start = ataque_fim + 1
    Tr = None
    for i in range(reconv_start, ciclos):
        window = list(zip(A.realidade[i-20:i], B.realidade[i-20:i]))
        if window:
            d = sum(1 for x, y in window if x != y) / len(window)
            if d < limiar_reconvergencia:
                Tr = i - reconv_start
                break

    # Qualidade da reconvergência (B vs baseline A)
    Qr = divergencia(A.realidade[reconv_start:], B.realidade[reconv_start:])

    return {
        "Instabilidade": {"A": instA, "B": instB, "C": instC},
        "Divergencia": {"A_B": divAB, "A_C": divAC, "B_C": divBC},
        "Reconvergencia": {
            "Tempo_Tr": Tr,
            "Qualidade_Qr": Qr
        }
    }

# ---------------------------
# Execução
# ---------------------------
if __name__ == "__main__":
    r = experimento_C1()
    print("🧪 CMR–C1 — Reconvergência Espontânea\n")
    print("Instabilidade:")
    for k, v in r["Instabilidade"].items():
        print(f"  {k}: {v:.3f}")

    print("\nDivergência:")
    for k, v in r["Divergencia"].items():
        print(f"  {k}: {v:.3f}")

    print("\nReconvergência:")
    Tr = r["Reconvergencia"]["Tempo_Tr"]
    Qr = r["Reconvergencia"]["Qualidade_Qr"]
    print(f"  Tempo de Reconvergência (Tr): {Tr}")
    print(f"  Qualidade da Reconvergência (Qr): {Qr:.3f}")
