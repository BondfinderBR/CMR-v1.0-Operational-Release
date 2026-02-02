import random
import math

ANGULOS_A = [0, math.pi / 2]
ANGULOS_B = [math.pi / 4, -math.pi / 4]

RODADAS = 20000
FORCA_MEIO = 0.6  # ← teste: 1.0, 0.6, 0.3, 0.0


def correlacao_global(theta_a, theta_b):
    return math.cos(theta_a - theta_b)


def experimento(theta_a, theta_b):
    E = correlacao_global(theta_a, theta_b)

    # meio fraco: mistura correlação com ruído
    E_eff = FORCA_MEIO * E

    p_same = (1 + E_eff) / 2
    r = random.choice([1, -1])

    if random.random() < p_same:
        return r, r
    else:
        return r, -r


def rodar():
    resultados = {}

    for a in ANGULOS_A:
        for b in ANGULOS_B:
            soma = 0
            for _ in range(RODADAS):
                ra, rb = experimento(a, b)
                soma += ra * rb
            resultados[(a, b)] = soma / RODADAS

    S = (
        resultados[(ANGULOS_A[0], ANGULOS_B[0])] +
        resultados[(ANGULOS_A[0], ANGULOS_B[1])] +
        resultados[(ANGULOS_A[1], ANGULOS_B[0])] -
        resultados[(ANGULOS_A[1], ANGULOS_B[1])]
    )

    print("\n🔻 FORÇA DO MEIO =", FORCA_MEIO)
    print("CHSH S =", round(S, 3))


if __name__ == "__main__":
    rodar()
