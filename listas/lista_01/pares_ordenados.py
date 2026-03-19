# Exercício: Pares Ordenados entre dois Conjuntos
#
# Obtenha do usuário dois conjuntos de valores e armazene-os em duas variáveis conjunto
# (set). Em seguida, apresente no console todas as tuplas formadas pelos pares ordenados
# (x1, x2), onde x1 está no set1 e x2 no set2.

print("Digite os valores do primeiro conjunto separados por espaço:")
set1 = set(input().split())

print("Digite os valores do segundo conjunto separados por espaço:")
set2 = set(input().split())

print("\nPares ordenados (x1, x2):")
for x1 in set1:
    for x2 in set2:
        print((x1, x2))
