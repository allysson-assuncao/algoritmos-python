import numpy as np

lista_lancamento_dados = np.random.uniform(1, 7, 10000000).astype(int)

faces, contagem = np.unique(lista_lancamento_dados, return_counts=True)

prob_teorica = 1/6

print(f"Probabilidade Teórica: {prob_teorica:.6f}\n")

for f, c in zip(faces, contagem):
    prob_real = c / 10000000
    print(f"Face {f}: Saiu {c} vezes | Chance: {prob_real:.6f}")
