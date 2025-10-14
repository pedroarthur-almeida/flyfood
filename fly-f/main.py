from matriz_utils import *
from rotas_utils import *
import tracemalloc
import psutil
import os


def medir_memoria(funcao, *args, **kwargs):
    #função utilizada para medir a quantidade de memória ram utilizada a partir das 
    #bibliotecas psutil e tracemalloc
    process = psutil.Process(os.getpid())
    tracemalloc.start()

    resultado = funcao(*args, **kwargs)

    pico_tracemalloc = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    ram_uso_total = process.memory_info().rss / 1024**2

    print(f"\n{GREEN}(MEDIÇÃO DE MEMÓRIA){RESET}")
    print(f"RAM total usada pelo processo (psutil): {ram_uso_total:.2f} MB")
    print(f"Pico de memória alocada por objetos Python (tracemalloc): {pico_tracemalloc / 1024**2:.2f} MB\n")

    return resultado


def main():
    try:
        #puxará a função ler_matriz e 
        #retornará nrows, ncols, matriz
        _, _, matriz = ler_matriz_arquivo("fly-f/entrada.txt")
    except Exception as e:
        print(f"{YELLOW}Erro ao ler a matriz: {e}{RESET}")
        return

    print(f"{GREEN}(Matriz lida){RESET}")
    for linha in matriz:
        print(" ".join(linha))

    try:
        #puxará a função com a matriz já organizada
        # vinda da função ler_matriz_arquivo e retornará os pontos 
        
        
        
        
        
        
        #retorna rotas um dicionário com as coordenadas de cada ponto
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
       
        rotas = medir_memoria(calcular_rotas, pontos)
    except Exception as e:
        print(f"{YELLOW}Erro no cálculo das rotas: {e}{RESET}")
        return
    

    print(f"Total de rotas: {len(rotas)}")

    if not rotas:
        print(f"{YELLOW}Nenhuma rota encontrada.{RESET}")
        return

    print(f"{GREEN}\n(Todas as rotas - filtradas){RESET}")

    primeira_rota, custo_primeira = rotas[0]
    print(f"{' -> '.join(primeira_rota)} | Custo: {custo_primeira}")

    for rota, custo in rotas[1:]:
        if custo < custo_primeira:
            print(f"{' -> '.join(rota)} | Custo: {custo}")

    menor_custo = min(c for _, c in rotas)
    melhores = [rota for rota, custo in rotas if custo == menor_custo]

    if len(melhores) == 1:
        print(f"{GREEN}\n(Melhor rota){RESET}")
    else:
        print(f"{GREEN}\n(Melhores rotas){RESET}")

    for rota in melhores:
        print(f"{' -> '.join(rota)} | Custo: {menor_custo}")

if __name__ == "__main__":
    main()
