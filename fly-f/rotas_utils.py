def distancia(a, b):
    #cálculo de manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def gerar_permutacoes(seq):
    #se a lista de lugares for ==0 retorna uma lista de lista
    if len(seq) == 0:
        return [[]]
    if len(seq) == 1:
        #se tiver apenas um elemento,então só tem uma permutação
        return [seq[:]]
    perms = [] #cria a lista perms
    for i in range(len(seq)): # irá interar o for até chegar no tamanho da leitura da lista
        #pega o valor do i
        atual = seq[i]
        #pega o valor do que sobra e junta em uma lista só
        resto = seq[:i] + seq[i + 1 :]
        #chama recursivamente a função gerar permutações
        for p in gerar_permutacoes(resto):
            # vai adicionando tudo após a chamada recursiva a lista perms
            perms.append([atual] + p)
    #retorna a lista perms
    return perms


def calcular_rotas(pontos):
    #Cria um novo dicionário entregas que terá apenas os pontos de entrega,sem o R
    entregas = {k: v for k, v in pontos.items() if k != "R"}
    #pega apenas as chaves dos dicionários e coloca nuna lista
    letras = list(entregas.keys())
    if not letras:
        raise ValueError("Nenhum ponto de entrega encontrado.")
    rotas = []
    #puxa a função gerar permutação com a lista de lugares
    for perm in gerar_permutacoes(letras):
        #para cada elemento da lista retornada da função,o elemento será as permutações já feitas
        custo = 0 #custo inicial
        rota_completa = ["R"] + list(perm) + ["R"] # lista da rota completa de como deve ser
        for i in range(len(rota_completa) - 1): #irá interar o i até acabar o tamanho da lista -1
            #intera os pares consecutivos,indo somando R-->A-->B-->C--> até acabar,ma
            a, b = rota_completa[i], rota_completa[i + 1]
            # vai somando os custos 
            custo += distancia(pontos[a], pontos[b])
            #adiciona na lista de rotas
        rotas.append((rota_completa, custo))
    return rotas