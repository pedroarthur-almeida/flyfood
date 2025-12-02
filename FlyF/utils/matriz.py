RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"


def ler_matriz_arquivo(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
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


def encontrar_pontos(matriz):
    pontos = {}
    coords_ocupados = {}
    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            if valor and valor != "0":
                if len(valor) != 1 or not valor.isalpha():
                    raise ValueError(f"Caractere inválido encontrado na posição {(i, j)}: {valor}")

                if valor in pontos:
                    raise ValueError(f"Letra duplicada encontrada: '{valor}' já em {pontos[valor]} e novamente em {(i, j)}")

                if (i, j) in coords_ocupados:
                    raise ValueError(f"Mais de um ponto na mesma posição {(i, j)}: '{coords_ocupados[(i, j)]}' e '{valor}'")

                pontos[valor] = (i, j)
                coords_ocupados[(i, j)] = valor
    return pontos