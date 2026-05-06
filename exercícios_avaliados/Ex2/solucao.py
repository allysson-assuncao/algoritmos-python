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
    # ...
    return custo

#Define aqui a função para resolver o Exercícios 2:
def constroiGuloso(n, matrizDist, fs):
    # n: numero de cidades:  de 0..n
    # matrizDist: matrix nxn de distâncias
    # fs: função de avaliação da solução
    s = []
    # ...

    return s

# Gera vizinhança de uma solução s, fazendo movimentos de troca (swap).
def NS_swap(s, n):
    return s[:n], s[n:]
# s: a lista ou array de elementos
# n: o número de elementos de s

#retorno: lista contendo todas as soluções vizinhas

# Gera vizinhança de uma solução s, fazendo movimentos de insercao.
def NS_insertion(s, n):
    return None
# s: a lista ou array de elementos
# n: o número de elementos de s

#retorno: lista contendo todas as soluções vizinhas

# Método da descida com Best Improvement
def descida():
    return None

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
