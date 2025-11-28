import os
class TratamentoMatriz:

    @staticmethod
    #método de classe,apenas faz uma "conta básica"
    def distancia(a,b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def __init__(self, caminho, usarBR58=False):
        """
        Lê o arquivo de entrada e guarda:
        - nrows  → número de linhas
        - matriz → matriz original em formato de lista de listas

        """
        self.usar_br58 = usarBR58
        self.caminho= caminho


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
        # Garante que acha o arquivo no mesmo diretório do script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_absoluto = os.path.join(base_dir, self.caminho)
        distancias = {}

        try:
            with open(caminho_absoluto, "r") as arq:
                linhas = arq.readlines()

            numeros_brutos = []
            lendo_dados = False

            for linha in linhas:
                linha = linha.strip()
                
                # Procura a marcação onde começam os números no padrão TSPLIB
                if "EDGE_WEIGHT_SECTION" in linha:
                    lendo_dados = True
                    continue
                
                # Se encontrar EOF, para
                if "EOF" in linha:
                    break
                
                # Se já passou pelo cabeçalho OU se a linha começa com número (caso sem cabeçalho)
                if lendo_dados or (linha and linha[0].isdigit()):
                    lendo_dados = True 
                    # Quebra a linha em pedaços e pega só o que for dígito
                    partes = linha.split()
                    for p in partes:
                        if p.isdigit():
                            numeros_brutos.append(int(p))

            # Agora distribui os números na lógica triangular superior
            iterador = iter(numeros_brutos)
            for i in range(1, 58):       # Linhas: cidade 1 a 57
                for j in range(i+1, 59): # Colunas: cidade i+1 a 58
                    try:
                        peso = next(iterador)
                        distancias[(i, j)] = peso
                        distancias[(j, i)] = peso
                    except StopIteration:
                        raise ValueError("O arquivo acabou antes de preencher a matriz 58x58.")

        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_absoluto}")

        # --- Montagem da Matriz Final (igual ao original) ---
        matriz = []
        for i in range(1, 59):
            linha = []
            for j in range(1, 59):
                if i == j:
                    linha.append(0)
                else:
                    linha.append(distancias.get((i, j), 0))
            matriz.append(linha)

        chaves = list(range(1, 59))  # cidades 1..58

        return chaves, matriz