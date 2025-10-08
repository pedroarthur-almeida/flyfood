

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
                    raise ValueError(f"Caractere inválido encontrado na posição {(i,j)}: {valor}")

                if valor in pontos:
                    raise ValueError(f"Letra duplicada encontrada: '{valor}' já em {pontos[valor]} e novamente em {(i,j)}")

                if (i, j) in coords_ocupados:
                    raise ValueError(f"Mais de um ponto na mesma posição {(i,j)}: '{coords_ocupados[(i,j)]}' e '{valor}'")

                pontos[valor] = (i, j)
                coords_ocupados[(i, j)] = valor
    return pontos


def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def gerar_permutacoes(seq):
    if len(seq) == 0:
        return [[]]
    if len(seq) == 1:
        return [seq[:]]
    perms = []
    for i in range(len(seq)):
        atual = seq[i]
        resto = seq[:i] + seq[i + 1 :]
        for p in gerar_permutacoes(resto):
            perms.append([atual] + p)
    return perms


def calcular_rotas(pontos):
    entregas = {k: v for k, v in pontos.items() if k != "R"}
    letras = list(entregas.keys())
    if not letras:
        raise ValueError("Nenhum ponto de entrega encontrado.")
    rotas = []
    for perm in gerar_permutacoes(letras):
        custo = 0
        rota_completa = ["R"] + list(perm) + ["R"]
        for i in range(len(rota_completa) - 1):
            a, b = rota_completa[i], rota_completa[i + 1]
            custo += distancia(pontos[a], pontos[b])
        rotas.append((rota_completa, custo))
    rotas.sort(key=lambda x: x[1])
    return rotas


def main():
    try:
        _, _, matriz = ler_matriz_arquivo("entrada.txt")
    except Exception as e:
        print(f"{YELLOW}Erro ao ler a matriz: {e}{RESET}")
        return

    print(f"{GREEN}(Matriz lida){RESET}")
    for linha in matriz:
        print(" ".join(linha))

    try:
        pontos = encontrar_pontos(matriz)
    except Exception as e:
        print(f"{YELLOW}Erro nos pontos: {e}{RESET}")
        return

    print(f"{GREEN}\n(Pontos encontrados){RESET}")
    for k, v in sorted(pontos.items()):
        print(f"{k}: {v}")

    if "R" not in pontos:
        print(f"{YELLOW}\nPonto 'R' não encontrado na matriz.{RESET}")
        return

    try:
        rotas = calcular_rotas(pontos)
    except Exception as e:
        print(f"{YELLOW}Erro no cálculo das rotas: {e}{RESET}")
        return
    
    print(f"Total de rotas: {len(rotas)}")

    if not rotas:
        print(f"{YELLOW}Nenhuma rota encontrada.{RESET}")
        return

    print(f"{GREEN}\n(Todas as rotas){RESET}")
    menor_custo = min(c for _, c in rotas)
    for rota, custo in rotas:
        marca = " <-- ÓTIMA" if custo == menor_custo else ""
        print(f"{' -> '.join(rota)} | Custo: {custo}{marca}")

    melhores = [rota for rota, custo in rotas if custo == menor_custo]
    if len(melhores) == 1:
        print(f"{GREEN}\n(Melhor rota){RESET}")
    else:
        print(f"{GREEN}\n(Melhores rotas){RESET}")
    for rota in melhores:
        print(f"{' -> '.join(rota)} | Custo: {menor_custo}")


if __name__ == "__main__":
    main()
