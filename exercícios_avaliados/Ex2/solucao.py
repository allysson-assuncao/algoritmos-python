import sys
import time
import numpy as np  # importa o pacote com 'alias' ou apelido de 'np'
import math
import matplotlib.pyplot as plt    # o módulo pyplot, parte do matplotlib, como plt
np.random.seed(1000)    ## produz o mesmos numeros 'pseudo'aleatórios a cada execução

def le_arq_vetor(arquivo):
    v = []
    with open(arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        #print(linhas)
    for linha in linhas:
        l = linha.split()
        v.append((int(l[0]), int(l[1]), int(l[2])))
    return np.array(v)

def gera_matriz_dist(data, cid):
    num_cid = cid.shape[-1]
    dist = np.zeros((num_cid,num_cid))
    for i in np.arange(num_cid):
        for j in np.arange(num_cid):
            dist[i, j] = np.sqrt(data[i][1]*data[j][1] + data[i][2]*data[j][2])
            dist[j, i] =  dist[i, j]
    return dist

def gera_vetor_cidades(data):
    cidades = np.zeros(data.shape[0])
    for i in np.arange(data.shape[0]):
        cidades[i] = data[i][0]
    return cidades

data = le_arq_vetor("C50.TXT")
cidades = gera_vetor_cidades(data)
dist = gera_matriz_dist(data, cidades)

# Avalia o custo de uma solução s do TSP simples (soma das distâncias)
def fs(s):
    custo = 0
    n = len(s)

    # Soma a distância de cada cidade para a próxima no caminho
    for i in range(n - 1):
        cidade_atual = int(s[i])
        proxima_cidade = int(s[i+1])
        custo += dist[cidade_atual, proxima_cidade]

    # Adiciona a distância da última cidade de volta para a primeira (origem)
    cidade_final = int(s[-1])
    cidade_origem = int(s[0])
    custo += dist[cidade_final, cidade_origem]

    return custo

def constroiGuloso(n, matrizDist, fs):
    # n: numero de cidades:  de 0..n
    # matrizDist: matrix nxn de distâncias
    # fs: função de avaliação da solução
    s = [0] # Partindo da cidade 0
    visitados = set([0])
    atual = 0

    while len(s) < n:
        menor_dist = float('inf')
        proxima_cidade = -1

        for i in range(n):
            if i not in visitados:
                if matrizDist[atual, i] < menor_dist:
                    menor_dist = matrizDist[atual, i]
                    proxima_cidade = i

        s.append(proxima_cidade)
        visitados.add(proxima_cidade)
        atual = proxima_cidade

    return s

# Gera vizinhança de uma solução s, fazendo movimentos de troca (swap).
def NS_swap(s, n):
    # s: a lista ou array de elementos
    # n: o número de elementos de s
    vizinhos = []

    for i in range(n - 1):
        for j in range(i + 1, n):
            # Cria uma cópia da solução atual
            vizinho = list(s)
            # Realiza a troca (swap)
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
            vizinhos.append(vizinho)

    return vizinhos # retorno: lista contendo todas as soluções vizinhas

# Gera vizinhança de uma solução s, fazendo movimentos de insercao.
def NS_insertion(s, n):
    # s: a lista ou array de elementos
    # n: o número de elementos de s
    vizinhos_unicos = set()

    for i in range(n):
        for j in range(n):
            if i != j:
                vizinho = list(s)
                # Remove o elemento da posição i
                elemento = vizinho.pop(i)
                # Insere o elemento na nova posição j
                vizinho.insert(j, elemento)

                # Adiciona como tupla no set para eliminar duplicatas automaticamente
                vizinhos_unicos.add(tuple(vizinho))

    # Converte as tuplas de volta para listas antes de retornar
    return [list(v) for v in vizinhos_unicos]

# Método da descida com Best Improvement
def descida(s_inicial, n, funcao_vizinhanca):
    s_atual = s_inicial
    custo_atual = fs(s_atual)
    melhoria = True

    while melhoria:
        melhoria = False
        vizinhos = funcao_vizinhanca(s_atual, n)

        melhor_vizinho = s_atual
        menor_custo_vizinhanca = custo_atual

        # Best Improvement: Avalia TODOS os vizinhos antes de decidir
        for vizinho in vizinhos:
            custo_vizinho = fs(vizinho)
            if custo_vizinho < menor_custo_vizinhanca:
                menor_custo_vizinhanca = custo_vizinho
                melhor_vizinho = vizinho

        # Se encontrou um vizinho melhor que o estado atual, move para ele
        if menor_custo_vizinhanca < custo_atual:
            s_atual = melhor_vizinho
            custo_atual = menor_custo_vizinhanca
            melhoria = True # Continua o loop procurando mais melhorias

    return s_atual, custo_atual

def leInt(msg):
    return int(input(msg))

def permutar(arr, i=0):
    if i == len(arr):
        print(arr)
        return

    for j in range(i, len(arr)):
        # troca elemento atual com o candidato
        arr[i], arr[j] = arr[j], arr[i]

        permutar(arr, i + 1)

        # desfaz a troca (backtrack)
        arr[i], arr[j] = arr[j], arr[i]

arr = ['a', 'b', 'c', 'd']
permutar(arr)

# 1. Gerar solução inicial com heurística construtiva
n_cidades = len(cidades)
solucao_inicial = constroiGuloso(n_cidades, dist, fs)
custo_inicial = fs(solucao_inicial)
print(f"Solução Inicial (Gulosa): Custo = {custo_inicial:.2f}")

# 2. Refinar usando Descida com Swap
solucao_final_swap, custo_final_swap = descida(solucao_inicial, n_cidades, NS_swap)
print(f"Refinamento (Swap): Custo = {custo_final_swap:.2f}")

# 3. Refinar usando Descida com Insertion
solucao_final_ins, custo_final_ins = descida(solucao_inicial, n_cidades, NS_insertion)
print(f"Refinamento (Insertion): Custo = {custo_final_ins:.2f}")
