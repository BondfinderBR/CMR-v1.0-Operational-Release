import random
from collections import deque

RODADAS = 5000
RESET_EM = 2500
JANELA_MEMORIA = 25


def materializar():
    return random.choice([1, -1])


class Observador:
    def __init__(self):
        self.memoria = deque(maxlen=JANELA_MEMORIA)
        self.estado = None
        self.mudancas = 0

    def observar(self):
        leitura = materializar()
        self.memoria.append(leitura)

        percebido = 1 if sum(self.memoria) >= 0 else -1

        if self.estado is not None and percebido != self.estado:
            self.mudancas += 1

        self.estado = percebido

    def reset(self):
        self.memoria.clear()
        self.estado = None


def rodar():
    obs = Observador()

    for i in range(RODADAS):
        if i == RESET_EM:
            obs.reset()
        obs.observar()

    print("\n🔄 TESTE DE RESET DE MEMÓRIA")
    print("Mudanças percebidas:", obs.mudancas)


if __name__ == "__main__":
    rodar()
