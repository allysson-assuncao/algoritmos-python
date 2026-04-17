def le_arq_tsp(arquivo):
    grafo = {}
    with open(arquivo, "r") as f:
        linhas = f.readlines()
    for linha in linhas:
        partes = linha.strip().split()
        if len(partes) == 3:
            u, v, d = int(partes[0]), int(partes[1]), float(partes[2])
            if u not in grafo: grafo[u] = {}
            if v not in grafo: grafo[v] = {}
            grafo[u][v] = d
            grafo[v][u] = d
    return grafo

def resolver_tsp_insercao_barata(grafo, cidade_inicial):
    cidades_nao_visitadas = set(grafo.keys())
    if cidade_inicial not in cidades_nao_visitadas:
        raise ValueError(f"Cidade {cidade_inicial} não encontrada.")

    cidades_nao_visitadas.remove(cidade_inicial)

    # 1. Encontrar a cidade mais próxima para criar o ciclo inicial (10 -> vizinho -> 10)
    primeiro_vizinho = min(cidades_nao_visitadas,
                           key=lambda c: grafo[cidade_inicial].get(c, float('inf')))
    cidades_nao_visitadas.remove(primeiro_vizinho)

    # Rota inicial circular
    rota = [cidade_inicial, primeiro_vizinho, cidade_inicial]
    custo_total = grafo[cidade_inicial][primeiro_vizinho] * 2

    # 2. Processo de Inserção
    while cidades_nao_visitadas:
        melhor_custo_insercao = float('inf')
        melhor_cidade = None
        melhor_posicao = -1

        # Testa cada cidade de fora...
        for k in cidades_nao_visitadas:
            for idx in range(len(rota) - 1):
                i = rota[idx]
                j = rota[idx + 1]

                if k in grafo[i] and k in grafo[j]:
                    # Custo extra = (distancia para ir e voltar de k) - (distancia que ja existia entre i e j)
                    custo_insercao = grafo[i][k] + grafo[k][j] - grafo[i][j]

                    if custo_insercao < melhor_custo_insercao:
                        melhor_custo_insercao = custo_insercao
                        melhor_cidade = k
                        melhor_posicao = idx + 1

        if melhor_cidade is not None:
            rota.insert(melhor_posicao, melhor_cidade)
            custo_total += melhor_custo_insercao
            cidades_nao_visitadas.remove(melhor_cidade)
        else:
            break # Caso o grafo não seja completo e não haja conexões

    return rota, custo_total

# --- Execução ---
grafo = le_arq_tsp("cidades50.txt")
rota, custo = resolver_tsp_insercao_barata(grafo, 10)
print(f"Custo: {custo}\nRota: {rota}")