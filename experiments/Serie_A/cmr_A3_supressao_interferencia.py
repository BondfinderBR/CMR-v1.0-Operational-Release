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
# Políticas observacionais
# -------------------------------
def politica_rigida(valor):
    return decide(valor)


def politica_elastica(buffer, lambd=0.2):
    pesos = [math.exp(-lambd * i) for i in range(len(buffer))]
    Z = sum(pesos)
    return sum(buffer[i] * pesos[i] for i in range(len(buffer))) / Z


# -------------------------------
# Teste A3
# -------------------------------
def teste_A3(amostras=300, peso_A=0.85):
    buffer_B = []
    resultados_A = []
    resultados_B = []
    combinados = []

    for _ in range(amostras):
        O_t = meio_observado()

        # Política A (rígida)
        A = politica_rigida(O_t)

        # Política B (elástica)
        buffer_B.insert(0, O_t)
        if len(buffer_B) > 20:
            buffer_B.pop()
        B_val = politica_elastica(buffer_B)
        B = decide(B_val)

        # Combinação com política dominante
        combinado = peso_A * A + (1 - peso_A) * B
        combinados.append(combinado)

        resultados_A.append(A)
        resultados_B.append(B)

    return resultados_A, resultados_B, combinados


# -------------------------------
# Métricas
# -------------------------------
def instabilidade(seq):
    return sum(seq[i] != seq[i-1] for i in range(1, len(seq))) / len(seq)


def variancia(seq):
    media = sum(seq) / len(seq)
    return sum((x - media) ** 2 for x in seq) / len(seq)


# -------------------------------
# Execução
# -------------------------------
A, B, C = teste_A3()

print("🧪 CMR–A3 — SUPRESSÃO DE INTERFERÊNCIA\n")
print(f"Instabilidade Política A (rígida):  {instabilidade(A):.3f}")
print(f"Instabilidade Política B (elástica): {instabilidade(B):.3f}")
print(f"Divergência A vs B:                {sum(a!=b for a,b in zip(A,B))/len(A):.3f}")
print(f"Variância da combinação:           {variancia(C):.4f}")
