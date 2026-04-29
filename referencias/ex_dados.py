import matplotlib.pyplot as plt

def lancamento_dados():
    print("=== Simulador de Probabilidade de Dados ===")

    # 1. Entrada de dados e Conversão (Casting)
    entrada = input("Digite o número de dados a serem lançados (ex: 2): ")
    n_dados = int(entrada) # Convertendo string para inteiro

    # Validação simples usando condicional
    if n_dados < 1:
        print("Você precisa lançar pelo menos 1 dado!")
        return

    # 2. Estrutura de Dados: Lista de Listas (Matriz)
    # Começamos com as 6 possibilidades do primeiro dado
    combinacoes = [[1], [2], [3], [4], [5], [6]]

    # 3. Laços de Repetição
    # Se n_dados for 2, o laço roda 1 vez. Se for 3, roda 2 vezes, etc.
    for i in range(1, n_dados):
        novas_combinacoes = []

        # Iteramos sobre as combinações existentes e adicionamos as faces de 1 a 6
        for combo in combinacoes:
            for face in range(1, 7): # range(1, 7) gera de 1 até 6
                # Cria uma nova lista fundindo a combinação anterior com a nova face
                novo_combo = combo + [face]
                novas_combinacoes.append(novo_combo)

        # Atualizamos a lista principal para o próximo dado
        combinacoes = novas_combinacoes

    # 4. Uso de Dicionários para contagem
    frequencias = {}

    for combo in combinacoes:
        # Calculando a soma "na mão" para demonstrar o uso de laços
        soma_atual = 0
        for valor in combo:
            soma_atual += valor

        # Condicional: se a soma já existe no dicionário, incrementa. Se não, cria com valor 1.
        if soma_atual in frequencias:
            frequencias[soma_atual] += 1
        else:
            frequencias[soma_atual] = 1

    # 5. Manipulação de Dicionários e Listas
    # Pegamos as chaves (somas) e ordenamos do menor para o maior
    somas_possiveis = sorted(frequencias.keys())

    # List Comprehension para pegar as frequências na ordem correta das chaves
    ocorrencias = [frequencias[soma] for soma in somas_possiveis]

    # Exibição de texto no terminal (f-strings)
    print(f"\nAnalisando {len(combinacoes)} combinações possíveis para {n_dados} dado(s):")
    for soma in somas_possiveis:
        print(f"Soma {soma}: {frequencias[soma]} ocorrências")

    # 6. Plotagem com matplotlib
    # Usamos o matplotlib apenas para a saída visual, como solicitado
    plt.bar(somas_possiveis, ocorrencias, color='skyblue', edgecolor='black')
    plt.title(f'Distribuição das Somas no Lançamento de {n_dados} Dado(s)')
    plt.xlabel('Soma das faces')
    plt.ylabel('Frequência (Nº de combinações)')

    # Garante que o eixo X mostre exatamente os números das somas
    plt.xticks(somas_possiveis)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    print("\nAbrindo o gráfico...")
    plt.show()

# Executando a função
if __name__ == "__main__":
    lancamento_dados()
