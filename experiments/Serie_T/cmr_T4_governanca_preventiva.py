import random
import math

# Simulação simples de sistema caótico (proxy observacional)
def sistema_caotico(x):
    return math.sin(x) + random.gauss(0, 0.05)

def observador(x, metodo="verlet"):
    if metodo == "verlet":
        return sistema_caotico(x)
    elif metodo == "euler":
        return sistema_caotico(x) + random.gauss(0, 0.15)

def teste_T4(passos=300, limiar=0.25):
    x = 0.1
    divergencias = []
    intervencoes = 0

    metodo_B = "euler"

    for _ in range(passos):
        A = observador(x, "verlet")
        B = observador(x, metodo_B)

        d = abs(A - B)
        divergencias.append(d)

        # Governança preventiva
        if d > limiar:
            metodo_B = "verlet"
            intervencoes += 1

        x += 0.01

    print("🧪 CMR–T4 — GOVERNANÇA PREVENTIVA")
    print(f"Divergência média: {sum(divergencias)/len(divergencias):.4f}")
    print(f"Divergência máxima: {max(divergencias):.4f}")
    print(f"Intervenções preventivas: {intervencoes}")

teste_T4()
