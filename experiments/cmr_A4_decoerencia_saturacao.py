import random
import math

# -------------------------------
# Meio (inalterado)
# -------------------------------
def meio_observado():
    estado_latente = random.choice([-1, 1])
    ruido = random.gauss(0, 1.5)
    return estado_latente + ruido


def decide(valor):
    return 1 if valor >= 0 else -1


# -------------------------------
# Políticas
# -------------------------------
def politica_rigida(valor):
    return decide(valor)


def politica_elastica(buffer, lambd=0.15):
    pesos = [math.exp(-lambd * i) for i in range(len(buffer))]
    Z = sum(pesos)
    return sum(buffer[i] * pesos[i] for i in range(len(buffer))) / Z


# -------------------------------
# Métricas
# -------------------------------
def variancia(seq):
    media = sum(seq) / len(seq)
    return sum((x - media) ** 2 for x in seq) / len(seq)


# -------------------------------
# Teste A4
# -------------------------------
def teste_A4(amostras=300):
    buffer_B = []
    resultados = []

    for peso_A in [i / 10 for i in range(0, 11)]:
        combinados = []

        for _ in range(amostras):
            O_t = meio_observado()

            A = politica_rigida(O_t)

            buffer_B.insert(0, O_t)
            if len(buffer_B) > 20:
                buffer_B.pop()

            B_val = politica_elastica(buffer_B)
            B = decide(B_val)

            combinado = peso_A * A + (1 - peso_A) * B
            combinados.append(combinado)

        resultados.append((peso_A, variancia(combinados)))

    return resultados


# -------------------------------
# Execução
# -------------------------------
print("🧪 CMR–A4 — DECOERÊNCIA COMO SATURAÇÃO\n")

dados = teste_A4()
for peso, var in dados:
    print(f"Peso política rígida: {peso:.1f} | Variância (interferência): {var:.4f}")
