import random
import statistics
import math

# =========================
# 1. MODELO DO MEIO REAL
# =========================

def meio_real():
    """
    Posição real do drone (desconhecida aos observadores)
    """
    x = random.uniform(0, 1000)
    y = random.uniform(0, 1000)
    return (x, y)

# =========================
# 2. OBSERVADORES (SENSORES)
# =========================

def sensor_radar(pos):
    # radar: ruído médio
    return (
        pos[0] + random.gauss(0, 30),
        pos[1] + random.gauss(0, 30)
    )

def sensor_gps(pos):
    # GPS: ruído maior + drift ocasional
    drift = random.choice([0, 0, 0, 50])
    return (
        pos[0] + random.gauss(0, 60) + drift,
        pos[1] + random.gauss(0, 60) + drift
    )

def sensor_visual(pos):
    # visão computacional: alta precisão, mas instável
    if random.random() < 0.15:
        # falha momentânea
        return None
    return (
        pos[0] + random.gauss(0, 10),
        pos[1] + random.gauss(0, 10)
    )

# =========================
# 3. HUD CMR (ENVELOPE)
# =========================

def construir_envelope(observacoes):
    """
    Cria envelope probabilístico de segurança
    """
    xs = [o[0] for o in observacoes if o is not None]
    ys = [o[1] for o in observacoes if o is not None]

    if not xs or not ys:
        return None

    centro = (
        statistics.mean(xs),
        statistics.mean(ys)
    )

    raio = max(
        math.dist(centro, o)
        for o in observacoes if o is not None
    )

    return centro, raio

# =========================
# 4. DECISÃO OPERACIONAL
# =========================

def decisao_hud(envelope, obstaculo):
    """
    Verifica se envelope cruza zona proibida
    """
    centro, raio = envelope
    distancia = math.dist(centro, obstaculo)

    if distancia <= raio:
        return "RISCO"
    elif distancia <= raio + 50:
        return "CAUTELA"
    else:
        return "SEGURO"

# =========================
# 5. SIMULAÇÃO PRINCIPAL
# =========================

def simular(iteracoes=200):
    riscos = 0
    cautelas = 0
    seguros = 0

    for _ in range(iteracoes):
        real = meio_real()

        obs = [
            sensor_radar(real),
            sensor_gps(real),
            sensor_visual(real)
        ]

        envelope = construir_envelope(obs)
        if envelope is None:
            continue

        # obstáculo fixo no espaço
        obstaculo = (500, 500)

        estado = decisao_hud(envelope, obstaculo)

        if estado == "RISCO":
            riscos += 1
        elif estado == "CAUTELA":
            cautelas += 1
        else:
            seguros += 1

    print("🧪 CMR–J1 — HUD MULTI-OBSERVADOR\n")
    print(f"Estados SEGUROS : {seguros}")
    print(f"Estados CAUTELA : {cautelas}")
    print(f"Estados RISCO   : {riscos}")
    print("\n📌 Interpretação CMR:")
    print("- HUD não mostra posição única")
    print("- Envelope torna a incerteza visível")
    print("- Segurança emerge da margem, não da certeza")

# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    simular()
