import random
import math

# -------------------------
# Meio (estado + ruído)
# -------------------------
def meio():
    estado = random.choice([-1, 1])
    ruido = random.gauss(0, 1.2)
    return estado + ruido

# -------------------------
# Operador de memória
# -------------------------
def memoria(buffer, lambd):
    pesos = [math.exp(-lambd * i) for i in range(len(buffer))]
    Z = sum(pesos)
    return sum(buffer[i] * pesos[i] for i in range(len(buffer))) / Z

# -------------------------
# Decisão
# -------------------------
def decide(x):
    return 1 if x >= 0 else -1

# -------------------------
# Observador com política
# -------------------------
def observador(politica, passos=300):
    if politica == "rigida":
        k = 5
        lambd = 0.5
    else:  # elástica
        k = 30
        lambd = 0.1

    buffer = []
    realidade = []

    for t in range(passos):
        O = meio()
        buffer.insert(0, O)
        if len(buffer) > k:
            buffer.pop()

        psi = memoria(buffer, lambd)
        realidade.append(decide(psi))

        # mudança real do meio (simulada)
        if t == 150:
            for i in range(len(buffer)):
                buffer[i] *= -1

    return realidade

# -------------------------
# Métrica de instabilidade
# -------------------------
def instabilidade(r):
    return sum(1 for i in range(1, len(r)) if r[i] != r[i-1]) / len(r)

# -------------------------
# Execução
# -------------------------
rigida = observador("rigida")
elastica = observador("elastica")

print("Instabilidade (política rígida): ", instabilidade(rigida))
print("Instabilidade (política elástica):", instabilidade(elastica))
