import random

# -----------------------------
# Meio físico (compartilhado)
# -----------------------------
def meio():
    # Estado latente não acessível
    estado = random.choice([-1, 1])
    # Ruído do meio
    ruido = random.gauss(0, 1.0)
    return estado + ruido


def decide(x):
    return 1 if x >= 0 else -1


# -----------------------------
# Observador CMR
# -----------------------------
class Observador:
    def __init__(self, memoria, ruido):
        self.memoria = memoria
        self.ruido = ruido
        self.buffer = []
        self.custo = 0
        self.historico = []

    def observa(self, valor):
        valor += random.gauss(0, self.ruido)
        self.buffer.insert(0, valor)

        if len(self.buffer) > self.memoria:
            self.buffer.pop()

        psi = sum(self.buffer) / len(self.buffer)
        r = decide(psi)
        self.historico.append(r)
        return r

    def penaliza(self):
        # custo informacional
        self.custo += 1

        # custo torna o mundo mais difícil
        self.ruido *= 1.01

        # memória encolhe, mas não zera
        self.memoria = max(3, int(self.memoria * 0.99))


# -----------------------------
# Simulação principal
# -----------------------------
def rodar_simulacao(passos=2000, tolerancia=50):
    A = Observador(memoria=25, ruido=0.5)
    B = Observador(memoria=7,  ruido=0.9)

    divergencias = []
    janela_convergente = 0
    reconvergiu = False

    for t in range(passos):
        s = meio()

        rA = A.observa(s)
        rB = B.observa(s)

        if rA != rB:
            divergencias.append(1)
            A.penaliza()
            B.penaliza()
            janela_convergente = 0
        else:
            divergencias.append(0)
            janela_convergente += 1

        if janela_convergente >= tolerancia:
            reconvergiu = True

    return {
        "divergencia_media": sum(divergencias) / len(divergencias),
        "reconvergencia": reconvergiu,
        "custo_A": A.custo,
        "custo_B": B.custo,
        "memoria_A": A.memoria,
        "memoria_B": B.memoria,
        "ruido_A": round(A.ruido, 3),
        "ruido_B": round(B.ruido, 3)
    }


# -----------------------------
# Execução
# -----------------------------
if __name__ == "__main__":
    resultado = rodar_simulacao()

    print("🧪 CMR–T6 — AUTO-SINCRONIZAÇÃO SEM AUTORIDADE\n")
    print(f"Divergência média:        {resultado['divergencia_media']:.3f}")
    print(f"Reconvergência detectada: {resultado['reconvergencia']}")
    print(f"Custo final A / B:        {resultado['custo_A']} / {resultado['custo_B']}")
    print(f"Memória final A / B:      {resultado['memoria_A']} / {resultado['memoria_B']}")
    print(f"Ruído final A / B:        {resultado['ruido_A']} / {resultado['ruido_B']}")
