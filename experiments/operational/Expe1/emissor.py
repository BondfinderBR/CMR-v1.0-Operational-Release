# emissor.py
import random

def emitir():
    # decide por qual fenda "saiu"
    escolha = random.choice(["A", "B"])
    print(f"[EMISSOR] saiu pela fenda {escolha}")
    return escolha
