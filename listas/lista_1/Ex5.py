from math import hypot
from pathlib import Path


def le_arq_tsp(arquivo):
    coordenadas = {}

    with open(arquivo, "r") as f:
        for linha in f:
            # O arquivo traz: id_da_cidade x y
            partes = linha.strip().split()
            if len(partes) == 3:
                cidade = int(partes[0])
                x = float(partes[1])
                y = float(partes[2])
                coordenadas[cidade] = (x, y)

    # Constrói um grafo completo com distâncias euclidianas entre todas as cidades.
    grafo = {cidade: {} for cidade in coordenadas}
    cidades = list(coordenadas.keys())

    for i, cidade_de in enumerate(cidades):
        x1, y1 = coordenadas[cidade_de]
        for cidade_ate in cidades[i + 1:]:
            x2, y2 = coordenadas[cidade_ate]
            distancia = hypot(x2 - x1, y2 - y1)
            grafo[cidade_de][cidade_ate] = distancia
            grafo[cidade_ate][cidade_de] = distancia

    return grafo

def heuristica_vizinho_mais_proximo(grafo, cidade_inicial):
    # Cria uma lista de todas as cidades e remove a inicial
    cidades_nao_visitadas = set(grafo.keys())

    # Verifica se a cidade inicial existe no grafo
    if cidade_inicial not in cidades_nao_visitadas:
        raise ValueError(f"A cidade inicial {cidade_inicial} não foi encontrada no arquivo.")

    cidades_nao_visitadas.remove(cidade_inicial)

    rota = [cidade_inicial]
    cidade_atual = cidade_inicial
    distancia_total = 0.0

    # Enquanto houver cidades para visitar
    while cidades_nao_visitadas:
        vizinho_mais_perto = None
        menor_distancia = float('inf')

        # Procura a cidade não visitada mais próxima
        for vizinho in cidades_nao_visitadas:
            # Verifica se existe uma aresta entre a cidade atual e o vizinho
            if vizinho in grafo[cidade_atual]:
                dist = grafo[cidade_atual][vizinho]
                if dist < menor_distancia:
                    menor_distancia = dist
                    vizinho_mais_perto = vizinho

        if vizinho_mais_perto is None:
            print("Erro: O grafo não está totalmente conectado ou há cidades isoladas.")
            break

        # Move para a cidade mais próxima encontrada
        rota.append(vizinho_mais_perto)
        distancia_total += menor_distancia
        cidades_nao_visitadas.remove(vizinho_mais_perto)
        cidade_atual = vizinho_mais_perto

    # Retorna à cidade de origem para fechar o ciclo do TSP
    if cidade_inicial in grafo[cidade_atual]:
        distancia_total += grafo[cidade_atual][cidade_inicial]
        rota.append(cidade_inicial)

    return rota, distancia_total

if __name__ == "__main__":
    nome_do_arquivo = Path(__file__).with_name("cidades50.txt")

    try:
        grafo_tsp = le_arq_tsp(nome_do_arquivo)

        cidade_partida = 10
        melhor_rota, custo_total = heuristica_vizinho_mais_proximo(grafo_tsp, cidade_partida)

        print(f"--- Solução Inicial Gulosa (Iniciando na cidade {cidade_partida}) ---")
        print(f"Custo total da rota : {custo_total:.2f}")
        print(f"Sequência de cidades: {melhor_rota}")

    except FileNotFoundError:
        print(f"Arquivo '{nome_do_arquivo}' não encontrado. Verifique o caminho.")