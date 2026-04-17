import numpy as np
import matplotlib.pyplot as plt

numero_lancamentos = 1000000

lista_lancamento_dados = np.random.uniform(1, 7, numero_lancamentos).astype(int)
faces, contagem = np.unique(lista_lancamento_dados, return_counts=True)

prob_teorica = 1/6
print(f"Probabilidade Teórica: {prob_teorica:.6f}\n")

for f, c in zip(faces, contagem):
    prob_real = c / numero_lancamentos
    print(f"Face {f}: Saiu {c} vezes | Chance: {prob_real:.6f}")

plt.figure(figsize=(10, 6))

barras = plt.bar(faces, contagem, color='#4C72B0', edgecolor='black', zorder=2, label='Frequência Real')

contagem_teorica = numero_lancamentos / 6
plt.axhline(y=contagem_teorica, color='#C44E52', linestyle='--', linewidth=2, zorder=3, label='Frequência Teórica Esperada')

plt.title('Distribuição de 1.000.000 Lançamentos de 1 Dado', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Face do Dado', fontsize=12, labelpad=10)
plt.ylabel('Contagem (Frequência)', fontsize=12, labelpad=10)

plt.xticks(faces)
plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
plt.legend(loc='upper left', framealpha=1)

for barra in barras:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, yval + 5000,
             f'{yval:,}'.replace(',', '.'), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()