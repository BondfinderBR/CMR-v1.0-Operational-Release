import random
import math
import statistics

# ---------- MEIO ----------
def meio_observado():
    estado_latente = random.choice([-1, 1])
    ruido = random.gauss(0, 1.2)
    return estado_latente + ruido


def decide(x):
    return 1 if x >= 0 else -1


# ---------- OPERADOR DE MEMÓRIA ----------
def operador_memoria(buffer, lambd):
    pesos = [math.exp(-lambd * i) for i in range(len(buffer))]
    Z = sum(pesos)
    return sum(buffer[i] * pesos[i] for i in range(len(buffer))) / Z


# ---------- OBSERVADOR ----------
def observador(amostras, k, lambd):
    buffer = []
    realidade = []

    for _ in range(amostras):
        O_t = meio_observado()
        buffer.insert(0, O_t)

        if len(buffer) > k:
            buffer.pop()

        psi = operador_memoria(buffer, lambd)
        realidade.append(decide(psi))

    return realidade


# ---------- INTERFERÊNCIA ----------
def interferencia(amostras=400):
    # Política A: rígida
    A = observador(amostras, k=3, lambd=0.6)

    # Política B: elástica
    B = observador(amostras, k=25, lambd=0.1)

    combinada = [a + b for a, b in zip(A, B)]

    return A, B, combinada


# ---------- MÉTRICAS ----------
def instabilidade(seq):
    return sum(1 for i in range(1, len(seq)) if seq[i] != seq[i-1]) / len(seq)


def divergencia(A, B):
    return sum(1 for a, b in zip(A, B) if a != b) / len(A)


# ---------- EXECUÇÃO ----------
A, B, C = interferencia()

print("🧪 CMR–A2 — INTERFERÊNCIA OPERACIONAL\n")

print("Instabilidade Política A (rígida): ", instabilidade(A))
print("Instabilidade Política B (elástica):", instabilidade(B))
print("Divergência A vs B:               ", divergencia(A, B))

# Oscilação da combinação
variancia = statistics.pvariance(C)
print("Variância da combinação (interferência):", variancia)
