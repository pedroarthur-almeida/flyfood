RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"


def ler_matriz_arquivo(caminho):
    #função utilizada para ler a matriz
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = [ln.strip() for ln in f if ln.strip()]
            #usando o for,vai adicionando numa lista "linhas" as linhas da matriz de entrada
            #["5 5","...","..."]
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo não encontrado.")

    #se não existir nada no arquivo,retornar que o arquivo não existe
    if not linhas:
        raise ValueError("Arquivo vazio.")

    try:
        #função map aplica a função para algum interável
        #map(função,interavel)
        #buscará ler a quantidade de linhas e colunas respectivamente
        #pega o valor de índice 0 na lista ois é o valor da dimensão da matriz
        nrows, ncols = map(int, linhas[0].split())
    except Exception:
        raise ValueError("Cabeçalho inválido. Esperado: 'linhas colunas'.")

    if nrows <= 0 or ncols <= 0:
        #verifica se as dimensões de linhas e colunas são validas
        raise ValueError("Dimensões inválidas da matriz.")

    matriz = []

    #loop responsável por retornar a matriz já organizada em formato de matriz padrão
    for i in range(1, 1 + nrows):
        #irá percorrer os índices da lista linhas começando do 1,pois zero
        #é a parte da dimensão da matriz
        
        #verifica se a linha existe no arquivo
        if i < len(linhas):
            #guarda a linha em uma lista token
            tokens = linhas[i].split()
            #se só tiver um elemento na lista token e verifica se o número de caracteres
            #corresponde ao número de colunas caso a matriz esteja toda colada
            #ex=R000A invés de R 0 0 0 A
            if len(tokens) == 1 and len(tokens[0]) == ncols:
                #lista os elementos,separando cada um
                elementos = list(tokens[0])
            else:
                #apenas guarda a lista em uma variável elementos
                #ex=["R","0","0","0","A"]
                elementos = tokens
            
            #verifica se a quantidade de elementos bate com a quantidadde de colunas
            if len(elementos) > ncols:
                raise ValueError(f"Linha {i} com colunas a mais.")
            #se tiver menos elementos do que o esperado,vai adicionando 0 na lista elementos
            while len(elementos) < ncols:
                elementos.append("0")
            #adiciona na matriz apenas os elementos necessários,usando o fatiador
            matriz.append(elementos[:ncols])
        #caso a linha não exista no arquivo,vai colocando 0
        else:
            matriz.append(["0"] * ncols)

    return nrows, ncols, matriz


def encontrar_pontos(matriz):
    #função utilizada para encontrar as coordenadas na matriz
    pontos = {} # dicionário que guardará os pontos e suas coordenadas
    #{"R":"coordenada"}
    coords_ocupados = {}
    #percorrerá a matriz linha por linha=["R", "0", "0", "0", "A"]
    for i, linha in enumerate(matriz):
        #percorrerá cada valor="R" se j=0 dentro da linha
        for j, valor in enumerate(linha):
            if valor and valor != "0":
                #verifica se o caractere é válido
                if len(valor) != 1 or not valor.isalpha():
                    raise ValueError(f"Caractere inválido encontrado na posição {(i, j)}: {valor}")
                #verifica se existe letras duplicadas
                if valor in pontos:
                    raise ValueError(f"Letra duplicada encontrada: '{valor}' já em {pontos[valor]} e novamente em {(i, j)}")
                #verifica se tem mais de um ponto na mesma posição
                if (i, j) in coords_ocupados:
                    raise ValueError(f"Mais de um ponto na mesma posição {(i, j)}: '{coords_ocupados[(i, j)]}' e '{valor}'")


                #adiciona no dicionário ponto o valor=letra usada e as coordenadas dentro de 
                #cada lista(matriz em relação a linha e linha em relação a coluna)
                pontos[valor] = (i, j)
                #adiciona o inverso no dicionário coords_ocupados
                coords_ocupados[(i, j)] = valor
    return pontos