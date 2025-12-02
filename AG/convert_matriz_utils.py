import os
class TratamentoMatriz:

    @staticmethod
    #método de classe,apenas faz uma "conta básica"
    def distancia(a,b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def __init__(self,usarBR58=False):
        """
        Lê o arquivo de entrada e guarda:
        - nrows  → número de linhas
        - matriz → matriz original em formato de lista de listas

        """
        self.usar_br58 = usarBR58
        self.caminho= "entrada.txt"


        if usarBR58:
            self.chaves, self.matriz_adjacencia = self.carregar_br58()
        else:
            self.nrows, self.ncols, self.matriz = self.ler_matriz_arquivo()
            self.chaves,self.matriz_adjacencia=self.converter_matriz()

        


    def ler_matriz_arquivo(self):
        try:
            caminho_absoluto = os.path.join(os.path.dirname(__file__), self.caminho)
            with open(caminho_absoluto, "r", encoding="utf-8") as f:
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
                    #celula="nome da posição"=A,B,C...
                    pontos[celula] = (i, j)#valor de i e j seria o valor das coordenadas

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

        #matriz convertida é a matriz de adjacência
        #chaves ordenadas é =#chaves=['R', 'A', 'B', 'C', 'D']
    @staticmethod
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

    def get_resultados(self):
        
        return self.chaves,self.matriz_adjacencia
    

    
    def carregar_br58(self):
        """
        Lê um arquivo TSPLIB no formato:
        EDGE_WEIGHT_TYPE: EXPLICIT
        EDGE_WEIGHT_FORMAT: UPPER_ROW

        Constrói e retorna a matriz de adjacência completa 58×58.
        """

        base_dir = os.path.dirname(os.path.abspath(__file__))
        arquivo_br58 = os.path.join(base_dir, "edgesbrasil58.tsp")

        with open(arquivo_br58, "r") as f:
            linhas = f.readlines()

        # 1. Ignorar cabeçalho até encontrar EDGE_WEIGHT_SECTION
        idx = 0
        while idx < len(linhas) and "EDGE_WEIGHT_SECTION" not in linhas[idx]:
            idx += 1

        if idx == len(linhas):
            raise ValueError("EDGE_WEIGHT_SECTION não encontrado no arquivo TSPLIB.")

        idx += 1  # primeira linha dos dados numéricos

        # 2. Carregar todos os números da upper row
        upper_values = []
        for i in range(idx, len(linhas)):
            linha = linhas[i].strip()
            if linha == "EOF":
                break
            if linha == "":
                continue
            nums = linha.split()
            for n in nums:
                upper_values.append(int(n))

        # 3. Reconstruir matriz 58×58
        N = 58
        matriz = [[0] * N for _ in range(N)]

        k = 0
        for i in range(N):
            for j in range(i + 1, N):
                matriz[i][j] = upper_values[k]
                matriz[j][i] = upper_values[k]
                k += 1

        if k != (N * (N - 1)) // 2:
            raise ValueError("Quantidade incorreta de valores para UPPER_ROW.")

        chaves = list(range(N))

        return chaves, matriz
