import random
import math
import statistics

# -----------------------------
# Meio com mudança súbita
# -----------------------------
def meio(t):
    if t < 50:
        return 100
    else:
        return 120  # mudança clara no meio

# -----------------------------
# Observador
# -----------------------------
class Observador:
    def __init__(self, ruido=2.0, memoria=20, colapso=False):
        self.ruido = ruido
        self.memoria = memoria
        self.colapso = colapso
        self.buffer = []

    def observa(self, v):
        o = v + random.gauss(0, self.ruido)
        self.buffer.insert(0, o)
        if len(self.buffer) > self.memoria:
            self.buffer.pop()

    def estimativa(self):
        if not self.buffer:
            return 0
        if self.colapso:
            # pesos aleatórios → presente fantasma
            pesos = [random.random() for _ in self.buffer]
        else:
            pesos = [math.exp(-0.15 * i) for i in range(len(self.buffer))]

        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

# -----------------------------
# Execução do teste
# -----------------------------
def teste_presente_fantasma():
    A = Observador(colapso=False)
    B = Observador(colapso=True)

    respostas_A = []
    respostas_B = []

    for t in range(100):
        v = meio(t)
        A.observa(v)
        B.observa(v)
        respostas_A.append(A.estimativa())
        respostas_B.append(B.estimativa())

    # capacidade de resposta após mudança
    resposta_A = abs(statistics.mean(respostas_A[60:]) -
                     statistics.mean(respostas_A[40:50]))
    resposta_B = abs(statistics.mean(respostas_B[60:]) -
                     statistics.mean(respostas_B[40:50]))

    print("🧪 CMR–T′5 — DETECTOR DE PRESENTE FANTASMA\n")
    print(f"Resposta Observador A (normal):   {resposta_A:.2f}")
    print(f"Resposta Observador B (fantasma): {resposta_B:.2f}")

    print("\n📌 Interpretação CMR:")
    print("- Baixa resposta indica colapso do presente.")
    print("- Estabilidade não implica adaptação.")
    print("- Presente fantasma é detectável por inércia temporal.")

teste_presente_fantasma()
