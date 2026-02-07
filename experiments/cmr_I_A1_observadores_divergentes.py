import random
import math
import statistics

# =========================
# Parâmetros do experimento
# =========================

STEPS = 300

# Ruído dos sensores (metros)
RADAR_A_NOISE = 20      # preciso, lento
RADAR_B_NOISE = 60      # menos preciso, rápido
ADSB_NOISE    = 120     # ruidoso

# =========================
# Trajetória real (oculta)
# =========================

def true_trajectory(t):
    """
    Trajetória verdadeira da aeronave (nunca observada diretamente)
    Movimento quase linear com leve variação.
    """
    x = 1000 + 5 * t + 20 * math.sin(t / 25)
    y = 2000 + 3 * t + 15 * math.cos(t / 30)
    z = 10000
    return (x, y, z)

# =========================
# Sensores (observadores)
# =========================

def observe(position, noise):
    return tuple(
        coord + random.gauss(0, noise)
        for coord in position
    )

# =========================
# Métrica de divergência
# =========================

def distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

# =========================
# Execução do experimento
# =========================

radarA = []
radarB = []
adsb   = []

for t in range(STEPS):
    real_pos = true_trajectory(t)

    radarA.append(observe(real_pos, RADAR_A_NOISE))
    radarB.append(observe(real_pos, RADAR_B_NOISE))
    adsb.append(observe(real_pos, ADSB_NOISE))

# =========================
# Análise
# =========================

div_AB = [distance(a, b) for a, b in zip(radarA, radarB)]
div_AC = [distance(a, c) for a, c in zip(radarA, adsb)]
div_BC = [distance(b, c) for b, c in zip(radarB, adsb)]

print("🧪 CMR–I-A1 — OBSERVADORES DIVERGENTES\n")

print(f"Divergência média Radar A vs Radar B : {statistics.mean(div_AB):.2f} m")
print(f"Divergência média Radar A vs ADS-B   : {statistics.mean(div_AC):.2f} m")
print(f"Divergência média Radar B vs ADS-B   : {statistics.mean(div_BC):.2f} m")

print("\n📌 Interpretação CMR:")
print("- Não existe posição única verdadeira acessível.")
print("- Observadores divergem significativamente.")
print("- Divergência não implica falha operacional.")
