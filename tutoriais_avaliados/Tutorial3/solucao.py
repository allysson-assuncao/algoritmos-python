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
matrizDistancias = gera_matriz_dist(data, cidades)


def fs(s, matrizDistancias):
    custo = 0
    for i in range(1, len(s)):
        custo = custo + matrizDistancias[s[i - 1], s[i]]
    custo = custo + matrizDistancias[s[-1], s[0]]
    return custo


def constroiAleatorio(n, matrizDist, fs):
    # n: numero de cidades:  de 0..n
    # matrizDist: matrix nxn de distâncias
    # fs: função de avaliação da solução
    s = []
    lista_cidades = [i for i in range(n)]
    while (len(s) < (n - 1)):
        idx = np.random.randint(0, len(lista_cidades))
        s = s + [lista_cidades[idx]]
        lista_cidades.remove(lista_cidades[idx])
    s = s + [lista_cidades[0]]
    return s


# aleatoriamente duas posições de s e faça a troca
def NS_aleatorio(s, n):
    # s: a lista ou array de elementos
    # n: o número de elementos de s
    while True:
        c1 = np.random.randint(n)
        c2 = np.random.randint(n)
        if (c1 != c2):
            break
    cid_aux = s[c1]
    s[c1] = s[c2]
    s[c2] = cid_aux  # s[c1]
    # retorno: uma solução da vizinhança
    return


# teste
NS_aleatorio([1, 2, 3, 7], 4)


# Metaheurística Simulated Annealing (SA)
def SA(fs, NS_aleatorio, alpha, SAMax, T0, s_inicial, matrizDistancias):
    # s_inicial: conjunto de cidades (solução inicial)

    # É fundamental trabalhar com cópias para não corromper a solução original
    s_atual = s_inicial.copy()
    custo_atual = fs(s_atual, matrizDistancias)

    melhor_s = s_atual.copy()
    melhor_custo = custo_atual

    T = T0
    T_final = 0.01
    n = len(s_atual)

    while T > T_final:
        for iteracao in range(SAMax):
            # Gera um vizinho usando uma CÓPIA para não alterar s_atual prematuramente
            vizinho = s_atual.copy()
            NS_aleatorio(vizinho, n)  # Altera a variável 'vizinho' in-place
            custo_vizinho = fs(vizinho, matrizDistancias)

            delta = custo_vizinho - custo_atual

            # Aceita se houver melhoria (delta negativo)
            if delta < 0:
                s_atual = vizinho.copy()
                custo_atual = custo_vizinho

                # Atualiza o melhor global
                if custo_vizinho < melhor_custo:
                    melhor_s = vizinho.copy()
                    melhor_custo = custo_vizinho
            else:
                # Se for pior, calcula a probabilidade de aceitação baseada na temperatura
                x = np.random.uniform(0, 1)
                probabilidade = math.exp(-delta / T)

                if x < probabilidade:
                    s_atual = vizinho.copy()
                    custo_atual = custo_vizinho

        # Resfriamento: reduz a temperatura
        T = T * alpha

    return melhor_s, melhor_custo


n_cidades = len(cidades)
SAMax = 2 * n_cidades

# Gera UMA solução inicial comum para todos os experimentos (base justa de comparação)
s_inicial = constroiAleatorio(n_cidades, matrizDistancias, fs)
custo_inicial = fs(s_inicial, matrizDistancias)


def rodar_experimentos_e_plotar(experimentos, s_inicial, titulo_extra=""):
    resultados_custo = []
    legendas_s = []

    for i, (alpha, T0) in enumerate(experimentos):
        np.random.seed(42 + i)
        s_final, custo_final = SA(fs, NS_aleatorio, alpha, SAMax, T0, s_inicial, matrizDistancias)
        resultados_custo.append(custo_final)
        legendas_s.append(f"s{i + 1}: {s_final[:5]}...")
        print(f"Exp {i + 1} (alpha={alpha}, T0={T0:.2f}) -> Custo Final: {custo_final:.2f}")

    labels = [f's{i + 1}' for i in range(len(experimentos))]
    cores = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B2'][:len(experimentos)]

    plt.figure(figsize=(10, 6))
    barras = plt.bar(labels, resultados_custo, color=cores)

    plt.xlabel('Soluções Finais dos Experimentos')
    plt.ylabel('Custo f(s) - Menor é melhor')
    plt.title(f'SA para 50CSP, SAMax={SAMax} {titulo_extra}')

    for bar in barras:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 5, f'{yval:.1f}', ha='center', va='bottom')

    plt.legend(barras, legendas_s, title="Início da Rota (Amostra)", loc='upper right')

    plt.ylim(min(resultados_custo) * 0.8, max(resultados_custo) * 1.2)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


