# Simulando a divergência de realidade compartilhada
import random

class Meio:
    def __init__(self, sustentacao=1.0):
        self.sustentacao = sustentacao # Força da 'verdade'

    def materializar(self, tendencia):
        # O meio decide o que o observador vê
        if random.random() < self.sustentacao:
            return tendencia # Verdade sustentada
        return random.choice([-1, 1]) # Materialização contingente

# Setup
meio = Meio(sustentacao=0.7) # Meio com falha de sustentação
geometria_global = 1 # A "tendência" do spin ser UP

print("--- TESTE DE REALIDADE ASSIMÉTRICA ---")
for i in range(10):
    obs_A = meio.materializar(geometria_global) # Olha sempre
    obs_B = meio.materializar(geometria_global) # Olha de relance
    
    status = "COERENTE" if obs_A == obs_B else "DIVERGENTE ❗"
    print(f"Frame {i}: A={obs_A} | B={obs_B} -> {status}")

