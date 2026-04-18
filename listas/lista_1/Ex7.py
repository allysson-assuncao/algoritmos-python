import itertools

def gerar_permutacoes():
    elementos = ['A', 'B', 'C', 'D', 'E']

    print("=== PERMUTAÇÕES ===")
    print("Regra: A ordem dos elementos IMPORTA (Ex: ABC é diferente de CBA).")
    print(f"Conjunto base: {elementos}\n")

    # Gera todas as permutações possíveis (usando os 5 elementos)
    permutacoes = list(itertools.permutations(elementos))

    print(f"Total de permutações possíveis: {len(permutacoes)}")
    print("Exibindo todas as possibilidades:")

    for i, p in enumerate(permutacoes[:]):
        print(f"{i+1:03d}. {p}")

gerar_permutacoes()