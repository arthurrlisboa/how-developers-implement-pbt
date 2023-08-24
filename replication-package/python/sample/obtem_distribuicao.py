
intervalos = [
    (0, 298), (299, 301), (302, 313), (314, 316), (317, 322),
    (323, 327), (328, 338), (339, 361), (362, 442), (443, 450),
    (451, 453), (454, 494), (495, 509), (510, 519), (520, 523),
    (524, 527), (528, 537), (538, 547), (548, 548), (549, 555),
    (556, 557), (558, 565), (566, 568), (569, 603), (604, 627),
    (628, 635), (636, 643), (644, 649), (650, 653), (654, 763)
]


def calcular_distribuicao(numeros):
    distribuicao = [0] * len(intervalos)

    for numero in numeros:
        for i, intervalo in enumerate(intervalos):
            if numero >= intervalo[0] and numero <= intervalo[1]:
                distribuicao[i] += 1
                break
    
    for i, intervalo in enumerate(intervalos):
        print(f"{intervalo}: {distribuicao[i]}")

    intervalos_vazios = sum([1 for count in distribuicao if count == 0])
    print("Número de intervalos com 0 elementos:", intervalos_vazios)


def imprimir_numeros_por_intervalo(numeros):
    numeros_por_intervalo = [[] for _ in intervalos]

    for numero in numeros:
        for i, intervalo in enumerate(intervalos):
            if numero >= intervalo[0] and numero <= intervalo[1]:
                numeros_por_intervalo[i].append(numero)
                break
    
    for i, intervalo in enumerate(intervalos):
        print(f"{intervalo}: {numeros_por_intervalo[i]}")




