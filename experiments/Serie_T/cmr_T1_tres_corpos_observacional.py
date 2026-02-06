import math
import copy
import statistics

G = 1.0
DT = 0.01
STEPS = 6000

# -----------------------------
# Sistema físico: 3 corpos
# -----------------------------
class Body:
    def __init__(self, m, x, y, vx, vy):
        self.m = m
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

def acceleration(bodies, i):
    ax = ay = 0.0
    bi = bodies[i]
    for j, bj in enumerate(bodies):
        if i == j:
            continue
        dx = bj.x - bi.x
        dy = bj.y - bi.y
        r2 = dx*dx + dy*dy + 1e-9
        r = math.sqrt(r2)
        a = G * bj.m / r2
        ax += a * dx / r
        ay += a * dy / r
    return ax, ay

# -----------------------------
# Observador A — Velocity Verlet
# -----------------------------
def step_verlet(bodies):
    acc = [acceleration(bodies, i) for i in range(len(bodies))]
    for i, b in enumerate(bodies):
        b.x += b.vx * DT + 0.5 * acc[i][0] * DT * DT
        b.y += b.vy * DT + 0.5 * acc[i][1] * DT * DT

    acc_new = [acceleration(bodies, i) for i in range(len(bodies))]
    for i, b in enumerate(bodies):
        b.vx += 0.5 * (acc[i][0] + acc_new[i][0]) * DT
        b.vy += 0.5 * (acc[i][1] + acc_new[i][1]) * DT

# -----------------------------
# Observador B — Euler explícito
# -----------------------------
def step_euler(bodies):
    acc = [acceleration(bodies, i) for i in range(len(bodies))]
    for i, b in enumerate(bodies):
        b.vx += acc[i][0] * DT
        b.vy += acc[i][1] * DT
        b.x += b.vx * DT
        b.y += b.vy * DT

# -----------------------------
# Métricas CMR
# -----------------------------
def state_signature(bodies):
    # Assinatura simples: energia total aproximada
    kinetic = sum(0.5*b.m*(b.vx*b.vx + b.vy*b.vy) for b in bodies)
    potential = 0.0
    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            dx = bodies[j].x - bodies[i].x
            dy = bodies[j].y - bodies[i].y
            r = math.sqrt(dx*dx + dy*dy) + 1e-9
            potential -= G * bodies[i].m * bodies[j].m / r
    return kinetic + potential

# -----------------------------
# Execução do teste
# -----------------------------
def run():
    # Condições iniciais idênticas
    init = [
        Body(1.0, -1.0, 0.0, 0.0, 0.6),
        Body(1.0,  1.0, 0.0, 0.0, -0.6),
        Body(1.0,  0.0, 0.5, -0.5, 0.0),
    ]

    A = copy.deepcopy(init)
    B = copy.deepcopy(init)

    sigA, sigB = [], []

    for _ in range(STEPS):
        step_verlet(A)
        step_euler(B)
        sigA.append(state_signature(A))
        sigB.append(state_signature(B))

    # Divergência observacional
    diffs = [abs(a - b) for a, b in zip(sigA, sigB)]

    # Instabilidade interna (mudanças bruscas)
    instA = statistics.pstdev([sigA[i]-sigA[i-1] for i in range(1, len(sigA))])
    instB = statistics.pstdev([sigB[i]-sigB[i-1] for i in range(1, len(sigB))])

    print("🧪 CMR–T1 — TRÊS CORPOS OBSERVACIONAIS")
    print(f"Instabilidade Observador A (Verlet): {instA:.5f}")
    print(f"Instabilidade Observador B (Euler) : {instB:.5f}")
    print(f"Divergência média A vs B           : {statistics.mean(diffs):.5f}")
    print(f"Divergência final A vs B           : {diffs[-1]:.5f}")

if __name__ == "__main__":
    run()
