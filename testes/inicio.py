import sys
import math

def play_game():
    number = 23
    running = True
    while running:

        guess = int(input("Enter and integer: "))

        if guess == number:
            print('Congratulations! You guessed the number!')
            print('(but you do not win any prizes...)')

        elif guess < number:
            print('No, it is a little higher than that')

        else:
            print('No, it is a little lower than that')

    else:
        print('The while loop is over')

    print('Done')

def for_in_test():
    fruits = ['apple', 'banana', 'cherry']
    for x in fruits:
        print(x)

def comprehensive_list():
    list_test = [i for i in range(10) if i % 2 == 0]
    for x in list_test:
        print(x)

    lista_de_compra = []
    i = 0
    continua = True
    resposta = ''
    while continua:
        lista_de_compra.append(input("De o item["+ str(i) +"]: "))
        i += 1
        print("\nMais itens? (S/N):")
        resposta = input().strip().upper()
        continua = (resposta[0]) == 'S'

    print("\nLista em ordem alfabetica: ")
    lista_de_compra.sort()
    print(lista_de_compra)

    print("\nLista em ordem alfabetica invertida: ")
    lista_de_compra.reverse()
    print(lista_de_compra)

    tam = int(input("Dê tamanho da lista: "))
    lista_de_compra = [input("Dê o produto: ") for i in range(tam)]

def lista_de_dicionarios():
    lista_de_compra = []
    i = 0
    continua = True
    resposta = ''
    item_de_compra = {
        "descrição": "",
        "qtde": 0.0
    }

    while continua:
        item_de_compra["descrição"] = input("De o item["+str(i)+"]:")
        item_de_compra["qtde"] = input("Qtde["+str(i)+"]:")

        lista_de_compra.append(item_de_compra)
        i+=1
        print("\nMais itens (S/N): ")
        resposta = input().strip().upper()
        continua = (resposta[0]) == 'S'

    print("\nLista de compra: ")
    print(lista_de_compra)

def matriz_comprehension():
    m = [[int(input("De m["+str(i)+", "+str(j)+"]:")) for i in range(3)] for j in range(3)]

    for x in m:
        print("[")
        for y in x:
            print(str(y) + ", ")
        print("]")

def sum_two_numbers(a, b):
    return a + b

def fib(n):
    result = []
    a = 1
    b = a
    while a < n:
        result.append(a)
        tmp_var = b

    return  result

if __name__ == '__main__':
    # matriz_comprehension()
    for x in sys.path:
        print(x)

