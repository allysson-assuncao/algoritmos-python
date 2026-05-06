a1 = [1, 3, 5, 7, 9]
a2 = [0, 2, 4, 6, 8]

def retorna_lista_de_pares_ordenadas(a1, a2):
    return set([(n1, n2) for n1 in a1 for n2 in a2])

print(retorna_lista_de_pares_ordenadas(a1, a2))