import random
import math

def meio(t):
    return math.sin(t / 12)

class Observador:
    def __init__(self, memoria, lambd):
        self.memoria = memoria
        self.lambd = lambd
        self.buffer = []

    def observa(self, v):
        o = v + random.gauss(0, 0.5)
        self.buffer.insert(0, o)
        if len(self.buffer) > self.memoria:
            self.buffer.pop()
        return self.integrar()

    def integrar(self):
        pesos = [math.exp(-self.lambd * i) for i in range(len(self.buffer))]
        Z = sum(pesos)
        return sum(self.buffer[i]*pesos[i] for i in range(len(self.buffer))) / Z

def decide(x):
    return 1 if x >= 0 else -1

A = Observador(memoria=5,  lambd=0.4)
B = Observador(memoria=25, lambd=0.1)

div = 0
for t in range(300):
    v = meio(t)
    if decide(A.observa(v)) != decide(B.observa(v)):
        div += 1

print("🧪 CMR–T′2 — PRESENTES INCOMPATÍVEIS")
print(f"Divergência de presente: {div/300:.3f}")
