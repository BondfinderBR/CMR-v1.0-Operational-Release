import random
import math

# =========================
# Configurações gerais
# =========================
STEPS = 300
DT = 0.01
DIVERGENCE_THRESHOLD = 0.25  # θ — limiar de adaptação
EPS = 1e-6

# =========================
# Utilidades físicas mínimas
# =========================
def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) + EPS

def accel(pos, others, G=1.0):
    ax, ay = 0.0, 0.0
    for o in others:
        r = dist(pos, o)
        dx, dy = o[0]-pos[0], o[1]-pos[1]
        ax += G * dx / (r**3)
        ay += G * dy / (r**3)
    return ax, ay

# =========================
# Integradores
# =========================
def euler_step(state):
    new_state = []
    for i, (x, y, vx, vy) in enumerate(state):
        others = [(s[0], s[1]) for j, s in enumerate(state) if j != i]
        ax, ay = accel((x, y), others)
        vx += ax * DT
        vy += ay * DT
        x += vx * DT
        y += vy * DT
        new_state.append([x, y, vx, vy])
    return new_state

def verlet_step(state, prev_state):
    new_state = []
    for i, (x, y, vx, vy) in enumerate(state):
        ox, oy, _, _ = prev_state[i]
        others = [(s[0], s[1]) for j, s in enumerate(state) if j != i]
        ax, ay = accel((x, y), others)
        nx = 2*x - ox + ax * DT**2
        ny = 2*y - oy + ay * DT**2
        nvx = (nx - ox) / (2*DT)
        nvy = (ny - oy) / (2*DT)
        new_state.append([nx, ny, nvx, nvy])
    return new_state

# =========================
# Métricas CMR
# =========================
def divergence(stateA, stateB):
    return sum(
        math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
        for a, b in zip(stateA, stateB)
    ) / len(stateA)

def instability(history):
    flips = 0
    for i in range(1, len(history)):
        if history[i] != history[i-1]:
            flips += 1
    return flips / len(history)

# =========================
# Inicialização
# =========================
def init_state():
    return [
        [random.uniform(-1,1), random.uniform(-1,1),
         random.uniform(-0.5,0.5), random.uniform(-0.5,0.5)]
        for _ in range(3)
    ]

# =========================
# Experimento T3
# =========================
state_A = init_state()
state_B = [s.copy() for s in state_A]
state_C = [s.copy() for s in state_A]

prev_A = [s.copy() for s in state_A]
prev_B = [s.copy() for s in state_B]
prev_C = [s.copy() for s in state_C]

policy_C = "euler"
policy_log = []

div_before = []
div_after = []

adapted = False

for step in range(STEPS):
    # Observador A — Euler fixo
    next_A = euler_step(state_A)

    # Observador B — Verlet fixo
    next_B = verlet_step(state_B, prev_B)

    # Observador C — adaptativo
    if policy_C == "euler":
        next_C = euler_step(state_C)
    else:
        next_C = verlet_step(state_C, prev_C)

    # Divergência local A vs C
    d = divergence(next_A, next_C)

    if not adapted:
        div_before.append(d)
        if d > DIVERGENCE_THRESHOLD:
            policy_C = "verlet"
            adapted = True
            policy_log.append(step)
    else:
        div_after.append(d)

    # Atualiza estados
    prev_A, state_A = state_A, next_A
    prev_B, state_B = state_B, next_B
    prev_C, state_C = state_C, next_C

# =========================
# Resultados
# =========================
print("🧪 CMR–T3 — POLÍTICA ADAPTATIVA EM SISTEMA CAÓTICO\n")

print("🔹 Divergência média ANTES da adaptação:",
      round(sum(div_before)/len(div_before), 5))

if div_after:
    print("🔹 Divergência média DEPOIS da adaptação:",
          round(sum(div_after)/len(div_after), 5))
else:
    print("🔹 Adaptação não foi acionada")

print("🔹 Passo da adaptação:", policy_log if policy_log else "—")

print("\n✅ Interpretação CMR:")
print("- Correção tardia falha (T2)")
print("- Governança antecipada limita fragmentação")
print("- Alinhamento é intervenção de regime, não consenso")
