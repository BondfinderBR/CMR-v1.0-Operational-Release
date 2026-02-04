# CMR–D5 — Auto-referência
# Processo que integra a si mesmo
# Autor: Flávio Oliveira

import random
import math
import statistics

# ===============================
# PROCESSO AUTO-REFERENTE
# ===============================

class ProcessoAutoReferente:
    def __init__(self, k=30, lambd=0.2, alpha=0.7):
        """
        k      : tamanho da memória
        lambd  : taxa de esquecimento
        alpha  : peso da auto-referência (0 < alpha < 1)
        """
        self.k = k
        self.lambd = lambd
        self.alpha = alpha
        self.buffer = []
        self.trajetoria = []

    def passo(self, entrada):
        # entrada externa mínima
        self.buffer.insert(0, entrada)
        if len(self.buffer) > self.k:
            self.buffer.pop()

        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)

        integrado = sum(self.buffer[i] * pesos[i] for i in range(len(self.buffer))) / Z

        # auto-referência: mistura do integrado anterior
        if self.trajetoria:
            estado = self.alpha * self.trajetoria[-1] + (1 - self.alpha) * integrado
        else:
            estado = integrado

        self.trajetoria.append(estado)
        return estado

# ===============================
# MÉTRICAS
# ===============================

def variancia(seq):
    if len(seq) < 2:
        return 0
    return statistics.variance(seq)

def deriva(seq):
    diffs = [abs(seq[i] - seq[i-1]) for i in range(1, len(seq))]
    return statistics.mean(diffs)

def ciclicidade(seq):
    # mede repetição aproximada
    if len(seq) < 20:
        return 0
    return abs(statistics.mean(seq[-10:]) - statistics.mean(seq[-20:-10]))

# ===============================
# EXPERIMENTO D5
# ===============================

def experimento_D5(passos=800):
    P = ProcessoAutoReferente(k=40, lambd=0.15, alpha=0.85)

    # fase inicial: ruído mínimo só para iniciar
    for _ in range(20):
        P.passo(random.gauss(0, 0.5))

    # fase principal: quase sem mundo externo
    for _ in range(passos):
        P.passo(0.0)

    var = variancia(P.trajetoria)
    der = deriva(P.trajetoria)
    cyc = ciclicidade(P.trajetoria)

    print("\n🌀 CMR–D5 — AUTO-REFERÊNCIA\n")
    print(f"Variância da trajetória: {var:.3f}")
    print(f"Deriva média: {der:.3f}")
    print(f"Índice de ciclicidade: {cyc:.3f}")

    if der < 0.2 and cyc < 0.1:
        print("\n✅ Processo auto-referente funcional")
    elif cyc >= 0.1:
        print("\n⚠️ Ciclo auto-referente detectado")
    else:
        print("\n❌ Colapso ou divergência")

# ===============================
# EXECUÇÃO
# ===============================

if __name__ == "__main__":
    experimento_D5()
