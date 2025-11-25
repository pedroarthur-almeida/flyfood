
from python_tsp.heuristics import solve_tsp_local_search
import numpy as np



class TratamentoMatriz:

    @staticmethod
    #método de classe,apenas faz uma "conta básica"
    def distancia(a,b,):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def __init__(self):
        """
        Lê o arquivo de entrada e guarda:
        - nrows  → número de linhas
        - ncols  → número de colunas
        - matriz → matriz original em formato de lista de listas

        """
        self.caminho="AG/entrada.txt"
        self.nrows, self.ncols, self.matriz = self.ler_matriz_arquivo()

        self.chaves,self.matriz_adjacencia=self.converter_matriz()
        self.permutacao,self.distancia_total=self.matriz_tsp()


    def ler_matriz_arquivo(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                linhas = [ln.strip() for ln in f if ln.strip()]
        except FileNotFoundError:
            raise FileNotFoundError("Arquivo não encontrado.")

        if not linhas:
            raise ValueError("Arquivo vazio.")

        try:
            nrows, ncols = map(int, linhas[0].split())
        except Exception:
            raise ValueError("Cabeçalho inválido. Esperado: 'linhas colunas'.")

        if nrows <= 0 or ncols <= 0:
            raise ValueError("Dimensões inválidas da matriz.")

        matriz = []
        for i in range(1, 1 + nrows):
            if i < len(linhas):
                tokens = linhas[i].split()
                if len(tokens) == 1 and len(tokens[0]) == ncols:
                    elementos = list(tokens[0])
                else:
                    elementos = tokens
                if len(elementos) > ncols:
                    raise ValueError(f"Linha {i} com colunas a mais.")
                while len(elementos) < ncols:
                    elementos.append("0")
                matriz.append(elementos[:ncols])
            else:
                matriz.append(["0"] * ncols)

        return nrows, ncols, matriz



    

    def converter_matriz(self):
        """
        Converte a matriz original em:

        - chaves_ordenadas → ["R", "A", "B", ...]
        - matriz_convertida → matriz de adjacência com distâncias Manhattan
        """

        # 1. Achar posições de todos os pontos da matriz
        pontos = {}
        for i, linha in enumerate(self.matriz):
            for j, celula in enumerate(linha):
                if celula != "0":
                    pontos[celula] = (i, j)

        # 2. Criar lista de pontos ignorando 'R'
        lista = []
        for k in pontos:
            if k != "R":
                lista.append(k)

        # 3. Ordenar e colocar 'R' primeiro
        chaves_ordenadas = ["R"] + sorted(lista)

        # 4. Criar matriz de adjacência
        matriz_convertida = []
        for a in chaves_ordenadas:
            linha = []
            for b in chaves_ordenadas:
                if a == b:
                    linha.append(0)
                else:
                    #chamamento de um static method
                    linha.append(TratamentoMatriz.distancia(pontos[a], pontos[b]))
            matriz_convertida.append(linha)

        return chaves_ordenadas, matriz_convertida


    def matriz_tsp(self):
        matriz_np = np.array(self.matriz_adjacencia) 
        #Conversão para NumPy,pois a biblioteca usada trabalha melhor nesse formato
        #de array
        """
    array(
            [ 
            [0, 2, 3, 5],
            [2, 0, 4, 1],
            [3, 4, 0, 2],
            [5, 1, 2, 0]
            ]
            )

        """
        permutacao, distancia_total = solve_tsp_local_search(matriz_np)

        """
        A função solve_tsp_local_search resolve o Problema do Caixeiro Viajante (TSP) usando heurísticas de busca local. 
        Ela recebe como entrada uma matriz de adjacência (representada como um numpy.array) onde cada posição [i][j] 
        indica a distância do ponto i para o ponto j.

        O algoritmo tenta encontrar uma rota de menor custo que visita todos os pontos exatamente uma vez, 
        retornando dois resultados:

        permutation - uma lista de inteiros que representa a ordem dos pontos que devem ser visitados.
        Esses inteiros são índices da matriz, não os nomes originais dos pontos.
        Exemplo: [0, 2, 1, 3].

        distance - um número que representa o custo total da rota calculada, obtido somando as distâncias da matriz seguindo a ordem indicada pela permutação.

        O método não garante encontrar a solução ótima absoluta (pois é heurístico), mas encontra soluções rápidas e de 
        boa qualidade usando operações como troca de vizinhos, reversão de trechos da rota e outras técnicas de otimização local.
    
        permutacao = [0, 3, 1, 2] -->índices da permutação
        distancia_total = 17 -->distância calculada
    
        """

        return permutacao, distancia_total

    def get_resultados(self):
        return self.permutacao,self.distancia_total,self.chaves,self.matriz_adjacencia
        