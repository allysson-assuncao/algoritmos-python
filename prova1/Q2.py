import numpy as np

print(" --- Questão 2 a) --- \n\n\n")
a = np.array([-10, -3, 0, 2, 3, 6, 7, 9, 12, 15])

novo_vetor = np.array([n for n in a if n >= 0 and n % 3 == 0])
print(novo_vetor)



print("\n\n\n --- Questão 2 b) --- \n\n\n")
A = np.array([
    [3, 12, 7, 18],
    [5, 20, 9, 14],
    [6, 25, 11, 30],
    [8, 15, 22, 4]
])

nova_matriz = np.array([n for x in A for n in x if n > 10 or n % 2 == 0])
print(nova_matriz)
