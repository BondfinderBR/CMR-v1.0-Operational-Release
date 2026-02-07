import random
import math

def movimento(direcao, passo=1.0):
    if direcao == "N": return (0, passo)
    if direcao == "E": return (passo, 0)
    if direcao == "S": return (0, -passo)
    if direcao == "W": return (-passo, 0)

def observador(pos, direcao):
    dx, dy = movimento(direcao)
    dx += random.gauss(0, 0.05)
    dy += random.gauss(0, 0.05)
    return (pos[0] + dx, pos[1] + dy)

def teste_G2B(voltas=60, limiar=0.6):
    pos = (0.0, 0.0)
    origem = (0.0, 0.0)
    direcoes = ["N", "E", "S", "W"]

    erros = []
    intervencoes = 0

    for _ in range(voltas):
        for d in direcoes:
            pos = observador(pos, d)

        erro = math.dist(pos, origem)
        erros.append(erro)

        # Governança da curvatura
        if erro > limiar:
            # reancoragem parcial (não zera)
            pos = ((pos[0] + origem[0]) / 2, (pos[1] + origem[1]) / 2)
            intervencoes += 1

    print("🧪 CMR–G2B — GOVERNANÇA DA CURVATURA")
    print(f"Erro médio: {sum(erros)/len(erros):.4f}")
    print(f"Erro máximo: {max(erros):.4f}")
    print(f"Intervenções: {intervencoes}")

teste_G2B()
