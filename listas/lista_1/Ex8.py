import itertools

def gerar_combinacoes():
    elementos = ['A', 'B', 'C', 'D', 'E']

    print("=== COMBINAÇÕES ===")
    print("Regra: A ordem dos elementos NÃO IMPORTA (Ex: ABC é igual a CBA).")
    print(f"Conjunto base: {elementos}\n")

    # Lista com os tamanhos de grupos solicitados
    tamanhos = [2, 3, 4, 5]

    for r in tamanhos:
        # Gera as combinações para o tamanho de grupo 'r'
        combinacoes = list(itertools.combinations(elementos, r))

        print(f"--- Agrupando de {r} em {r} elementos ---")
        print(f"Total de combinações: {len(combinacoes)}")

        # Exibe todas as combinações para este tamanho
        for i, c in enumerate(combinacoes):
            print(f"{i+1:02d}. {c}")

        print("-" * 40) # Linha divisória para facilitar a leitura

gerar_combinacoes()