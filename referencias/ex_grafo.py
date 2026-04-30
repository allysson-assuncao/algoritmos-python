def problema_3_rotas():
    print("=== Otimizador de Rotas (Vizinho Mais Próximo) ===")

    # 1. Matriz Quadrada de Distâncias
    distancias = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]

    nomes_cidades = ["A", "B", "C", "D"]
    num_cidades = len(distancias) # Retorna 4

    # 2. Entrada de dados e Tratamento de Erro Básico
    print("Cidades disponíveis: 0: A, 1: B, 2: C, 3: D")
    entrada_origem = input("Digite o número da cidade de origem (0 a 3): ")

    if not entrada_origem.isdigit() or int(entrada_origem) >= num_cidades:
        print("Entrada inválida. Usando a cidade 0 (A) como padrão.")
        cidade_atual = 0
    else:
        cidade_atual = int(entrada_origem)

    cidade_origem = cidade_atual

    # 3. Estruturas de Dados: Sets e Listas
    # Usamos um Set (conjunto) para as cidades não visitadas.
    cidades_nao_visitadas = {0, 1, 2, 3}
    cidades_nao_visitadas.remove(cidade_atual) # Removemos a origem pois já estamos nela

    rota = [cidade_atual] # Lista para manter a ORDEM do trajeto
    distancia_total = 0

    # 4. Lógica de Navegação (While loop)
    while len(cidades_nao_visitadas) > 0:

        # Inicializamos a menor distância com "infinito" do Python
        menor_distancia = float('inf')
        proxima_cidade = None

        # 5. Laço For iterando sobre os elementos do Conjunto (Set)
        # Checamos apenas as cidades que AINDA NÃO visitamos
        for destino_candidato in cidades_nao_visitadas:

            # Acesso à matriz bidimensional: matriz[linha][coluna]
            distancia_candidata = distancias[cidade_atual][destino_candidato]

            # Encontrando o menor valor "na mão"
            if distancia_candidata < menor_distancia:
                menor_distancia = distancia_candidata
                proxima_cidade = destino_candidato

        # Movemos para a cidade mais próxima encontrada
        rota.append(proxima_cidade)
        distancia_total += menor_distancia
        cidade_atual = proxima_cidade

        # Operação de Conjunto: Removemos a cidade escolhida para não voltar nela
        cidades_nao_visitadas.remove(cidade_atual)

    # 6. Fechando o ciclo (Voltando para a origem)
    distancia_volta = distancias[cidade_atual][cidade_origem]
    distancia_total += distancia_volta
    rota.append(cidade_origem)

    # 7. Manipulação de Listas para a Saída de Resultados
    print("\n--- Resultado da Rota ---")

    # List Comprehension para converter os índices [0, 1, 3...] nos nomes ["A", "B", "D"...]
    rota_nomes = [nomes_cidades[i] for i in rota]

    # O método .join() une os elementos da lista usando uma string como separador
    caminho_formatado = " -> ".join(rota_nomes)

    print("Melhor trajeto encontrado (Heurística Gulosa):")
    print(caminho_formatado)
    print(f"Distância total percorrida: {distancia_total} km")

# Executando a função
if __name__ == "__main__":
    problema_3_rotas()
