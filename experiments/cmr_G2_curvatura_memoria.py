import random
import math

# Movimento ideal (quadrado)
def movimento(direcao, passo=1.0):
    if direcao == "N": return (0, passo)
    if direcao == "E": return (passo, 0)
    if direcao == "S": return (0, -passo)
    if direcao == "W": return (-passo, 0)

def observador_A(pos, direcao):
    dx, dy = movimento(direcao)
    return (pos[0] + dx, pos[1] + dy)

def observador_B(pos, direcao):
    dx, dy = movimento(direcao)
    dx += random.gauss(0, 0.05)
    dy += random.gauss(0, 0.05)
    return (pos[0] + dx, pos[1] + dy)

def teste_G2(voltas=50):
    pos_A = (0.0, 0.0)
    pos_B = (0.0, 0.0)

    direcoes = ["N", "E", "S", "W"]

    for _ in range(voltas):
        for d in direcoes:
            pos_A = observador_A(pos_A, d)
            pos_B = observador_B(pos_B, d)

    erro_A = math.dist(pos_A, (0, 0))
    erro_B = math.dist(pos_B, (0, 0))

    print("🧪 CMR–G2 — CURVATURA COMO MEMÓRIA")
    print(f"Erro de fechamento Obs A: {erro_A:.6f}")
    print(f"Erro de fechamento Obs B: {erro_B:.6f}")

teste_G2()
