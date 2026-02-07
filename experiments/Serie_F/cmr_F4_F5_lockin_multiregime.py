import random
import math
import statistics

# -------------------------
# MEIO
# -------------------------

def meio():
    estado = random.choice([-1, 1])
    ruido = random.gauss(0, 1.1)
    return estado + ruido


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
# POLÍTICAS
# -------------------------

def politica_rigida(v):
    return decide(v)

def politica_elastica(v):
    return decide(v + random.gauss(0, 0.7))

def politica_instavel(v):
    return random.choice([-1, 1])


# -------------------------
# OBSERVADOR
# -------------------------

def observador(politica, passos=300, k=20, lambd=0.15):
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
            r = politica_instavel(psi)

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
# F4 — LOCK-IN
# -------------------------

def teste_lockin():
    base = observador("rigida")
    inst_base = instabilidade(base)

    # tentativa de ruptura progressiva
    ruptura = []
    for _ in range(3):
        ruptura = observador("elastica")
    inst_pos = instabilidade(ruptura)

    lockin = inst_pos > inst_base * 0.9

    return inst_base, inst_pos, lockin


# -------------------------
# F5 — MULTI-REGIME
# -------------------------

def controlador_multiregime():
    regimes = ["rigida", "instavel", "elastica"]
    realidade = []

    for r in regimes:
        realidade.extend(observador(r, passos=120))

    inst = instabilidade(realidade)

    # teste de retorno à elasticidade
    retorno = observador("elastica", passos=120)
    inst_retorno = instabilidade(retorno)

    return inst, inst_retorno


# -------------------------
# EXECUÇÃO
# -------------------------

inst_base, inst_pos, lockin = teste_lockin()
inst_mr, inst_ret = controlador_multiregime()

print("\n🧪 CMR — F4 + F5\n")

print("F4 — Lock-in Consciente:")
print(f"  Instabilidade base       : {inst_base:.3f}")
print(f"  Instabilidade pós-ruptura: {inst_pos:.3f}")
print(f"  Lock-in detectado        : {lockin}\n")

print("F5 — Governança Multi-Regime:")
print(f"  Instabilidade global     : {inst_mr:.3f}")
print(f"  Instabilidade pós-retorno: {inst_ret:.3f}")
