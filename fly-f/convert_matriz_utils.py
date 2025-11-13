from rotas_utils import distancia
from python_tsp.heuristics import solve_tsp_local_search
import numpy as np
import random

def converter_matriz(matriz):
    #Acha a posição dos pontos
    pontos = {}
    for i, linha in enumerate(matriz): #Passa pelas linhas
        for j, celula in enumerate(linha): #Passa por cada celula ou seja, as colunas nas linhas
            if celula != "0": #Se for vazia
                pontos[celula] = (i,j) #Coordenada
    lista = []
    for k in pontos:
        if k != "R":
            lista.append(k) #Pega os pontos, como ABCD... e adiciona o R no inicio
    chaves_ordenadas = ["R"] + sorted(lista)

    matriz_convertida = []
    for a in chaves_ordenadas:
        linha = [] #Monta as linhas
        for b in chaves_ordenadas: 
            if a==b:
                linha.append(0) #Adiciona 0 se a linha e a coluna forem iguais, ou seja
                                #Não há distancia entre um ponto e si mesmo
            else:
                linha.append(distancia(pontos[a], pontos[b]))
        matriz_convertida.append(linha) #Adciona as distancias entre os pontos nas linhas
    
    return chaves_ordenadas, matriz_convertida

def matriz_tsp(matriz_convertida):
    matriz_np = np.array(matriz_convertida)
    permutacao, distancia_total = solve_tsp_local_search(matriz_np)
    return permutacao, distancia_total

def salvar_como_tsplib(chaves, matriz, nome_arquivo="instancia.tsp"):
    n = len(chaves)
    with open(nome_arquivo, "w") as f:
        f.write(f"NAME: {nome_arquivo}\n")
        f.write("TYPE: TSP\n")
        f.write(f"DIMENSION: {n}\n")
        f.write("EDGE_WEIGHT_TYPE: EXPLICIT\n")
        f.write("EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
        f.write("EDGE_WEIGHT_SECTION\n")
        for linha in matriz:
            f.write(" ".join(map(str, linha)) + "\n")
        f.write("EOF\n")



def gerar_individuos_aleatorios(chaves):
    aleatorios = []
    tentativas = 0
    max_tentativas = 1000
    while len(aleatorios)  < 8*len(chaves) and tentativas < max_tentativas:
        copia = chaves[:]
        copia.pop(0)
        random.shuffle(copia)
        individuo = ["R"]+copia
        inverso = ["R"]+ copia[::-1]
        if individuo not in aleatorios and inverso not in aleatorios:
            aleatorios.append(individuo)
        tentativas +=1
        
    return aleatorios


# ===================== TESTE =====================
if __name__ == "__main__":
    matriz_exemplo = [
        ["0", "0", "A", "0", "B"],
        ["0", "E", "0", "0", "0"],
        ["0", "C", "0", "D", "0"],
        ["0", "0", "0", "0", "0"],
        ["R", "0", "0", "0", "0"]
    ]

    print("=== MATRIZ ORIGINAL ===")
    for linha in matriz_exemplo:
        print(linha)

    chaves, matriz_convertida = converter_matriz(matriz_exemplo)

    

    print("\n=== PONTOS ORDENADOS ===")
    print(chaves)

    print("\n=== MATRIZ DE DISTÂNCIAS ===")
    for linha in matriz_convertida:
        print(linha)

    permutacao, distancia_total = matriz_tsp(matriz_convertida)

    print("\n=== RESULTADO DO TSP (Heurística Local Search) ===")
    rota = [chaves[i] for i in permutacao]
    print("Rota encontrada:", " -> ".join(rota))
    print("Distância total:", round(distancia_total, 2))

    salvar_como_tsplib(chaves, matriz_convertida)
    print("\nArquivo 'instancia.tsp' salvo com sucesso!")

    print("Individuos aleatorios")
    print(gerar_individuos_aleatorios(chaves))
