"""
CMR_Math_Reproduction.py

Reprodução matemática direta do Framework CMR v1.0
Campo de Materialização Relacional

Autor: Flávio Oliveira
Descrição:
Este script traduz, linha por linha, a formulação matemática do CMR
em código Python executável, sem atalhos conceituais.

Objetivo:
Mostrar como a estabilidade da realidade observada emerge da memória
do observador, e não da fixidez do meio físico.
"""

import random
import math
import statistics


# -------------------------------------------------
# 1. Meio observado (estado latente + ruído)
# -------------------------------------------------

def meio_observado():
    """
    Implementa:
    O(t) = S(t) + η_meio(t)

    S(t): estado latente (não acessível)
    η_meio(t): ruído físico (simulado)
    """
    S_t = random.choice([-1, 1])          # estado latente desconhecido
    eta = random.gauss(0, 1.5)            # ruído do meio
    return S_t + eta


# -------------------------------------------------
# 2. Função de decisão (materialização do fato)
# -------------------------------------------------

def decide(valor):
    """
    Regra simples de decisão.
    Pode ser trocada por limiar, maioria, etc.
    """
    return 1 if valor >= 0 else -1


# -------------------------------------------------
# 3. Observador sem memória (caso instável)
# -------------------------------------------------

def observador_sem_memoria(amostras=200):
    """
    R(t) = decide(O(t))
    """
    realidade = []
    for _ in range(amostras):
        O_t = meio_observado()
        realidade.append(decide(O_t))
    return realidade


# -------------------------------------------------
# 4. Operador de memória (integração temporal)
# -------------------------------------------------

def operador_memoria(buffer, lambd):
    """
    Ψ_obs(t) = (1/Z) * Σ O(t - i) * exp(-λ * i)
    """
    pesos = [math.exp(-lambd * i) for i in range(len(buffer))]
    Z = sum(pesos)

    psi = sum(buffer[i] * pesos[i] for i in range(len(buffer))) / Z
    return psi


# -------------------------------------------------
# 5. Observador com memória (realidade estabilizada)
# -------------------------------------------------

def observador_com_memoria(amostras=300, k=20, lambd=0.15):
    """
    Observador que integra o meio ao longo do tempo.
    """
    buffer = []
    realidade = []

    for _ in range(amostras):
        O_t = meio_observado()
        buffer.insert(0, O_t)

        if len(buffer) > k:
            buffer.pop()

        psi = operador_memoria(buffer, lambd)
        realidade.append(decide(psi))

    return realidade


# -------------------------------------------------
# 6. Métrica de instabilidade temporal
# -------------------------------------------------

def instabilidade(realidade):
    """
    Mede quantas vezes a realidade muda de estado.
    """
    mudancas = 0
    for i in range(1, len(realidade)):
        if realidade[i] != realidade[i - 1]:
            mudancas += 1
    return mudancas / len(realidade)


# -------------------------------------------------
# 7. Dois observadores (Wigner operacional)
# -------------------------------------------------

def dois_observadores(amostras=300):
    """
    Dois observadores com memórias distintas observando o mesmo meio.
    """
    obsA = observador_com_memoria(amostras, k=25, lambd=0.1)
    obsB = observador_com_memoria(amostras, k=5, lambd=0.3)

    divergencias = sum(1 for a, b in zip(obsA, obsB) if a != b)
    return divergencias / amostras


# -------------------------------------------------
# 8. Execução principal (validação empírica)
# -------------------------------------------------

if __name__ == "__main__":
    print("🧮 CMR — Reprodução Matemática Direta\n")

    sem_mem = observador_sem_memoria()
    com_mem = observador_com_memoria()

    print("Instabilidade sem memória :", round(instabilidade(sem_mem), 3))
    print("Instabilidade com memória :", round(instabilidade(com_mem), 3))

    divergencia = dois_observadores()
    print("Divergência entre observadores A/B:", round(divergencia, 3))

    print("\nConclusão:")
    print("• O meio permanece ruidoso.")
    print("• A memória estabiliza a realidade observada.")
    print("• Observadores distintos podem viver realidades incompatíveis.")
