# 1. ENTRADA E SAÍDA DE DADOS (I/O)
print("Olá, Mundo!")
nome = "Desenvolvedor"
idade = 30

print(f"Nome: {nome}, Idade: {idade}")

# entrada_usuario = input("Digite algo: ")

# 2. TIPOS DE DADOS E VARIÁVEIS

# Type Hinting (dicas de tipo)
texto: str = "Isso é uma string"
inteiro: int = 42
ponto_flutuante: float = 3.14
booleano: bool = True
nulo: None = None # Equivalente a null

# 3. CONVERSÃO DE TIPOS

num_str = "100"
num_int = int(num_str)      # "100" -> 100
num_float = float(num_int)  # 100 -> 100.0
texto_novo = str(num_float) # 100.0 -> "100.0"
bool_val = bool(1)          # 1 -> True (0, "", [], None são False)

# 4. OPERADORES

div_int = 10 // 3   # 3 (Divisão inteira)
mod  = 10 % 3       # 1 (Resto da divisão)
pot  = 2 ** 3       # 8 (Exponenciação)

# Lógicos
verdade = True and False  # AND (e) -> False
falso = True or False     # OR (ou) -> True
negacao = not True        # NOT (não) -> False

# 5. Operador Ternário

status = "Aprovado" if 50 >= 70 else "Reprovado"

# 6. LAÇOS DE REPETIÇÃO

for i in range(0, 5, 1):
    pass # 0, 1, 2, 3, 4 (pass é um comando nulo que não faz nada)

contador = 0
while contador < 3:
    contador += 1

for num in range(10):
    if num == 2:
        continue # Pula o 2
    if num == 5:
        break    # Interrompe no 5

# 7. FUNÇÕES

# Definição padrão com Type Hinting e valor padrão
def saudar(nome: str, saudacao: str = "Olá") -> str:
    """Docstring: Esta função retorna uma saudação."""
    return f"{saudacao}, {nome}!"

# *args (Múltiplos argumentos posicionais -> Tupla)
def somar_todos(*args):
    return sum(args) # sum() é uma função nativa

# **kwargs (Múltiplos argumentos nomeados -> Dicionário)
def exibir_dados(**kwargs):
    for chave, valor in kwargs.items():
        print(f"{chave}: {valor}")

# Função Lambda (Função anônima de uma linha)
dobro = lambda x: x * 2

# 8. ESTRUTURAS DE DADOS

# ---------------------------------------------------------
# A. LISTAS (List - Mutáveis, ordenadas, aceitam duplicatas)
# Atuam como vetores (arrays dinâmicos) em Python.
# ---------------------------------------------------------
frutas = ["maçã", "banana", "cereja"]
frutas.append("uva")        # Adiciona ao final
frutas.insert(1, "manga")   # Insere no índice 1
removido = frutas.pop()     # Remove e retorna o último elemento
frutas.remove("maçã")       # Remove a primeira ocorrência do valor

# Fatiamento (Slicing): lista[inicio:fim:passo]
primeiras = frutas[0:2]     # Pega índices 0 e 1
inverso = frutas[::-1]      # Inverte a lista

# List Comprehension (Maneira concisa de criar listas)
quadrados = [x**2 for x in range(5)] # [0, 1, 4, 9, 16]

# B. MATRIZES (Listas de Listas)
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
elemento_5 = matriz[1][1] # Acessando a linha 1, coluna 1 (índice começa em 0)

# C. TUPLAS (Tuple - Imutáveis, ordenadas)
# Usadas para dados que não devem ser alterados.
coordenadas = (10.0, 20.0)
# coordenadas[0] = 15.0  # Isso geraria um erro (TypeError)

# Desempacotamento de Tuplas (Unpacking)
x, y = coordenadas

# D. DICIONÁRIOS (Dict - Chave-Valor, mutáveis)
# Chaves devem ser únicas e imutáveis (strings, números, tuplas).
usuario = {
    "nome": "João",
    "idade": 25,
    "ativo": True
}

# Acessando e modificando
nome_user = usuario["nome"]
usuario["idade"] = 26             # Modifica valor
usuario["email"] = "j@email.com"  # Adiciona nova chave

# Métodos úteis de Dicionários
chaves = usuario.keys()           # Retorna as chaves
valores = usuario.values()        # Retorna os valores
itens = usuario.items()           # Retorna pares (chave, valor)
email = usuario.get("email", "Sem email") # Tenta pegar, se não achar retorna "Sem email"

# E. CONJUNTOS (Set - Não ordenados, valores ÚNICOS)
# Muito eficientes para verificar pertinência e remover duplicatas.
numeros_set = {1, 2, 3, 3, 4} # Fica apenas {1, 2, 3, 4}
numeros_set.add(5)
numeros_set.remove(2) # Gera erro se não existir. Use .discard(2) para evitar erro.

set_a = {1, 2, 3}
set_b = {3, 4, 5}

# Operações de Conjuntos (Teoria dos Conjuntos)
uniao = set_a | set_b         # {1, 2, 3, 4, 5} ou set_a.union(set_b)
intersecao = set_a & set_b    # {3}             ou set_a.intersection(set_b)
diferenca = set_a - set_b     # {1, 2}          ou set_a.difference(set_b)

if __name__ == "__main__":
    print("Guia de Referência Python carregado e pronto para uso.")