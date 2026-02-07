import random
import math
import statistics

STEPS = 300
SEPARATION_LIMIT = 500  # metros

# Ruído dos sensores
RADAR_A_NOISE = 20
RADAR_B_NOISE = 60
ADSB_NOISE    = 120

def true_trajectory_A(t):
    return (1000 + 5*t, 2000 + 2*t, 10000)

def true_trajectory_B(t):
    return (1500 + 5*t, 2000 + 2*t, 10000)

def observe(pos, noise):
    return tuple(p + random.gauss(0, noise) for p in pos)

def distance(p1, p2):
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

# =========================
# Execução
# =========================

rigid_conflicts = 0
cmr_conflicts = 0

for t in range(STEPS):
    # posições reais (ocultas)
    realA = true_trajectory_A(t)
    realB = true_trajectory_B(t)

    # observações
    obsA_radarA = observe(realA, RADAR_A_NOISE)
    obsB_radarA = observe(realB, RADAR_A_NOISE)

    obsA_all = [
        observe(realA, RADAR_A_NOISE),
        observe(realA, RADAR_B_NOISE),
        observe(realA, ADSB_NOISE)
    ]
    obsB_all = [
        observe(realB, RADAR_A_NOISE),
        observe(realB, RADAR_B_NOISE),
        observe(realB, ADSB_NOISE)
    ]

    # 🔒 Alinhamento rígido
    if distance(obsA_radarA, obsB_radarA) < SEPARATION_LIMIT:
        rigid_conflicts += 1

    # 🔓 Concessão relacional (pior caso)
    worst_case_distance = min(
        distance(a, b)
        for a in obsA_all
        for b in obsB_all
    )

    if worst_case_distance < SEPARATION_LIMIT:
        cmr_conflicts += 1

# =========================
# Resultados
# =========================

print("🧪 CMR–I-A2 — ALINHAMENTO VS CONCESSÃO\n")

print(f"Conflitos detectados (alinhamento rígido): {rigid_conflicts}")
print(f"Conflitos detectados (concessão CMR):     {cmr_conflicts}")

print("\n📌 Interpretação CMR:")
print("- Alinhamento rígido ignora incerteza.")
print("- Concessão aceita divergência e age com margem.")
print("- Segurança emerge da cautela relacional, não da certeza.")
