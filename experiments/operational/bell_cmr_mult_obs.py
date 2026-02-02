import random
import math

RODADAS = 10000
ANGULO = math.pi / 4


def materializar():
    return random.choice([1, -1])


def rodar():
    divergencias = 0

    for _ in range(RODADAS):
        A1 = materializar()
        A2 = materializar()

        if A1 != A2:
            divergencias += 1

    print("\n👁️👁️ Observadores no mesmo ponto")
    print("Divergência:", divergencias / RODADAS)


if __name__ == "__main__":
    rodar()
