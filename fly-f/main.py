#Códigos ANSI para formatação de texto no terminal
BOLD = "\033[1m"       # Negrito
RESET = "\033[0m"      # Reseta o estilo
GREEN = "\033[32m"     # Verde
CYAN = "\033[36m"      # Ciano
YELLOW = "\033[33m"    # Amarelo
MAGENTA = "\033[35m"   # Magenta


#Função para ler a matriz a partir de um arquivo 
def ler_matriz_arquivo(caminho):
    try:
        #Abre o arquivo e remove espaços ou linhas vazias
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo não encontrado.")

    #Verifica se o arquivo não está vazio
    if not linhas:
        raise ValueError("Arquivo vazio.")

    try:
        #Primeira linha do arquivo contém o número de linhas e colunas
        nrows, ncols = map(int, linhas[0].split())
    except Exception:
        raise ValueError("Cabeçalho inválido. Esperado: 'linhas colunas'.")

    #Garante que as dimensões sejam válidas
    if nrows <= 0 or ncols <= 0:
        raise ValueError("Dimensões inválidas da matriz.")

    matriz = []
    #Lê as linhas seguintes para construir a matriz
    for i in range(1, 1 + nrows):
        if i < len(linhas):
            tokens = linhas[i].split()
            #Caso os elementos estejam juntos (ex: "RAB00"), separa caractere por caractere
            if len(tokens) == 1 and len(tokens[0]) == ncols:
                elementos = list(tokens[0])
            else:
                elementos = tokens
            #Verifica se a linha tem mais colunas que o permitido
            if len(elementos) > ncols:
                raise ValueError(f"Linha {i} com colunas a mais.")
            #Completa com "0" se houver menos colunas que o esperado
            while len(elementos) < ncols:
                elementos.append("0")
            matriz.append(elementos[:ncols])
        else:
            #Caso o arquivo tenha menos linhas que o informado, completa com zeros
            matriz.append(["0"] * ncols)

    #Retorna as dimensões e a matriz construída
    return nrows, ncols, matriz


#Função que encontra os pontos da matriz (R e entregas)
def encontrar_pontos(matriz):
    pontos = {}
    for i, linha in enumerate(matriz):        #Percorre cada linha com seu índice
        for j, valor in enumerate(linha):     #Percorre cada coluna com seu índice
            if valor and valor != "0":        #Ignora células vazias ou com zero
                #Garante que cada ponto seja uma letra válida (ex: R, A, B, C)
                if len(valor) != 1 or not valor.isalpha():
                    raise ValueError(f"Caractere inválido encontrado: {valor}")
                #Armazena o ponto e sua posição (linha, coluna)
                pontos[valor] = (i, j)
    return pontos


#Função que calcula a distância de Manhattan entre dois pontos
def distancia(a, b):
    # Soma das diferenças absolutas entre as coordenadas
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


#Função que gera todas as permutações possíveis de uma lista
def gerar_permutacoes(seq):
    #Caso base: lista vazia
    if len(seq) == 0:
        return [[]]
    #Caso base: lista com um único elemento
    if len(seq) == 1:
        return [seq[:]]

    perms = []
    #Gera todas as combinações possíveis
    for i in range(len(seq)):
        atual = seq[i]
        resto = seq[:i] + seq[i + 1:]
        for p in gerar_permutacoes(resto):
            perms.append([atual] + p)
    return perms


#Função que calcula todas as rotas possíveis e seus custos
def calcular_rotas(pontos):
    #Cria um dicionário apenas com os pontos de entrega (exclui o R)
    entregas = {k: v for k, v in pontos.items() if k != "R"}
    letras = list(entregas.keys())

    #Verifica se há entregas
    if not letras:
        raise ValueError("Nenhum ponto de entrega encontrado.")

    rotas = []
    #Gera todas as permutações de entrega
    for perm in gerar_permutacoes(letras):
        custo = 0
        #Adiciona o ponto inicial e final (R)
        rota_completa = ["R"] + list(perm) + ["R"]
        #Soma o custo total da rota
        for i in range(len(rota_completa) - 1):
            a, b = rota_completa[i], rota_completa[i + 1]
            custo += distancia(pontos[a], pontos[b])
        rotas.append((rota_completa, custo))

    #Ordena as rotas pelo menor custo
    rotas.sort(key=lambda x: x[1])
    return rotas


#Função principal
def main():
    try:
        #Tenta ler a matriz do arquivo
        _, _, matriz = ler_matriz_arquivo("entrada.txt")
    except Exception as e:
        print(f"{YELLOW}Erro ao ler a matriz: {e}{RESET}")
        return

    #Exibe a matriz lida
    print(f"{GREEN}(Matriz lida){RESET}")
    for linha in matriz:
        print(" ".join(linha))

    try:
        #Encontra os pontos de entrega e o ponto R
        pontos = encontrar_pontos(matriz)
    except Exception as e:
        print(f"{YELLOW}Erro nos pontos: {e}{RESET}")
        return

    #Exibe os pontos encontrados
    print(f"{GREEN}\n(Pontos encontrados){RESET}")
    for k, v in sorted(pontos.items()):
        print(f"{k}: {v}")

    #Garante que o ponto R esteja presente
    if "R" not in pontos:
        print(f"{YELLOW}\nPonto 'R' não encontrado na matriz.{RESET}")
        return

    try:
        #Calcula todas as rotas possíveis
        rotas = calcular_rotas(pontos)
    except Exception as e:
        print(f"{YELLOW}Erro no cálculo das rotas: {e}{RESET}")
        return

    #Se não houver rotas, encerra
    if not rotas:
        print(f"{YELLOW}Nenhuma rota encontrada.{RESET}")
        return

    #Exibe todas as rotas e marca as de menor custo
    print(f"{GREEN}\n(Todas as rotas){RESET}")
    menor_custo = min(c for _, c in rotas)
    for rota, custo in rotas:
        marca = " <-- ÓTIMA" if custo == menor_custo else ""
        print(f"{' -> '.join(rota)} | Custo: {custo}{marca}")

    #Exibe a(s) melhor(es) rota(s)
    melhores = [rota for rota, custo in rotas if custo == menor_custo]
    if len(melhores) == 1:
        print(f"{GREEN}\n(Melhor rota){RESET}")
    else:
        print(f"{GREEN}\n(Melhores rotas){RESET}")
    for rota in melhores:
        print(f"{' -> '.join(rota)} | Custo: {menor_custo}")


#Execução do programa 
if __name__ == "__main__":
    main()
