def resolver_mochila():
    itens = [
        {'nome': 'A', 'valor': 3, 'peso': 7},
        {'nome': 'B', 'valor': 4, 'peso': 9},
        {'nome': 'C', 'valor': 2, 'peso': 4},
        {'nome': 'D', 'valor': 4, 'peso': 7},
        {'nome': 'E', 'valor': 2, 'peso': 5},
    ]
    capacidade = 23

    # 1. Ordenar: Valor decrescente e Peso crescente
    itens.sort(key=lambda x: (-x['valor'], x['peso']))

    print("--- Itens Ordenados ---")
    for item in itens:
        print(f"{item['nome']}: Valor={item['valor']}, Peso={item['peso']}")

    # 2. Preencher a mochila (Abordagem Gulosa)
    mochila_binaria = ""
    valor_total = 0
    peso_utilizado = 0

    for item in itens:
        if item['peso'] <= capacidade:
            mochila_binaria += "1"
            capacidade -= item['peso']
            valor_total += item['valor']
            peso_utilizado += item['peso']
        else:
            mochila_binaria += "0"

    # 3. Exibir resultados
    print("\n--- Resultado ---")
    print(f"Organização da mochila : {mochila_binaria}")
    print(f"Valor total alcançado  : {valor_total}")
    print(f"Peso total utilizado   : {peso_utilizado}")

resolver_mochila()
