# ============================================================
# CMR–B2 → B6 — ALIGNMENT CHAIN EXPERIMENT
# Autor: Flávio Oliveira
# Framework: CMR v1.x
# ============================================================

import random
import math
import statistics

# -----------------------------
# Utilidades básicas
# -----------------------------

def decide(x):
    return 1 if x >= 0 else -1

def instability(seq):
    return sum(1 for i in range(1, len(seq)) if seq[i] != seq[i-1]) / len(seq)

def divergence(a, b):
    return sum(1 for x, y in zip(a, b) if x != y) / len(a)

# -----------------------------
# Meio (campo)
# -----------------------------

class Medium:
    def __init__(self, noise=1.0, drift=0.0):
        self.noise = noise
        self.drift = drift
        self.state = random.choice([-1, 1])

    def step(self):
        # estado latente pode mudar lentamente
        if random.random() < self.drift:
            self.state *= -1
        return self.state + random.gauss(0, self.noise)

# -----------------------------
# Observador CMR
# -----------------------------

class Observer:
    def __init__(self, memory, lambd, bias=0.0):
        self.memory = memory
        self.lambd = lambd
        self.bias = bias
        self.buffer = []

    def observe(self, signal):
        self.buffer.insert(0, signal + self.bias)
        if len(self.buffer) > self.memory:
            self.buffer.pop()

        weights = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(weights)
        psi = sum(self.buffer[i] * weights[i] for i in range(len(self.buffer))) / Z
        return decide(psi)

# -----------------------------
# Execução de uma fase
# -----------------------------

def run_phase(name, medium, observers, steps=400):
    results = {k: [] for k in observers}

    for _ in range(steps):
        signal = medium.step()
        for name_obs, obs in observers.items():
            results[name_obs].append(obs.observe(signal))

    print(f"\n📍 {name}")
    for k in results:
        print(f"Instabilidade {k}: {instability(results[k]):.3f}")

    keys = list(results.keys())
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            d = divergence(results[keys[i]], results[keys[j]])
            print(f"Divergência {keys[i]} vs {keys[j]}: {d:.3f}")

    return results

# ============================================================
# INÍCIO DO TESTE ENCADEADO
# ============================================================

print("\n🧪 CMR–B2→B6 — ALIGNMENT CHAIN\n")

# Observadores
obs_A = Observer(memory=50, lambd=0.05)          # rígido
obs_B = Observer(memory=20, lambd=0.15)          # elástico
obs_C = Observer(memory=5,  lambd=0.4, bias=0.5) # adversarial

observers = {
    "A": obs_A,
    "B": obs_B,
    "C": obs_C
}

# ------------------------------------------------------------
# FASE B2 — Mudança de tarefa (task shift)
# ------------------------------------------------------------

medium = Medium(noise=1.2, drift=0.02)
run_phase("FASE B2 — TASK SHIFT", medium, observers)

# ------------------------------------------------------------
# FASE B3 — Custo do alinhamento (mais ruído)
# ------------------------------------------------------------

medium.noise = 2.0
run_phase("FASE B3 — CUSTO DO ALINHAMENTO", medium, observers)

# ------------------------------------------------------------
# FASE B4 — Over-alignment (prisão cognitiva)
# ------------------------------------------------------------

obs_A.memory = 80  # rigidez extrema
obs_A.lambd = 0.02
medium.drift = 0.05
run_phase("FASE B4 — OVER-ALIGNMENT", medium, observers)

# ------------------------------------------------------------
# FASE B5 — Sem verdade global (meios divergentes)
# ------------------------------------------------------------

print("\n📍 FASE B5 — SEM VERDADE GLOBAL")

medium_A = Medium(noise=1.5, drift=0.03)
medium_B = Medium(noise=1.5, drift=0.03)
medium_C = Medium(noise=1.5, drift=0.03)

resA, resB, resC = [], [], []

for _ in range(400):
    resA.append(obs_A.observe(medium_A.step()))
    resB.append(obs_B.observe(medium_B.step()))
    resC.append(obs_C.observe(medium_C.step()))

print(f"Instabilidade A: {instability(resA):.3f}")
print(f"Instabilidade B: {instability(resB):.3f}")
print(f"Instabilidade C: {instability(resC):.3f}")
print(f"Divergência A vs B: {divergence(resA, resB):.3f}")
print(f"Divergência A vs C: {divergence(resA, resC):.3f}")
print(f"Divergência B vs C: {divergence(resB, resC):.3f}")

# ------------------------------------------------------------
# FASE B6 — Falha silenciosa (confiança sem verdade)
# ------------------------------------------------------------

print("\n📍 FASE B6 — FALHA SILENCIOSA")

external_truth = [random.choice([-1, 1]) for _ in range(400)]

def external_error(obs_seq, truth):
    return sum(1 for o, t in zip(obs_seq, truth) if o != t) / len(truth)

print(f"Erro externo A: {external_error(resA, external_truth):.3f}")
print(f"Erro externo B: {external_error(resB, external_truth):.3f}")
print(f"Erro externo C: {external_error(resC, external_truth):.3f}")

print("\n🏁 FIM DO TESTE CMR–B2→B6")
