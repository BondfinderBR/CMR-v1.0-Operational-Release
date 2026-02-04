import random
import statistics

# ----------------------------
# Parâmetros globais
# ----------------------------
CICLOS_BASELINE = 120
CICLOS_CRISTAL = 120
CICLOS_POS = 120

MEMORIA = 25
LIMIAR = 0.0

# Intensidades de ruptura a testar
RUPTURAS = [0.05, 0.10, 0.20, 0.30, 0.45, 0.60, 0.80]

# ----------------------------
# Funções base
# ----------------------------
def decide(x):
    return 1 if x >= LIMIAR else -1

def meio(cristalizacao):
    estado_latente = random.choice([-1, 1])
    ruido = random.gauss(0, max(0.05, 1.0 - cristalizacao))
    return estado_latente + ruido

class Observador:
    def __init__(self, memoria):
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

def instabilidade(seq):
    if len(seq) < 2:
        return 0.0
    return sum(
        1 for i in range(1, len(seq)) if seq[i] != seq[i-1]
    ) / len(seq)

# ----------------------------
# Experimento E3b
# ----------------------------
def rodar_E3b(intensidade_ruptura):
    obs = Observador(MEMORIA)
    cristalizacao = 0.0

    # Fase 1 — baseline elástico
    for _ in range(CICLOS_BASELINE):
        obs.observar(meio(cristalizacao))

    # Fase 2 — cristalização forte
    for _ in range(CICLOS_CRISTAL):
        cristalizacao = 0.9
        obs.observar(meio(cristalizacao))

    instab_cristal = instabilidade(obs.realidade[-60:])

    # Fase 3 — ruptura progressiva
    for _ in range(30):
        ruido_extra = random.gauss(0, intensidade_ruptura)
        obs.observar(ruido_extra)

    # Fase 4 — recuperação
    for _ in range(CICLOS_POS):
        obs.observar(meio(cristalizacao * 0.3))

    instab_pos = instabilidade(obs.realidade[-60:])

    # Classificação do regime
    if instab_pos < 0.05:
        regime = "RÍGIDO"
    elif instab_pos < 0.25:
        regime = "ELÁSTICO"
    else:
        regime = "COLAPSO"

    return instab_cristal, instab_pos, regime

# ----------------------------
# Execução
# ----------------------------
print("🧪 CMR–E3b — RUPTURA PROGRESSIVA\n")

for r in RUPTURAS:
    ic, ip, reg = rodar_E3b(r)
    print(
        f"Ruptura={r:.2f} | "
        f"Instab cristal={ic:.3f} | "
        f"Instab pós={ip:.3f} | "
        f"Regime final: {reg}"
    )
