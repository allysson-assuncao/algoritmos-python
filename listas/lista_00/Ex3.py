

# [Joao, Lucas, Pedro, Jorge]


# [(0, 1), (0, 2), (0, 3)
#          (1, 2), (1, 3)
#                  (2, 3)]

def solucao1():
    n = int(input("Total de jogadores no torneio? "))
    jogadores = [input(f"Nome do jogador {i+1}: ") for i in range(n)]

    jogos = [(jogadores[i], jogadores[j])
                  for i in range(len(jogadores))
                  for j in range(i + 1, len(jogadores))]

    print("\nPerimeira Fase de Jogos")
    resultados = {}

    for p1, p2 in jogos:
        print(f"\nPartida: {p1} vs {p2}")
        vencedor = input(f"Quem venceu? ({p1}/{p2}/Empate): ")
        resultados[(p1, p2)] = vencedor

    pontos = {nome: 0 for nome in jogadores}

    for (p1, p2), v in resultados.items():
        if v == p1:
            pontos[p1] += 3
        elif v == p2:
            pontos[p2] += 3
        else:
            pontos[p1] += 1
            pontos[p2] += 1

    print("\n--- Resultado Final ---")
    for jogador, score in sorted(pontos.items(), key=lambda x: x[1], reverse=True):
        print(f"{jogador}: {score} pontos")

def solucao2():

    n = int(input("Qntd de jogadores: "))
    jogadores = [str(input("Informe o nome dos jogadores(as): ")) for i in range(n)]

def solucao3():

    n = int(input("Qntd de jogadores: "))
    jogadores = [str(input("Informe o nome dos jogadores(as): ")) for i in range(n)]

if __name__ == '__main__':
    solucao1()