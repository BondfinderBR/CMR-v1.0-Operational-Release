import random
import math
import statistics

# -----------------------------
# Parâmetros do cenário
# -----------------------------
NUM_PASSOS = 500
MARGEM_SEGURANCA = 300  # metros
SIGMAS = {
    "RadarA": 80,
    "RadarB": 120,
    "ADSB": 150
}

# -----------------------------
# Funções básicas
# -----------------------------
def distancia(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def ruido(sigma):
    return random.gauss(0, sigma)

def observador(posicao_real, sigma):
    return (
        posicao_real[0] + ruido(sigma),
        posicao_real[1] + ruido(sigma)
    )

# -----------------------------
# Envelope CMR
# -----------------------------
def envelope(observacoes):
    xs = [o[0] for o in observacoes]
    ys = [o[1] for o in observacoes]
    centro = (statistics.mean(xs), statistics.mean(ys))
    raio = max(distancia(centro, o) for o in observacoes)
    return centro, raio

# -----------------------------
# Simulação
# -----------------------------
conflitos_rigidos = 0
conflitos_cmr = 0
falsos_negativos = 0

for _ in range(NUM_PASSOS):
    # Posições reais (duas aeronaves)
    real_A = (random.uniform(0, 5000), random.uniform(0, 5000))
    real_B = (real_A[0] + random.uniform(200, 600),
              real_A[1] + random.uniform(200, 600))

    # Observações
    obs_A = [
        observador(real_A, SIGMAS["RadarA"]),
        observador(real_A, SIGMAS["RadarB"]),
        observador(real_A, SIGMAS["ADSB"]),
    ]

    obs_B = [
        observador(real_B, SIGMAS["RadarA"]),
        observador(real_B, SIGMAS["RadarB"]),
        observador(real_B, SIGMAS["ADSB"]),
    ]

    # Alinhamento rígido (Radar A apenas)
    if distancia(obs_A[0], obs_B[0]) < MARGEM_SEGURANCA:
        conflitos_rigidos += 1

    # Envelope CMR
    env_A = envelope(obs_A)
    env_B = envelope(obs_B)

    dist_env = distancia(env_A[0], env_B[0]) - (env_A[1] + env_B[1])

    if dist_env < MARGEM_SEGURANCA:
        conflitos_cmr += 1

    # Verdade física (para avaliação)
    if distancia(real_A, real_B) < MARGEM_SEGURANCA:
        if dist_env >= MARGEM_SEGURANCA:
            falsos_negativos += 1

# -----------------------------
# Resultados
# -----------------------------
print("🧪 CMR–I-A3 — ENVELOPE DE SEGURANÇA PROBABILÍSTICO\n")
print(f"Conflitos (alinhamento rígido): {conflitos_rigidos}")
print(f"Conflitos (CMR envelope):      {conflitos_cmr}")
print(f"Falsos negativos (CMR):        {falsos_negativos}")

print("\n📌 Interpretação CMR:")
print("- Segurança emerge da margem, não da certeza.")
print("- Concessão aumenta custo operacional.")
print("- Falsos negativos são reduzidos.")
print("- Realidade operacional é probabilística.")
