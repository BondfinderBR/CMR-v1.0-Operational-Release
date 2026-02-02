import random
from collections import deque

RODADAS = 5000
JANELA_MEMORIA = 50
PRESSAO = 0.9


def materializar():
    return random.choice([1, -1])


class Observador:
    def __init__(self, vies):
        self.memoria = deque([vies]*JANELA_MEMORIA, maxlen=JANELA_MEMORIA)
        self.estado = vies

    def observar(self, imposto):
        if random.random() < PRESSAO:
            leitura = imposto
        else:
            leitura = materializar()

        self.memoria.append(leitura)
        self.estado = 1 if sum(self.memoria) >= 0 else -1


def rodar():
    A = Observador(1)
    B = Observador(-1)

    convergiram = 0

    for _ in range(RODADAS):
        A.observar(imposto=1)
        B.observar(imposto=1)
        if A.estado == B.estado:
            convergiram += 1

    print("\n⚠️ TESTE DE CONVERGÊNCIA FORÇADA")
    print("Taxa de convergência:", round(convergiram / RODADAS, 3))


if __name__ == "__main__":
    rodar()
