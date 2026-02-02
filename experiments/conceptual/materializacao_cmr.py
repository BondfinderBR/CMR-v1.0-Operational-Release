import random
import math
import statistics

# =========================
# UTILIDADES
# =========================

def entropia(valores, bins=10):
    hist = [0] * bins
    mn, mx = min(valores), max(valores)
    if mx == mn:
        return 0.0

    for v in valores:
        i = int((v - mn) / (mx - mn) * (bins - 1))
        hist[i] += 1

    total = sum(hist)
    ent = 0.0
    for h in hist:
        if h > 0:
            p = h / total
            ent -= p * math.log2(p)
    return ent


def assinatura(valores):
    return {
        "media": statistics.mean(valores),
        "desvio": statistics.pstdev(valores),
        "entropia": entropia(valores)
    }


def print_assinatura(nome, a):
    print(f"{nome}:")
    print(f"  média     = {a['media']:.3f}")
    print(f"  desvio    = {a['desvio']:.3f}")
    print(f"  entropia  = {a['entropia']:.3f}")


# =========================
# CAMPO CMR (MEIO)
# =========================

class CampoCMR:
    def __init__(self):
        self.geometria = None

    def excitar(self, assinatura):
        # NÃO guarda dados
        # apenas geometria agregada
        self.geometria = assinatura

    def materializar(self, n=50):
        if not self.geometria:
            # sem excitação → ruído puro
            return [random.gauss(0, 1) for _ in range(n)]

        m = self.geometria["media"]
        d = max(self.geometria["desvio"], 0.1)

        # materialização aproximada
        return [random.gauss(m, d) for _ in range(n)]


# =========================
# PONTO A — GERAÇÃO
# =========================

def ponto_A():
    # dado original (não será enviado)
    dados = [random.gauss(0, random.uniform(0.5, 2.5)) for _ in range(50)]

    a = assinatura(dados)

    print("\n[PONTO A] Assinatura gerada")
    print_assinatura("Assinatura A", a)

    # descarta os dados
    del dados

    return a


# =========================
# PONTO B — EMERGÊNCIA
# =========================

def ponto_B(campo):
    dados_B = campo.materializar(50)
    b = assinatura(dados_B)

    print("\n[PONTO B] Assinatura emergente")
    print_assinatura("Assinatura B", b)

    return b


# =========================
# COMPARAÇÃO
# =========================

def comparar(a, b):
    print("\n[COMPARAÇÃO]")
    for k in a:
        diff = abs(a[k] - b[k])
        print(f"{k}: diferença = {diff:.3f}")


# =========================
# EXECUÇÃO
# =========================

def main():
    campo = CampoCMR()

    assinatura_A = ponto_A()
   # campo.excitar(assinatura_A)

    assinatura_B = ponto_B(campo)

    comparar(assinatura_A, assinatura_B)

    print("\n[CRITÉRIO]")
    print("→ Se B ≈ A: materialização possível")
    print("→ Se B ~ ruído: hipótese cai")


if __name__ == "__main__":
    main()
