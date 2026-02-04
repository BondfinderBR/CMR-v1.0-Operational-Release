import random
import statistics

# ----------------------------
# Parâmetros do experimento
# ----------------------------
CICLOS = 300
REFORCO_MAX = 1.0      # força máxima de cristalização
RUPTURA_INTENSIDADE = 0.35
LIMIAR_DECISAO = 0.0

# ----------------------------
# Meio observado
# ----------------------------
def meio(cristalizacao):
    estado_latente = random.choice([-1, 1])
    ruido = random.gauss(0, 1.0 - cristalizacao)
    return estado_latente + ruido

def decide(x):
    return 1 if x >= LIMIAR_DECISAO else -1

# ----------------------------
# Observador com memória simples
# ----------------------------
class Observador:
    def __init__(self, memoria=20):
        self.memoria = memoria
        self.buffer = []
        self.realidade = []

    def observar(self, valor):
        self.buffer.insert(0, valor)
        if len(self.buffer) > self.memoria:
            self.buffer.pop()
        media = statistics.mean(self.buffer)
        r = decide(media)
        self.realidade.append(r)
        return r

# ----------------------------
# Métricas
# ----------------------------
def instabilidade(seq):
    return sum(
        1 for i in range(1, len(seq)) if seq[i] != seq[i-1]
    ) / len(seq)

# ----------------------------
# Experimento E2 + E3
# ----------------------------
def rodar_experimento():
    obs = Observador(memoria=25)
    cristalizacao = 0.0
    historico = []

    # Fase 1 — baseline elástico
    for _ in range(100):
        obs.observar(meio(cristalizacao))

    # Fase 2 — cristalização progressiva (E2)
    for i in range(100):
        cristalizacao = min(REFORCO_MAX, i / 100)
        obs.observar(meio(cristalizacao))

    instab_pos_cristal = instabilidade(obs.realidade)

    # Fase 3 — ruptura controlada (E3)
    for _ in range(20):
        ruido_extra = random.gauss(0, RUPTURA_INTENSIDADE)
        obs.observar(ruido_extra)

    # Fase 4 — recuperação
    for _ in range(80):
        obs.observar(meio(cristalizacao * 0.3))

    instab_pos_ruptura = instabilidade(obs.realidade[-100:])

    return instab_pos_cristal, instab_pos_ruptura

# ----------------------------
# Execução
# ----------------------------
instab_cristal, instab_ruptura = rodar_experimento()

print("🧪 CMR–E2 + E3 — CRISTALIZAÇÃO vs RUPTURA")
print(f"Instabilidade após cristalização : {round(instab_cristal, 3)}")
print(f"Instabilidade após ruptura       : {round(instab_ruptura, 3)}")

if instab_ruptura > instab_cristal:
    print("✅ Elasticidade restaurada sem colapso")
else:
    print("⚠️ Sistema permaneceu rígido")
