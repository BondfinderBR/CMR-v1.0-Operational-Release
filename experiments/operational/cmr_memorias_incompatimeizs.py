import random
from collections import deque

# =========================
# CONFIGURAÇÃO
# =========================

RODADAS = 5000
JANELA_MEMORIA = 25

# viés inicial (história pessoal)
VIES_A = 1     # observa mais +1 no início
VIES_B = -1    # observa mais -1 no início
INTENSIDADE_VIES = 0.8   # quanto o passado pesa


def materializar():
    return random.choice([1, -1])


class ObservadorComMemoria:
    def __init__(self, janela, vies):
        self.memoria = deque(maxlen=janela)
        self.vies = vies
        self.estado_estavel = None
        self.mudancas = 0

    def observar(self):
        leitura = materializar()

        # aplica viés histórico
        if random.random() < INTENSIDADE_VIES:
            leitura = self.vies

        self.memoria.append(leitura)

        # estado percebido = maioria na memória
        soma = sum(self.memoria)
        percebido = 1 if soma >= 0 else -1

        if self.estado_estavel is not None and percebido != self.estado_estavel:
            self.mudancas += 1

        self.estado_estavel = percebido


def rodar():
    obs_A = ObservadorComMemoria(JANELA_MEMORIA, VIES_A)
    obs_B = ObservadorComMemoria(JANELA_MEMORIA, VIES_B)

    discordancias = 0

    for _ in range(RODADAS):
        obs_A.observar()
        obs_B.observar()

        if obs_A.estado_estavel != obs_B.estado_estavel:
            discordancias += 1

    print("\n🧠 TESTE DE MEMÓRIAS INCOMPATÍVEIS\n")
    print(f"Rodadas: {RODADAS}")
    print(f"Janela de memória: {JANELA_MEMORIA}")
    print(f"Viés A: {VIES_A} | Viés B: {VIES_B}\n")

    print("🔹 Observador A")
    print("Mudanças percebidas:", obs_A.mudancas)

    print("\n🔹 Observador B")
    print("Mudanças percebidas:", obs_B.mudancas)

    print("\n⚠️ Discordância entre realidades:",
          round(discordancias / RODADAS, 3))


if __name__ == "__main__":
    rodar()
