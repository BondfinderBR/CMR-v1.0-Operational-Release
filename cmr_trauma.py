import random
from collections import deque

RODADAS = 5000
JANELA_MEMORIA = 50
RIGIDEZ = 0.95  # quanto menos atualiza


def materializar():
    return random.choice([1, -1])


class ObservadorTraumatizado:
    def __init__(self, vies):
        self.memoria = deque([vies]*JANELA_MEMORIA, maxlen=JANELA_MEMORIA)
        self.estado = vies
        self.mudancas = 0

    def observar(self):
        if random.random() > RIGIDEZ:
            self.memoria.append(materializar())

        percebido = 1 if sum(self.memoria) >= 0 else -1

        if percebido != self.estado:
            self.mudancas += 1

        self.estado = percebido


def rodar():
    obs = ObservadorTraumatizado(vies=1)

    for _ in range(RODADAS):
        obs.observar()

    print("\n🧠 TESTE DE TRAUMA")
    print("Mudanças percebidas:", obs.mudancas)


if __name__ == "__main__":
    rodar()
