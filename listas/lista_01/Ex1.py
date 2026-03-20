a = [int(input("l=[" + str(i) + "]:")) for i in range(5)]

b = [int(input("r=[" + str(i) + "]:")) for i in range(5)]

pares = [(x1, x2) for x1 in a for x2 in b]

print("\nTuplas formadas pelos pares ordenados:")
for p in pares:
    print(p)