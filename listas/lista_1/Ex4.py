def resolver_mochila_construtiva():
    itens = [
        {'nome': 'A', 'valor': 70, 'peso': 31},
        {'nome': 'B', 'valor': 20, 'peso': 10},
        {'nome': 'C', 'valor': 39, 'peso': 20},
        {'nome': 'D', 'valor': 37, 'peso': 19},
        {'nome': 'E', 'valor': 7, 'peso': 4},
        {'nome': 'F', 'valor': 5, 'peso': 3},
        {'nome': 'G', 'valor': 10, 'peso': 6},
    ]
    capacidade_restante = 50

    nomes_originais = [item['nome'] for item in itens]

    itens_selecionados = []
    itens_disponiveis = itens.copy()
    valor_total = 0
    peso_utilizado = 0

    print("--- Processo de Construção Passo a Passo ---")
    passo = 1

    while True:
        # 1. Filtrar a lista de restrições: pegar apenas os itens que ainda cabem na mochila
        candidatos_validos = [item for item in itens_disponiveis if item['peso'] <= capacidade_restante]

        # 2. Condição de parada: se nenhum candidato cabe na mochila, encerra a construção
        if not candidatos_validos:
            break

        # 3. Aplicar a função heurística: Selecionar o item com a melhor razão Valor/Peso
        melhor_item = max(candidatos_validos, key=lambda x: (x['valor'] / x['peso'], x['valor']))

        # 4. Atualizar os estados (adicionar na mochila)
        itens_selecionados.append(melhor_item['nome'])
        capacidade_restante -= melhor_item['peso']
        valor_total += melhor_item['valor']
        peso_utilizado += melhor_item['peso']

        razao = melhor_item['valor'] / melhor_item['peso']
        print(f"Passo {passo}: Adicionado '{melhor_item['nome']}' (Densidade: {razao:.2f}) | Espaço restante: {capacidade_restante}")

        # 5. Remover o item escolhido da lista de disponíveis para a próxima iteração
        itens_disponiveis.remove(melhor_item)
        passo += 1

    mochila_binaria = "".join(["1" if nome in itens_selecionados else "0" for nome in nomes_originais])

    print("\n--- Resultado Final ---")
    print(f"Itens selecionados     : {', '.join(itens_selecionados)}")
    print(f"Organização da mochila : {mochila_binaria}")
    print(f"Valor total alcançado  : {valor_total}")
    print(f"Peso total utilizado   : {peso_utilizado}")

resolver_mochila_construtiva()
