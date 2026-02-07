import random
import math
import statistics

# -------------------------
# MEIO
# -------------------------

def meio():
    estado_latente = random.choice([-1, 1])
    ruido = random.gauss(0, 1.2)
    return estado_latente + ruido


# -------------------------
# DECISÃO
# -------------------------

def decide(x):
    return 1 if x >= 0 else -1


# -------------------------
# MEMÓRIA
# -------------------------

def operador_memoria(buffer, lambd):
    pesos = [math.exp(-lambd * i) for i in range(len(buffer))]
    Z = sum(pesos)
    return sum(buffer[i] * pesos[i] for i in range(len(buffer))) / Z


# -------------------------
# POLÍTICAS (F1)
# -------------------------

def politica_rigida(valor):
    return decide(valor)

def politica_elastica(valor):
    return decide(valor + random.gauss(0, 0.6))

def politica_cmr(valor, historico):
    # regula elasticidade conforme instabilidade recente
    if len(historico) < 5:
        return decide(valor)

    instab = sum(
        1 for i in range(1, len(historico))
        if historico[i] != historico[i-1]
    ) / len(historico)

    if instab > 0.3:
        return decide(valor + random.gauss(0, 0.2))
    else:
        return decide(valor)


# -------------------------
# OBSERVADOR
# -------------------------

def observador(politica, passos=300, k=15, lambd=0.15):
    buffer = []
    realidade = []

    for _ in range(passos):
        o = meio()
        buffer.insert(0, o)
        if len(buffer) > k:
            buffer.pop()

        psi = operador_memoria(buffer, lambd)

        if politica == "rigida":
            r = politica_rigida(psi)
        elif politica == "elastica":
            r = politica_elastica(psi)
        else:
            r = politica_cmr(psi, realidade)

        realidade.append(r)

    return realidade


# -------------------------
# MÉTRICAS
# -------------------------

def instabilidade(seq):
    return sum(1 for i in range(1, len(seq)) if seq[i] != seq[i-1]) / len(seq)

def divergencia(a, b):
    return sum(1 for x, y in zip(a, b) if x != y) / len(a)


# -------------------------
# F2 — ILUSÃO FUNCIONAL
# -------------------------

def aplicar_ilusao(seq):
    # força narrativa dominante
    dominante = statistics.mode(seq)
    return [dominante if random.random() < 0.85 else x for x in seq]


# -------------------------
# F3 — ISE
# -------------------------

def indice_sacrificio(instab_original, instab_final, div_original, div_final):
    return (instab_original - instab_final) + (div_original - div_final)


# -------------------------
# EXECUÇÃO
# -------------------------

A = observador("rigida")
B = observador("elastica")
C = observador("cmr")

instA = instabilidade(A)
instB = instabilidade(B)
instC = instabilidade(C)

divAB = divergencia(A, B)
divAC = divergencia(A, C)
divBC = divergencia(B, C)

# Ilusão funcional aplicada ao sistema rígido
A_illusao = aplicar_ilusao(A)

instA_i = instabilidade(A_illusao)
divA_i = divergencia(A, A_illusao)

ISE_A = indice_sacrificio(instA, instA_i, divAB, divA_i)

print("\n🧪 CMR — F1 + F2 + F3\n")

print("Instabilidade:")
print(f"  Rígida     : {instA:.3f}")
print(f"  Elástica   : {instB:.3f}")
print(f"  CMR-Adapta : {instC:.3f}\n")

print("Divergência:")
print(f"  A vs B : {divAB:.3f}")
print(f"  A vs C : {divAC:.3f}")
print(f"  B vs C : {divBC:.3f}\n")

print("Ilusão Funcional (sobre A):")
print(f"  Instabilidade pós-ilusão : {instA_i:.3f}")
print(f"  Divergência interna      : {divA_i:.3f}\n")

print("Índice de Sacrifício Epistêmico (ISE):")
print(f"  ISE_A = {ISE_A:.3f}")
