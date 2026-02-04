import random
import math
import statistics

# ----------------------------
# Meio observado (estado + ruído)
# ----------------------------
def meio_observado():
    S = random.choice([-1, 1])
    ruido = random.gauss(0, 1.2)
    return S + ruido

# ----------------------------
# Operador de memória
# ----------------------------
def operador_memoria(buffer, lambd):
    pesos = [math.exp(-lambd * i) for i in range(len(buffer))]
    Z = sum(pesos)
    return sum(buffer[i] * pesos[i] for i in range(len(buffer))) / Z

# ----------------------------
# Decisão observacional
# ----------------------------
def decide(x):
    return 1 if x >= 0 else -1

# ----------------------------
# Simulação com ruptura
# ----------------------------
def simular(ruptura, memoria, lambd=0.15, amostras=300):
    buffer = []
    realidade = []

    for t in range(amostras):
        O = meio_observado()

        # aplica ruptura probabilística
        if random.random() < ruptura:
            O *= -1

        buffer.insert(0, O)
        if len(buffer) > memoria:
            buffer.pop()

        psi = operador_memoria(buffer, lambd)
        realidade.append(decide(psi))

    return realidade

# ----------------------------
# Métrica de instabilidade
# ----------------------------
def instabilidade(realidade):
    mudancas = sum(
        1 for i in range(1, len(realidade))
        if realidade[i] != realidade[i - 1]
    )
    return mudancas / len(realidade)

# ----------------------------
# Classificação de regime
# ----------------------------
def classificar(instab):
    if instab < 0.05:
        return "RÍGIDO"
    elif instab < 0.15:
        return "ELÁSTICO"
    else:
        return "INSTÁVEL"

# ----------------------------
# Experimento E3c
# ----------------------------
rupturas = [0.05, 0.1, 0.2, 0.4, 0.6, 0.8]
memorias = [5, 10, 20, 40]

print("🧪 CMR–E3c — MAPA DE REGIMES\n")

for r in rupturas:
    for m in memorias:
        real = simular(r, m)
        instab = instabilidade(real)
        regime = classificar(instab)

        print(
            f"Ruptura={r:.2f} | Memória={m:>2} "
            f"| Instabilidade={instab:.3f} "
            f"| Regime={regime}"
        )

print("\n🏁 FIM DO TESTE E3c")
