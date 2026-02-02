import random
import math

# =========================
# CONFIGURAÇÃO DO TESTE
# =========================

# Ângulos padrão de máxima violação CHSH
ANGULOS_A = [0, math.pi / 2]
ANGULOS_B = [math.pi / 4, -math.pi / 4]

RODADAS = 20000


# =========================
# CAMPO / MEIO CMR
# =========================

def correlacao_global(theta_a, theta_b):
    """
    Geometria do meio.
    NÃO é estado.
    NÃO é sinal.
    É estrutura global sustentada.
    """
    return math.cos(theta_a - theta_b)


def experimento(theta_a, theta_b):
    """
    Materialização local contingente,
    correlação global garantida pelo meio.
    """
    E = correlacao_global(theta_a, theta_b)

    # Probabilidade correta de resultados iguais
    p_same = (1 + E) / 2

    r = random.choice([1, -1])

    if random.random() < p_same:
        # mesmos resultados
        return r, r
    else:
        # resultados opostos
        return r, -r


# =========================
# EXECUÇÃO DO EXPERIMENTO
# =========================

def rodar():
    resultados = {}

    for a in ANGULOS_A:
        for b in ANGULOS_B:
            soma = 0
            for _ in range(RODADAS):
                ra, rb = experimento(a, b)
                soma += ra * rb
            resultados[(a, b)] = soma / RODADAS

    # Cálculo CHSH
    S = (
        resultados[(ANGULOS_A[0], ANGULOS_B[0])] +
        resultados[(ANGULOS_A[0], ANGULOS_B[1])] +
        resultados[(ANGULOS_A[1], ANGULOS_B[0])] -
        resultados[(ANGULOS_A[1], ANGULOS_B[1])]
    )

    print("\n📊 Correlações observadas:")
    for (a, b), v in resultados.items():
        print(f"A={a:.3f}  B={b:.3f}  →  E={v:.3f}")

    print("\n🔢 CHSH S =", round(S, 3))

    if abs(S) > 2:
        print("❗ Violação de Bell")
    else:
        print("✔ Dentro do limite clássico")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    rodar()
