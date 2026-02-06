import math
import copy
import statistics

G = 1.0
DT = 0.01
STEPS = 6000
SWITCH_AT = 3000  # ponto de forçamento

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

def step_verlet(bodies):
    acc = [acceleration(bodies, i) for i in range(len(bodies))]
    for i, b in enumerate(bodies):
        b.x += b.vx * DT + 0.5 * acc[i][0] * DT * DT
        b.y += b.vy * DT + 0.5 * acc[i][1] * DT * DT
    acc_new = [acceleration(bodies, i) for i in range(len(bodies))]
    for i, b in enumerate(bodies):
        b.vx += 0.5 * (acc[i][0] + acc_new[i][0]) * DT
        b.vy += 0.5 * (acc[i][1] + acc_new[i][1]) * DT

def step_euler(bodies):
    acc = [acceleration(bodies, i) for i in range(len(bodies))]
    for i, b in enumerate(bodies):
        b.vx += acc[i][0] * DT
        b.vy += acc[i][1] * DT
        b.x += b.vx * DT
        b.y += b.vy * DT

def state_signature(bodies):
    kinetic = sum(0.5*b.m*(b.vx*b.vx + b.vy*b.vy) for b in bodies)
    potential = 0.0
    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            dx = bodies[j].x - bodies[i].x
            dy = bodies[j].y - bodies[i].y
            r = math.sqrt(dx*dx + dy*dy) + 1e-9
            potential -= G * bodies[i].m * bodies[j].m / r
    return kinetic + potential

def run():
    init = [
        Body(1.0, -1.0, 0.0, 0.0, 0.6),
        Body(1.0,  1.0, 0.0, 0.0, -0.6),
        Body(1.0,  0.0, 0.5, -0.5, 0.0),
    ]

    A = copy.deepcopy(init)
    B = copy.deepcopy(init)

    sigA, sigB, diffs = [], [], []

    for t in range(STEPS):
        # Antes do forçamento: políticas diferentes
        if t < SWITCH_AT:
            step_verlet(A)
            step_euler(B)
        # Após o forçamento: mesma política (Verlet)
        else:
            step_verlet(A)
            step_verlet(B)

        sA = state_signature(A)
        sB = state_signature(B)
        sigA.append(sA)
        sigB.append(sB)
        diffs.append(abs(sA - sB))

    # Métricas
    pre = diffs[:SWITCH_AT]
    post = diffs[SWITCH_AT:]

    instA = statistics.pstdev([sigA[i]-sigA[i-1] for i in range(1, len(sigA))])
    instB = statistics.pstdev([sigB[i]-sigB[i-1] for i in range(1, len(sigB))])

    print("🧪 CMR–T2 — RECONVERGÊNCIA FORÇADA")
    print(f"Instabilidade A total: {instA:.5f}")
    print(f"Instabilidade B total: {instB:.5f}")
    print(f"Divergência média ANTES : {statistics.mean(pre):.5f}")
    print(f"Divergência média DEPOIS: {statistics.mean(post):.5f}")
    print(f"Divergência final       : {post[-1]:.5f}")

if __name__ == "__main__":
    run()
