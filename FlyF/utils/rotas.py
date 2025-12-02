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
    return rotas