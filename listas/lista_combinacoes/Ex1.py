def compara_valor(tupla):
    if tupla[1] < tupla[2]:
        return -1
    elif tupla[1] > tupla[2]:
        return 1
    else:
        return 0
itens = [(3, 7), (4, 9), (4, 7), (2, 4), (2, 5)]

compara_valor(itens)
