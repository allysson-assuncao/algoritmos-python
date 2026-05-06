def fatorial(n):
    fatorial = n
    for inteiro in range(n - 1, 1, -1):
        fatorial *= inteiro
    return fatorial

n = int(input("Qual número deseja calcular o fatorial? "))
print(fatorial(n))
