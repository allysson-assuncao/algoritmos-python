def resolver_mochila():
    itens = [
        {'nome': 'A', 'valor': 5.2, 'peso': 5},
        {'nome': 'B', 'valor': 2.7, 'peso': 7},
        {'nome': 'C', 'valor': 7, 'peso': 10},
        {'nome': 'D', 'valor': 7.5, 'peso': 10},
        {'nome': 'E', 'valor': 6.1, 'peso': 9},
        {'nome': 'F', 'valor': 4.3, 'peso': 9.5},
        {'nome': 'G', 'valor': 3.1, 'peso': 4.9},
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

    print("\n--- Resultado ---")
    for item in itens:
        if item['peso'] <= capacidade:
            mochila_binaria += "1"
            print(item['nome'])
            capacidade -= item['peso']
            valor_total += item['valor']
            peso_utilizado += item['peso']
        else:
            mochila_binaria += "0"

    # 3. Exibir resultados
    print(f"\nOrganização da mochila : {mochila_binaria}")
    print(f"Valor total alcançado  : {valor_total}")
    print(f"Peso total utilizado   : {peso_utilizado}")

resolver_mochila()
