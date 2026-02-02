import random
import statistics

# =========================
# CAMPO CMR (MEIO)
# =========================
class CampoCMR:
    def __init__(self):
        self.estado_latente = None

    def excitar(self, estado):
        # Estado NÃO trafega
        self.estado_latente = estado

    def projetar(self):
        """
        Projeção indireta do campo.
        Não retorna estado, só efeito.
        """
        if self.estado_latente == "A":
            base = -0.3
        elif self.estado_latente == "B":
            base = 0.3
        else:
            base = 1.0

        # Ruído controla o "grau quântico"
        return random.gauss(base, 4.0)


# =========================
# EMISSOR (FENDA)
# =========================
def emissor():
    estado = random.choice(["A", "B"])
    print(f"[EMISSOR] saiu pela fenda {estado}")
    return estado


# =========================
# RECEPTOR (TELA)
# =========================
def receptor(impactos):
    media = statistics.mean(impactos)
    desvio = statistics.pstdev(impactos)

    if media < 0:
        inferido = "A"
    else:
        inferido = "B"

    print(f"[RECEPTOR] média do padrão = {media:.2f}")
    print(f"[RECEPTOR] desvio = {desvio:.2f}")
    print(f"[RECEPTOR] fenda inferida = {inferido}")

    return inferido


# =========================
# EXECUÇÃO (ORQUESTRADOR)
# =========================
def main():
    campo = CampoCMR()

    # FASE 1 — EMISSÃO
    real = emissor()
    campo.excitar(real)

    # FASE 2 — PROJEÇÃO PELO MEIO
    impactos = []
    for _ in range(200):
        impactos.append(campo.projetar())

    # FASE 3 — OBSERVAÇÃO
    inferido = receptor(impactos)

    # RESULTADO FINAL
    print("------ RESULTADO ------")
    print(f"Real: {real}")
    print(f"Inferido: {inferido}")
    print("-----------------------")


if __name__ == "__main__":
    main()
