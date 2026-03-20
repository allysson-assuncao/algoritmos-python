

# [Joao, Lucas, Pedro, Jorge]


# [(0, 1), (0, 2), (0, 3)
#          (1, 2), (1, 3)
#                  (2, 3)]

def solucao1():
    n = int(input("Qntd de jogadores: "))
    jogadores = [str(input("Informe o nome dos jogadores: ")) for i in range(n)]




    tuplas = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for x in tuplas:
        for y in x:
            print(str(y) + ", ")

def solucao2():

    n = int(input("Qntd de jogadores: "))
    jogadores = [str(input("Informe o nome dos jogadores(as): ")) for i in range(n)]






def solucao3():

    n = int(input("Qntd de jogadores: "))
    jogadores = [str(input("Informe o nome dos jogadores(as): ")) for i in range(n)]





if __name__ == '__main__':
    solucao1()