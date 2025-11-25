import random



class PopulacaoInicial:
    def __init__(self,chaves,matriz_adj):

        self.chaves=chaves
        self.matriz_adj=matriz_adj
        
        self.populacao_inicial=self.opt2()



        
    def gerar_individuos_aleatorios(self):
        aleatorios = [] #lista para armazenar as permutacoes aleatorias
        tentativas = 0
        max_tentativas = 1000
        while len(aleatorios)  < 8*len(self.chaves) and tentativas < max_tentativas:
        #O objetivo é gerar 8 vezes mais indivíduos do que a quantidade de chaves
        #Se houver 5 pontos → cria até 40 indivíduos.
            copia = self.chaves[:]
            if copia and copia[0] == "R":
                copia.pop(0)
            random.shuffle(copia)
            individuo = ["R"]+copia+["R"]
            #testa o inverso do índivíduo
            inverso = ["R"]+ copia[::-1]+["R"]
            #verifica se já foi adicionado na lista
            if individuo not in aleatorios and inverso not in aleatorios:
                aleatorios.append(individuo)
            #a cada uma criacao é 
            tentativas +=1
        
        return aleatorios


    #Gerar rota Vizinho mais proximo
    def NN(self):
        start = 0
    
        numero_pontos = len(self.matriz_adj)
        rota = [start]
        nao_visitados = set(range(1, numero_pontos)) #os nao visitados, menos o 0
        atual = start

        while nao_visitados:
            menor = None
            melhor_distancia = float("inf") 
            for possibilidade in nao_visitados: #percorsse as possibilidades entre os nao visitados
                distanciaAtual = self.matriz_adj[atual][possibilidade]
                if distanciaAtual < melhor_distancia:
                    melhor_distancia = distanciaAtual
                    menor = possibilidade
            #add o escolhido e atualiza
            rota.append(menor)
            nao_visitados.remove(menor)
            atual = menor
        rota.append(start)

        return rota

    def juntarRotas(self):
        #gera as rotas aleatorias
        rotasAleatorias = self.gerar_individuos_aleatorios()
        # converter_matriz para obter mapeamento label -> índice
        
        label_to_indice = {label: index for index, label in enumerate(self.chaves)} 
        #cria um dicioonario relacionando a "letra" com o seu valor
        #Converte as rotas aleatorias para indices
        aleatoriasIndices = []
        for rota_labels in rotasAleatorias:
            rota_indice = [label_to_indice[label] for label in rota_labels]
            aleatoriasIndices.append(rota_indice)
        # obtém rota NN (já em índices) e junta
        rota_nn = self.NN()

        rotas = aleatoriasIndices + [rota_nn]
        #irá juntar as rotas aleatórias com as rotas do NN
        return rotas


    def opt2(self):

        """
        O 2-opt é um método de melhorar uma rota do TSP (Travelling Salesman Problem).
        Ele não cria uma nova rota do zero — ele pega uma rota existente e tenta deixá-la melhor.
        """
        
       

        
        
            
        #rotas é uma lista que possui rotas geradas aleatoriamente e pelo NN
        rotas = self.juntarRotas()

        populacao_inicial = []

        # --- aplica 2-opt em cada rota ---
        for rota in rotas:
            #irá ler o tamanho da rota
            n = len(rota)

            # função interna sempre tem acesso à matriz_convertida agora
            def ganho_troca(rota_local, i, j):
                a, b = rota_local[i - 1], rota_local[i]
                c, d = rota_local[j], rota_local[j + 1]

                antes = self.matriz_adj[a][b] + self.matriz_adj[c][d]
                depois = self.matriz_adj[a][c] + self.matriz_adj[b][d]

                return depois - antes

            melhorou = True
            while melhorou:
                melhorou = False

                for i in range(1, n - 2):
                    for j in range(i + 1, n - 1):
                        ganho = ganho_troca(rota, i, j)
                        if ganho < 0:
                            rota[i:j+1] = list(reversed(rota[i:j+1]))
                            melhorou = True
                            break
                    if melhorou:
                        break

            populacao_inicial.append(rota)

        return populacao_inicial
    
    def get_populacao(self):
        return self.populacao_inicial
