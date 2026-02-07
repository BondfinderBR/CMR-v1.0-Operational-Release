import random
import statistics

# -----------------------------
# Meio: tráfego aéreo simplificado
# -----------------------------
def ambiente():
    # posição real (não acessível)
    real = random.uniform(0, 1000)

    # sensores divergentes
    radarA = real + random.gauss(0, 80)
    radarB = real + random.gauss(0, 120)
    adsb   = real + random.gauss(0, 200)

    return real, [radarA, radarB, adsb]

# -----------------------------
# Envelope probabilístico
# -----------------------------
def envelope(sensores):
    return min(sensores), max(sensores)

# -----------------------------
# Decisores
# -----------------------------
def autopiloto_A(env):
    # sempre conservador
    largura = env[1] - env[0]
    if largura > 150:
        return "CAUTELA"
    return "SEGURO"

def autopiloto_B(env, memoria):
    largura = env[1] - env[0]
    media_mem = statistics.mean(memoria) if memoria else largura

    if largura > media_mem * 1.2:
        return "CAUTELA"
    return "SEGURO"

def autopiloto_C(sensores):
    # colapso clássico
    media = statistics.mean(sensores)
    return "SEGURO" if media < 900 else "RISCO"

# -----------------------------
# Simulação principal
# -----------------------------
def simular(passos=300):
    resultados = {
        "A": {"colisao":0,"cautela":0,"custo":0},
        "B": {"colisao":0,"cautela":0,"custo":0},
        "C": {"colisao":0,"cautela":0,"custo":0},
    }

    memoria_B = []

    for _ in range(passos):
        real, sensores = ambiente()
        env = envelope(sensores)

        # A
        decA = autopiloto_A(env)
        if decA == "CAUTELA":
            resultados["A"]["cautela"] += 1
            resultados["A"]["custo"] += 2

        # B
        decB = autopiloto_B(env, memoria_B)
        memoria_B.append(env[1] - env[0])
        if len(memoria_B) > 20:
            memoria_B.pop(0)

        if decB == "CAUTELA":
            resultados["B"]["cautela"] += 1
            resultados["B"]["custo"] += 1

        # C
        decC = autopiloto_C(sensores)

        # colisão real se real > 950
        if real > 950:
            if decA == "SEGURO":
                resultados["A"]["colisao"] += 1
            if decB == "SEGURO":
                resultados["B"]["colisao"] += 1
            if decC == "SEGURO":
                resultados["C"]["colisao"] += 1

    return resultados

# -----------------------------
# Execução
# -----------------------------
res = simular()

print("🧪 CMR–J2 — AUTOPILOTO RELACIONAL A+B+C\n")
for k,v in res.items():
    print(f"Autopiloto {k}:")
    print("  Colisões :", v["colisao"])
    print("  Cautelas :", v["cautela"])
    print("  Custo    :", v["custo"])
    print()
