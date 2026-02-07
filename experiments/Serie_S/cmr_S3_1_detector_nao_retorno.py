# ============================================
# CMR–S3.1 — DETECTOR DE PONTO DE NÃO RETORNO
# Autor: Flávio Oliveira
# Framework: CMR v1.x
# ============================================

import random
import math
import statistics

# -----------------------------
# Parâmetros globais
# -----------------------------
ITERACOES = 200
LIMITE_COLAPSO = 1.0        # Divergência acima disso = colapso
JANELA_ALERTA = 10          # Janela mínima para detector operar
TENDENCIA_MIN = 0.04        # Inclinação mínima para disparar alerta

# -----------------------------
# Meio relacional (estável)
# -----------------------------
def meio_latente(t):
    # Meio estável, sem choque externo
    return math.sin(t / 20)

# -----------------------------
# Observador CMR
# -----------------------------
class Observador:
    def __init__(self, ruido=0.6, memoria=8, lambd=0.15):
        self.ruido = ruido
        self.memoria = memoria
        self.lambd = lambd
        self.buffer = []

    def observa(self, valor):
        o = valor + random.gauss(0, self.ruido)
        self.buffer.insert(0, o)
        if len(self.buffer) > self.memoria:
            self.buffer.pop()
        return o

    def estimativa(self):
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        return sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

# -----------------------------
# Detector de tendência
# -----------------------------
def tendencia(lista):
    if len(lista) < 2:
        return 0
    diffs = [lista[i] - lista[i-1] for i in range(1, len(lista))]
    return statistics.mean(diffs)

# -----------------------------
# Execução principal
# -----------------------------
def executar_teste():
    A = Observador(ruido=0.6, memoria=10)
    B = Observador(ruido=0.9, memoria=4)

    divergencias = []

    tempo_alerta = None
    tempo_colapso = None

    for t in range(ITERACOES):
        v = meio_latente(t)

        A.observa(v)
        B.observa(v)

        pA = A.estimativa()
        pB = B.estimativa()

        D = abs(pA - pB)
        divergencias.append(D)

        # -----------------------------
        # DETECTOR DE ALERTA (tendência)
        # -----------------------------
        if t >= JANELA_ALERTA and tempo_alerta is None:
            incl = tendencia(divergencias[-JANELA_ALERTA:])
            if incl > TENDENCIA_MIN:
                tempo_alerta = t

        # -----------------------------
        # COLAPSO (somente após nascer)
        # -----------------------------
        if t >= JANELA_ALERTA and D > LIMITE_COLAPSO and tempo_colapso is None:
            tempo_colapso = t
            break

    # -----------------------------
    # Relatório
    # -----------------------------
    print("🧪 CMR–S3.1 — DETECTOR DE NÃO RETORNO\n")

    print(f"Tempo do ALERTA     : {tempo_alerta}")
    print(f"Tempo do COLAPSO    : {tempo_colapso}")

    if tempo_alerta is not None and tempo_colapso is not None:
        print(f"Antecedência do alerta: {tempo_colapso - tempo_alerta} ciclos")
    else:
        print("Antecedência do alerta: —")

    print("\n📌 Interpretação CMR:")
    print("- O detector monitora tendência, não valor absoluto.")
    print("- O colapso é precedido por sinais fracos quando é dinâmico.")
    print("- Sistemas que colapsam antes da janela são estruturalmente inviáveis.")
    print("- Soberania efetiva é temporal, não autoritária.")

# -----------------------------
# Rodar
# -----------------------------
if __name__ == "__main__":
    executar_teste()
