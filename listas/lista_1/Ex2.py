import numpy as np
import matplotlib.pyplot as plt

numero_lancamentos = 1000000

dado1 = np.random.randint(1, 7, numero_lancamentos)
dado2 = np.random.randint(1, 7, numero_lancamentos)

somas = dado1 + dado2

faces_soma, contagem_soma = np.unique(somas, return_counts=True)

print("--- Simulação da Soma de Dois Dados ---\n")
for f, c in zip(faces_soma, contagem_soma):
    prob_real = c / numero_lancamentos
    print(f"Soma {f:02d}: Saiu {c} vezes | Chance: {prob_real:.6f}")

plt.figure(figsize=(12, 6))

barras = plt.bar(faces_soma, contagem_soma, color='#55A868', edgecolor='black', zorder=2, label='Frequência Real da Soma')

plt.title('Distribuição da Soma de 2 Dados (1.000.000 Lançamentos)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Valor da Soma (2 ao 12)', fontsize=12, labelpad=10)
plt.ylabel('Contagem (Frequência)', fontsize=12, labelpad=10)

plt.xticks(faces_soma)
plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
plt.legend(loc='upper right', framealpha=1)

for barra in barras:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, yval + 2000,
             f'{yval:,}'.replace(',', '.'), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()