from rotas_utils import distancia
from python_tsp.heuristics import solve_tsp_local_search
import numpy as np
import random


#Matriz, por enquanto coloequei um exemplo
matriz = [
        ["0", "0", "A", "0", "B"],
        ["0", "E", "0", "0", "0"],
        ["0", "C", "0", "D", "0"],
        ["0", "0", "0", "0", "0"],
        ["R", "0", "0", "0", "0"]
    ]


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
        if copia and copia[0] == "R":
            copia.pop(0)
        random.shuffle(copia)
        individuo = ["R"]+copia+["R"]
        inverso = ["R"]+ copia[::-1]+["R"]
        if individuo not in aleatorios and inverso not in aleatorios:
            aleatorios.append(individuo)
        tentativas +=1
        
    return aleatorios


#Gerar rota Vizinho mais proximo
def NN(matriz):
    start = 0
    chaves, matriz_convertida = converter_matriz(matriz)
    numero_pontos = len(matriz_convertida)
    rota = [start]
    nao_visitados = set(range(1, numero_pontos)) #os nao visitados, menos o 0
    atual = start

    while nao_visitados:
        menor = None
        melhor_distancia = float("inf") 
        for possibilidade in nao_visitados: #percorsse as possibilidades entre os nao visitados
            distanciaAtual = matriz_convertida[atual][possibilidade]
            if distanciaAtual < melhor_distancia:
                melhor_distancia = distanciaAtual
                menor = possibilidade
        #add o escolhido e atualiza
        rota.append(menor)
        nao_visitados.remove(menor)
        atual = menor
    rota.append(start)

    return rota

def juntarRotas(chaves, matriz):
    #gera as rotas aleatorias
    rotasAleatorias = gerar_individuos_aleatorios(chaves)
    # converter_matriz para obter mapeamento label -> índice
    chaves_list, matriz_convertida = converter_matriz(matriz)
    label_to_indice = {label: index for index, label in enumerate(chaves_list)} #cria um dicioonario relacionando a "letra" com o seu valor
    #Converte as rotas aleatorias para indices
    aleatoriasIndices = []
    for rota_labels in rotasAleatorias:
        rota_indice = [label_to_indice[label] for label in rota_labels]
        aleatoriasIndices.append(rota_indice)
    # obtém rota NN (já em índices) e junta
    rota_nn = NN(matriz)

    rotas = aleatoriasIndices + [rota_nn]
    return rotas


def opt2(rotas=None, chaves=None, matriz=None):

    # --- sempre cria matriz_convertida ---
    if matriz is None:
        raise ValueError("É necessário fornecer 'matriz' para o opt2.")
     
    chaves_list, matriz_convertida = converter_matriz(matriz)

    # --- se rotas não foi informado, gera ---
    if rotas is None:
        if chaves is None:
            raise ValueError("É necessário fornecer 'chaves' quando rotas for None.")
        rotas = juntarRotas(chaves, matriz)

    populacao_inicial = []

    # --- aplica 2-opt em cada rota ---
    for rota in rotas:
        n = len(rota)

        # função interna sempre tem acesso à matriz_convertida agora
        def ganho_troca(rota_local, i, j):
            a, b = rota_local[i - 1], rota_local[i]
            c, d = rota_local[j], rota_local[j + 1]

            antes = matriz_convertida[a][b] + matriz_convertida[c][d]
            depois = matriz_convertida[a][c] + matriz_convertida[b][d]

            return depois - antes

        melhorou = True
        while melhorou:
            melhorou = False

            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    ganho = ganho_troca(rota, i, j)
                    if ganho < 0:
                        rota[i:j+1] = reversed(rota[i:j+1])
                        melhorou = True
                        break
                if melhorou:
                    break

        populacao_inicial.append(rota)

    return populacao_inicial

