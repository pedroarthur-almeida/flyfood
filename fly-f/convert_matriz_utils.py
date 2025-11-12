from python_tsp.heuristics import solve_tsp_local_search
import numpy as np

# Função auxiliar: distância euclidiana entre dois pontos (i,j)
def distancia(p1, p2):
    return round(((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5, 2)

def converter_matriz(matriz):
    pontos = {}
    for i, linha in enumerate(matriz):
        for j, celula in enumerate(linha):
            if celula != "0":
                pontos[celula] = (i, j)

    lista = []
    for k in pontos:
        if k != "R":
            lista.append(k)
    chaves_ordenadas = ["R"] + sorted(lista)

    matriz_convertida = []
    for a in chaves_ordenadas:
        linha = []
        for b in chaves_ordenadas:
            if a == b:
                linha.append(0)
            else:
                linha.append(distancia(pontos[a], pontos[b]))
        matriz_convertida.append(linha)

    return chaves_ordenadas, matriz_convertida

def matriz_tsp(matriz_convertida):
    matriz_np = np.array(matriz_convertida)  # ✅ conversão para NumPy
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

# ===================== TESTE =====================
if __name__ == "__main__":
    matriz_exemplo = [
        ["0", "0", "A", "0", "B"],
        ["0", "0", "0", "0", "0"],
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
