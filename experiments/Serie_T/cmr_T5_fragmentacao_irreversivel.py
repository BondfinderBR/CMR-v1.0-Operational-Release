import random
import math

def sistema_caotico(x):
    return math.sin(x) + random.gauss(0, 0.05)

def observador(x, metodo):
    ruido = 0.05 if metodo == "verlet" else 0.2
    return sistema_caotico(x) + random.gauss(0, ruido)

def teste_T5(passos=400, atraso=250):
    x = 0.1
    divergencias = []
    metodo_B = "euler"

    for i in range(passos):
        A = observador(x, "verlet")
        B = observador(x, metodo_B)

        divergencias.append(abs(A - B))

        # Política só entra tarde demais
        if i == atraso:
            metodo_B = "verlet"

        x += 0.01

    print("🧪 CMR–T5 — FRAGMENTAÇÃO IRREVERSÍVEL")
    print(f"Divergência média: {sum(divergencias)/len(divergencias):.4f}")
    print(f"Divergência final: {divergencias[-1]:.4f}")

teste_T5()
