def solucao1():

    m = [[[int(input(f"Valor para m[{i}][{j}][{k}]: "))
           for k in range(2)]
          for j in range(3)]
         for i in range(3)]

    print("\nConteúdo da estrutura 3D:")
    print(m)

if __name__ == '__main__':
    solucao1()
