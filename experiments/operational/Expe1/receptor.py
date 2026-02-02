# receptor.py
def observar(posicoes):
    # não sabe da fenda
    media = sum(posicoes) / len(posicoes)

    if media < 0:
        reconstruido = "A"
    else:
        reconstruido = "B"

    print(f"[RECEPTOR] padrão médio = {media:.2f}")
    print(f"[RECEPTOR] fenda inferida = {reconstruido}")
    return reconstruido
