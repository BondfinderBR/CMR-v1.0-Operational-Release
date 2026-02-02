import random
from collections import deque

RODADAS = 5000
JANELA_MEMORIA = 25
INFLUENCIA = 0.6  # 0.0 = nenhuma, 1.0 = total


def materializar():
    return random.choice([1, -1])


class Observador:
    def __init__(self, vies):
        self.memoria = deque(maxlen=JANELA_MEMORIA)
        self.vies = vies
        self.estado = None
        self.mudancas = 0

    def observar(self, narrativa_externa=None):
        leitura = materializar()

        if narrativa_externa and random.random() < INFLUENCIA:
            leitura = narrativa_externa

        self.memoria.append(leitura)
        percebido = 1 if sum(self.memoria) >= 0 else -1

        if self.estado is not None and percebido != self.estado:
            self.mudancas += 1

        self.estado = percebido
        return self.estado


def rodar():
    autoridade = Observador(vies=1)
    seguidor = Observador(vies=-1)

    colapsos = 0

    for _ in range(RODADAS):
        estado_aut = autoridade.observar()
        estado_seg = seguidor.observar(narrativa_externa=estado_aut)

        if estado_aut == estado_seg:
            colapsos += 1

    print("\n👑 TESTE DE AUTORIDADE NARRATIVA")
    print("Taxa de alinhamento:", round(colapsos / RODADAS, 3))
    print("Mudanças seguidor:", seguidor.mudancas)


if __name__ == "__main__":
    rodar()
