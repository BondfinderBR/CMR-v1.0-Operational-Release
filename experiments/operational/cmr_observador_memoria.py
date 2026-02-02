import random
from collections import deque

# =========================
# CONFIGURAÇÃO
# =========================

RODADAS = 5000
JANELA_MEMORIA = 25   # tamanho da memória temporal

def materializar():
    """
    Não existe valor real.
    Cada leitura é contingente.
    """
    return random.choice([1, -1])


class ObservadorSemMemoria:
    def __init__(self):
        self.ultimo = None
        self.mudancas = 0

    def observar(self):
        atual = materializar()
        if self.ultimo is not None and atual != self.ultimo:
            self.mudancas += 1
        self.ultimo = atual


class ObservadorComMemoria:
    def __init__(self, janela):
        self.memoria = deque(maxlen=janela)
        self.estado_estavel = None
        self.mudancas = 0

    def observar(self):
        leitura = materializar()
        self.memoria.append(leitura)

        # estado percebido = maioria na memória
        contagem = sum(self.memoria)
        percebido = 1 if contagem >= 0 else -1

        if self.estado_estavel is not None and percebido != self.estado_estavel:
            self.mudancas += 1

        self.estado_estavel = percebido


def rodar():
    sem_memoria = ObservadorSemMemoria()
    com_memoria = ObservadorComMemoria(JANELA_MEMORIA)

    for _ in range(RODADAS):
        sem_memoria.observar()
        com_memoria.observar()

    print("\n🧠 TESTE DO OBSERVADOR COM MEMÓRIA")
    print(f"Rodadas: {RODADAS}")
    print(f"Janela de memória: {JANELA_MEMORIA}\n")

    print("🔹 Sem memória")
    print("Mudanças percebidas:", sem_memoria.mudancas)
    print("Taxa de instabilidade:",
          round(sem_memoria.mudancas / RODADAS, 3))

    print("\n🔹 Com memória")
    print("Mudanças percebidas:", com_memoria.mudancas)
    print("Taxa de instabilidade:",
          round(com_memoria.mudancas / RODADAS, 3))


if __name__ == "__main__":
    rodar()
