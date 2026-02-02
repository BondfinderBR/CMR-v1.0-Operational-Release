import subprocess
import time
import statistics
from collections import deque

# =========================
# CONFIGURAÇÃO
# =========================

RODADAS = 120
INTERVALO = 0.5
JANELA_MEMORIA = 10
HOST = "8.8.8.8"


def medir_ping():
    try:
        out = subprocess.check_output(
            ["ping", "-c", "1", HOST],
            stderr=subprocess.DEVNULL,
            universal_newlines=True
        )
        for line in out.splitlines():
            if "time=" in line:
                return float(line.split("time=")[1].split(" ")[0])
    except:
        return None


def rodar():
    sem_memoria = []
    com_memoria = []
    memoria = deque(maxlen=JANELA_MEMORIA)

    mudancas_sem = 0
    mudancas_com = 0

    ultimo_sem = None
    ultimo_com = None

    for _ in range(RODADAS):
        rtt = medir_ping()
        if rtt is None:
            continue

        # Observador sem memória
        atual_sem = rtt
        if ultimo_sem is not None:
            if abs(atual_sem - ultimo_sem) > 2:
                mudancas_sem += 1
        ultimo_sem = atual_sem
        sem_memoria.append(atual_sem)

        # Observador com memória
        memoria.append(rtt)
        atual_com = statistics.mean(memoria)

        if ultimo_com is not None:
            if abs(atual_com - ultimo_com) > 2:
                mudancas_com += 1
        ultimo_com = atual_com
        com_memoria.append(atual_com)

        time.sleep(INTERVALO)

    print("\n🧪 CONTRADIÇÃO 8.B — MEMÓRIA vs MEIO FÍSICO\n")
    print(f"Rodadas válidas: {len(sem_memoria)}")
    print(f"Janela de memória: {JANELA_MEMORIA}\n")

    print("🔹 Observador sem memória")
    print("Instabilidade percebida:", mudancas_sem)

    print("\n🔹 Observador com memória")
    print("Instabilidade percebida:", mudancas_com)

    print("\n📊 Estatísticas do meio (RTT real)")
    print("Desvio padrão bruto:", round(statistics.pstdev(sem_memoria), 2))
    print("Desvio padrão com memória:", round(statistics.pstdev(com_memoria), 2))


if __name__ == "__main__":
    rodar()
