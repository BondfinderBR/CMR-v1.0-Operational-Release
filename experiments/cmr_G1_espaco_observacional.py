import random
import math

# Pontos reais no espaço (meio)
def pontos_reais(n=100):
    return [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(n)]

# Distância Euclidiana (Observador A)
def distancia_euclidiana(p1, p2):
    return math.dist(p1, p2)

# Distância Observacional Ruidosa (Observador B)
def distancia_observacional(p1, p2):
    base = math.dist(p1, p2)
    ruido = random.gauss(0, 0.2)
    distorcao = 1.05  # viés sistemático
    return base * distorcao + ruido

def teste_G1():
    pts = pontos_reais(200)
    divergencias = []

    for i in range(len(pts)-1):
        dA = distancia_euclidiana(pts[i], pts[i+1])
        dB = distancia_observacional(pts[i], pts[i+1])
        divergencias.append(abs(dA - dB))

    print("🧪 CMR–G1 — ESPAÇO OBSERVACIONAL")
    print(f"Divergência média de distância: {sum(divergencias)/len(divergencias):.4f}")
    print(f"Divergência máxima: {max(divergencias):.4f}")

teste_G1()
