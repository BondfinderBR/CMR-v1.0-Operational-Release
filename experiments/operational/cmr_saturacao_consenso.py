import random
from collections import Counter

# =========================
# CONFIGURAÇÃO
# =========================

OBSERVADORES = [1, 10, 100, 1000, 10000]
RODADAS = 100

FORCA_MEIO = 1.0   # meio forte, mas sem verdade objetiva


def materializar():
    """
    Não existe valor real.
    Cada observador materializa localmente.
    """
    return random.choice([1, -1])


def rodar():
    print("\n🧪 TESTE DE SATURAÇÃO DE CONSENSO\n")

    for N in OBSERVADORES:
        divergencias = []

        for _ in range(RODADAS):
            leituras = [materializar() for _ in range(N)]
            contagem = Counter(leituras)

            maioria = contagem.most_common(1)[0][0]
            minoria = contagem.most_common()[-1][1]

            divergencias.append(minoria / N)

        media_div = sum(divergencias) / len(divergencias)

        print(f"Observadores: {N:6d} | "
              f"Divergência média: {media_div:.4f}")


if __name__ == "__main__":
    rodar()
