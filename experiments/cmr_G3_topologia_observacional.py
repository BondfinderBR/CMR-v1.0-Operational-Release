import random
import math

# Espaço contínuo
def ruído_regiao():
    return random.random()

def passo(pos, direcao):
    dx, dy = direcao
    return (pos[0] + dx, pos[1] + dy)

def observador_A(pos):
    # aceita atravessar qualquer região
    dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
    return passo(pos, (dx, dy)), True

def observador_B(pos, limiar=0.6):
    # rejeita regiões "incertas"
    if ruído_regiao() > limiar:
        return pos, False  # bloqueio topológico
    dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
    return passo(pos, (dx, dy)), True

def teste_G3(passos=300):
    pos_A = (0,0)
    pos_B = (0,0)

    bloqueios_B = 0

    for _ in range(passos):
        pos_A, _ = observador_A(pos_A)
        pos_B, ok = observador_B(pos_B)
        if not ok:
            bloqueios_B += 1

    print("🧪 CMR–G3 — TOPOLOGIA OBSERVACIONAL")
    print(f"Posição final Obs A: {pos_A}")
    print(f"Posição final Obs B: {pos_B}")
    print(f"Bloqueios topológicos Obs B: {bloqueios_B}")

teste_G3()
