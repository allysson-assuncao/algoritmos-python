print(" --- Questão 2 a) --- \n\n\n")

pesos = [2, 3, 5, 7, 4, 5, 1, 2, 8, 4, 5]
valores = [3, 4, 8, 10, 5, 9, 2, 4, 12, 5, 7]
capacidade = 23

itens = [{'nome': 'Item ' + str(i), 'valor': valores[i], 'peso': pesos[i]}  for i in range (len(valores))]

nomes_originais = [item['nome'] for item in itens]

def score(w_item, v_item, c_restante, alpha=1.0):
    pontuacao = v_item * (c_restante / w_item)
    return pontuacao

def resolver_mochila1():
    capacidade_restante = capacidade

    itens_selecionados = []
    itens_disponiveis = itens.copy()
    valor_total = 0
    peso_utilizado = 0

    print("--- Alocação Passo a Passo ---")
    passo = 1

    while True:
        # 1. Pegando somente os itens que ainda cabem na mochila
        candidatos_validos = [item for item in itens_disponiveis if item['peso'] <= capacidade_restante]

        if not candidatos_validos:
            break

        # 2. Seleciona o item com o melhor score
        maior_valor = -999999999
        melhor_item = None
        for candidato in candidatos_validos:
            valor_candidato = score(candidato['peso'], candidato['valor'], capacidade_restante)
            if valor_candidato > maior_valor:
                maior_valor = valor_candidato
                melhor_item = candidato

        # 3. Adiciona na mochila
        itens_selecionados.append(melhor_item['nome'])
        capacidade_restante -= melhor_item['peso']
        valor_total += melhor_item['valor']
        peso_utilizado += melhor_item['peso']

        pontuacao = score(melhor_item['peso'], melhor_item['valor'], capacidade_restante)
        print(f"Passo {passo}: Adicionado '{melhor_item['nome']}' (Score: {pontuacao:.2f}) | Espaço restante: {capacidade_restante}")

        itens_disponiveis.remove(melhor_item)
        passo += 1

    mochila_binaria = "".join(["1" if nome in itens_selecionados else "0" for nome in nomes_originais])

    print("\n--- Resultado Final ---")
    print(f"Itens selecionados     : {', '.join(itens_selecionados)}")
    print(f"Organização da mochila : {mochila_binaria}")
    print(f"Valor total alcançado  : {valor_total}")
    print(f"Peso total utilizado   : {peso_utilizado}")

resolver_mochila1()

print("\n\n\n --- Questão 4 a) --- \n\n\n")

def resolver_mochila2():

    capacidade_restante = capacidade

    itens_selecionados = []
    itens_disponiveis = itens.copy()
    valor_total = 0
    peso_utilizado = 0

    print("--- Alocação Passo a Passo ---")
    passo = 1

    while True:
        # 1. Pegando somente os itens que ainda cabem na mochila
        candidatos_validos = [item for item in itens_disponiveis if item['peso'] <= capacidade_restante]

        if not candidatos_validos:
            break

        # 2. Seleciona o item com a melhor razão Valor/Peso
        melhor_item = max(candidatos_validos, key=lambda x: (x['valor'] / x['peso'], x['valor']))

        # 3. Adiciona na mochila
        itens_selecionados.append(melhor_item['nome'])
        capacidade_restante -= melhor_item['peso']
        valor_total += melhor_item['valor']
        peso_utilizado += melhor_item['peso']

        razao = melhor_item['valor'] / melhor_item['peso']
        print(f"Passo {passo}: Adicionado '{melhor_item['nome']}' (Densidade: {razao:.2f}) | Espaço restante: {capacidade_restante}")

        itens_disponiveis.remove(melhor_item)
        passo += 1

    mochila_binaria = "".join(["1" if nome in itens_selecionados else "0" for nome in nomes_originais])

    print("\n--- Resultado Final ---")
    print(f"Itens selecionados     : {', '.join(itens_selecionados)}")
    print(f"Organização da mochila : {mochila_binaria}")
    print(f"Valor total alcançado  : {valor_total}")
    print(f"Peso total utilizado   : {peso_utilizado}")

resolver_mochila2()
