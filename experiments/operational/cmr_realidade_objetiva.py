import random
import time

RODADAS = 20000

# força do meio (1.0 = forte, <0.7 = fraco)
FORCA_MEIO = 1.0

# frequência de observação
OBS_A_FREQ = 1      # observa sempre
OBS_B_FREQ = 50     # observa de relance


def materializar(meio_forca):
    """
    Materialização contingente.
    Não existe valor guardado.
    """
    if random.random() < meio_forca:
        return random.choice([1, -1])
    else:
        return random.choice([1, -1])


def rodar():
    divergencias = 0
    leituras_B = 0

    estado_A = None

    for t in range(RODADAS):
        # Observador A sustenta continuamente
        estado_A = materializar(FORCA_MEIO)

        # Observador B olha só de vez em quando
        if t % OBS_B_FREQ == 0:
            estado_B = materializar(FORCA_MEIO)
            leituras_B += 1

            if estado_B != estado_A:
                divergencias += 1

    print("\n🧪 TESTE A vs B — REALIDADE OBJETIVA")
    print("FORÇA DO MEIO:", FORCA_MEIO)
    print("Leituras de B:", leituras_B)
    print("Divergências:", divergencias)
    print("Taxa de divergência:", round(divergencias / leituras_B, 3))


if __name__ == "__main__":
    rodar()