# 4 Parâmetros distintos para testar: (alpha, T0)
experimentos_iniciais = [
    (0.90, 100),
    (0.95, 500),
    (0.98, 1000),
    (0.99, 5000)
]

print(f"Custo Inicial Aleatório: {custo_inicial:.2f}\n")
print("--- Experimentos Passo 4 ---")
rodar_experimentos_e_plotar(experimentos_iniciais, s_inicial, titulo_extra="(Definido Manualmente)")


# 5. Estimação de T0 empírica (Máxima Variação)
def estimar_T0_empirico(s_inicial, matrizDistancias, NS_aleatorio, n_iteracoes=100):
    n = len(s_inicial)
    max_delta = 0
    s_temp = s_inicial.copy()

    for _ in range(n_iteracoes):
        custo_antes = fs(s_temp, matrizDistancias)
        vizinho = s_temp.copy()
        NS_aleatorio(vizinho, n)
        custo_depois = fs(vizinho, matrizDistancias)

        delta = custo_depois - custo_antes
        if delta > max_delta:
            max_delta = delta

        s_temp = vizinho.copy()

    # Assume-se que a probabilidade inicial de aceitar a pior transição seja de 50% (0.5)
    # math.exp(-max_delta / T0) = 0.5  ->  T0 = -max_delta / ln(0.5)
    T0_estimado = -max_delta / math.log(0.5)
    return T0_estimado


T0_empirico = estimar_T0_empirico(s_inicial, matrizDistancias, NS_aleatorio)
print(f"\nTemperatura T0 Estimada (Slide 10): {T0_empirico:.2f}")

experimentos_empiricos = [
    (0.90, T0_empirico),
    (0.95, T0_empirico),
    (0.98, T0_empirico),
    (0.99, T0_empirico)
]
print("--- Experimentos Passo 5 (T0 Empírico) ---")
rodar_experimentos_e_plotar(experimentos_empiricos, s_inicial, titulo_extra=f"(T0={T0_empirico:.2f} Empírico)")


# 6. Estimação de T0 usando simulação para Gama = 0.95
def estimar_T0_gamma(s_inicial, matrizDistancias, NS_aleatorio, gamma=0.95, n_iteracoes=500):
    n = len(s_inicial)
    s_temp = s_inicial.copy()

    soma_deltas_positivos = 0
    quantidade_pioras = 0

    for _ in range(n_iteracoes):
        custo_antes = fs(s_temp, matrizDistancias)
        vizinho = s_temp.copy()
        NS_aleatorio(vizinho, n)
        custo_depois = fs(vizinho, matrizDistancias)

        delta = custo_depois - custo_antes

        # Só consideramos as transições que PIORAM a solução
        if delta > 0:
            soma_deltas_positivos += delta
            quantidade_pioras += 1

        # O random walk continua independente de melhora/piora para amostrar o espaço
        s_temp = vizinho.copy()

    if quantidade_pioras == 0:
        return 1000  # Fallback caso a rotação não ache pioras (raríssimo)

    media_deltas = soma_deltas_positivos / quantidade_pioras

    # Formula de Kirkpatrick/Aarts: T0 = - média_deltas / ln(gamma)
    T0_gamma = -media_deltas / math.log(gamma)
    return T0_gamma


T0_otimizado = estimar_T0_gamma(s_inicial, matrizDistancias, NS_aleatorio, gamma=0.95)
print(f"\nTemperatura T0 Simulada para Gama 0.95 (Slide 11): {T0_otimizado:.2f}")

experimentos_simulados = [
    (0.90, T0_otimizado),
    (0.95, T0_otimizado),
    (0.98, T0_otimizado),
    (0.99, T0_otimizado)
]
print("--- Experimentos Passo 6 (T0 J.M. 0.95) ---")
rodar_experimentos_e_plotar(experimentos_simulados, s_inicial, titulo_extra=f"(T0={T0_otimizado:.2f} Simulação)")
