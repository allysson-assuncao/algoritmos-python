import sys
import time
import numpy as np
import math
import matplotlib.pyplot as plt

np.random.seed(1000)


def le_arq_vetor(arquivo):
    v = []
    with open(arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        # print(linhas)
    for linha in linhas:
        l = linha.split()
        v.append((int(l[0]), int(l[1]), int(l[2])))
    return np.array(v)


def gera_matriz_dist(data, cid):
    num_cid = cid.shape[-1]
    dist = np.zeros((num_cid, num_cid))
    for i in np.arange(num_cid):
        for j in np.arange(num_cid):
            dist[i, j] = np.sqrt(data[i][1] * data[j][1] + data[i][2] * data[j][2])
            dist[j, i] = dist[i, j]
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
        proxima_cidade = int(s[i + 1])
        custo += dist[cidade_atual, proxima_cidade]

    # Adiciona a distância da última cidade de volta para a primeira (origem)
    cidade_final = int(s[-1])
    cidade_origem = int(s[0])
    custo += dist[cidade_final, cidade_origem]

    return custo

# Define aqui a função para resolver o Exercícios 2:
def constroiAleatorio(n, matrizDist, fs):
    # n: numero de cidades:  de 0..n
    # matrizDist: matrix nxn de distâncias
    # fs: função de avaliação da solução

    # Cria uma lista com as cidades de 0 até n-1
    s = list(range(n))

    # Embaralha a lista aleatoriamente
    np.random.shuffle(s)

    return s


# Função para obter uma solução vizinha de s, da seguinte maneira: sorteie
# aleatoriamente duas posições de s e faça a troca
# Função para obter uma solução vizinha de s, da seguinte maneira: sorteie
# aleatoriamente duas posições de s e faça a troca
def NS_swap_aleatorio(s, n):
    # s: a lista ou array de elementos
    # n: o número de elementos de s
    vizinho = list(s)

    # Sorteia 2 posições distintas sem reposição
    i, j = np.random.choice(n, size=2, replace=False)

    # Realiza o swap (troca)
    vizinho[i], vizinho[j] = vizinho[j], vizinho[i]

    return vizinho


# Método da descida com Best Improvement (adaptado para busca aleatória)
def descidaRandomica(fs, NS_swap_aleatorio, s, IterMax=1000):
    # fs: funcao que devolve o custo de uma solucao
    # NS_swap_aleatorio: função para obter uma solução vizinha de forma aleatória para o TSP
    # s: conjunto de cidades (solução inicial)

    s_atual = s
    custo_atual = fs(s_atual)
    n = len(s_atual)
    iteracoes_sem_melhora = 0

    while iteracoes_sem_melhora < IterMax:
        # Gera apenas UM vizinho aleatório
        vizinho = NS_swap_aleatorio(s_atual, n)
        custo_vizinho = fs(vizinho)

        # Se o vizinho for melhor, aceita o movimento e zera o contador
        if custo_vizinho < custo_atual:
            s_atual = vizinho
            custo_atual = custo_vizinho
            iteracoes_sem_melhora = 0
        else:
            # Se não houve melhora, incrementa o contador de parada
            iteracoes_sem_melhora += 1

    return s_atual


# Metaheurística Multistart
def multistart(fs, constroiAleatorio, descidaRandomica, s, criterioParada=10000):
    # fs: funcao que devolve o custo de uma solucao
    # constroiAleatorio: constrói uma solução inicial aleatória
    # descidaRandomica: função para refinar a solucao obtida
    # s: conjunto de cidades (usado para extrair o tamanho n)

    n = len(s)
    melhor_s_global = None
    melhor_custo_global = float('inf')
    iteracoes_sem_melhora = 0

    # Assumindo que a matriz 'dist' está disponível no escopo global
    # para passar para a função construtiva
    global dist

    while iteracoes_sem_melhora < criterioParada:
        # 1. Fase de Construção: Gera nova solução inicial aleatória
        s_inicial = constroiAleatorio(n, dist, fs)

        # 2. Fase de Busca Local: Refina a solução inicial
        s_refinada = descidaRandomica(fs, NS_swap_aleatorio, s_inicial)
        custo_refinada = fs(s_refinada)

        # 3. Atualização: Verifica se o ótimo local encontrado é o melhor global
        if custo_refinada < melhor_custo_global:
            melhor_s_global = s_refinada
            melhor_custo_global = custo_refinada
            iteracoes_sem_melhora = 0  # Reseta o critério de parada global
        else:
            iteracoes_sem_melhora += 1

    return melhor_s_global


def leInt(msg):
    return int(input(msg))
