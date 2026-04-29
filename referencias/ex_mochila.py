def problema_2_mochila():
    print("=== Algoritmo Guloso: O Problema da Mochila ===")

    itens = [
        {"nome": "Notebook", "valor": 3, "peso": 2.5},
        {"nome": "Smartphone", "valor": 2, "peso": 0.5},
        {"nome": "Console de Videogame", "valor": 3.5, "peso": 3.0},
        {"nome": "Fone de Ouvido", "valor": 5, "peso": 0.3},
        {"nome": "Câmera DSLR", "valor": 1.5, "peso": 1.5},
        {"nome": "Livro Técnico", "valor": 2, "peso": 1.0}
    ]

    # 2. Entrada e Validação
    entrada_capacidade = input("Digite a capacidade máxima da mochila em kg (ex: 5.0): ")
    try:
        capacidade_mochila = float(entrada_capacidade)
    except ValueError:
        print("Erro: Por favor, digite um número válido.")
        return

    # 3. Algoritmo de Ordenação Manual
    n = len(itens)
    for i in range(n):
        for j in range(0, n - i - 1):

            # Variável de controle (booleana)
            deve_trocar = False

            # Critério 1: O valor do item atual é MENOR que o do próximo?
            # (Queremos os maiores valores primeiro, então trocamos)
            if itens[j]["valor"] < itens[j+1]["valor"]:
                deve_trocar = True

            # Critério 2: Os valores são IGUAIS?
            # (Desempate: queremos os de MENOR peso primeiro)
            elif itens[j]["valor"] == itens[j+1]["valor"]:
                if itens[j]["peso"] > itens[j+1]["peso"]:
                    deve_trocar = True

            # Operação de troca de elementos na lista (Swap)
            if deve_trocar:
                # Armazena o atual em uma variável temporária
                temp = itens[j]
                # Sobrescreve o atual com o próximo
                itens[j] = itens[j+1]
                # Coloca o que estava no atual (temp) na posição do próximo
                itens[j+1] = temp

    # Exibindo a lista após nossa ordenação manual
    print("\nItens disponíveis (Ordenados por Maior Valor -> Menor Peso):")
    for item in itens:
        print(f"- {item['nome']}: {item['valor']} | {item['peso']}kg")

    # 4. Lógica Gulosa (Preenchendo a mochila)
    mochila_selecionada = []
    peso_atual = 0.0
    valor_acumulado = 0.0

    # Iterando sobre a lista ordenada
    for item in itens:
        # Condição: Se eu adicionar este item, ultrapasso a capacidade?
        if peso_atual + item["peso"] <= capacidade_mochila:
            # Se não ultrapassa, coloco na mochila
            mochila_selecionada.append(item)
            peso_atual += item["peso"]
            valor_acumulado += item["valor"]

    # 5. Saída de Resultados
    print(f"\n--- Resultado da Mochila (Capacidade: {capacidade_mochila}kg) ---")

    # Verificando se a lista está vazia
    if len(mochila_selecionada) == 0:
        print("Nenhum item coube na mochila.")
    else:
        print("Itens adicionados:")
        for item in mochila_selecionada:
            print(f" -> {item['nome']} ({item['valor']} / {item['peso']}kg)")

        print("-" * 40) # Multiplicação de string (Cria uma linha divisória)
        print(f"Peso Total Ocupado: {peso_atual:.2f}kg") # Formatação de casas decimais
        print(f"Valor Total Acumulado: {valor_acumulado:.2f}")

# Executando a função
if __name__ == "__main__":
    problema_2_mochila()
