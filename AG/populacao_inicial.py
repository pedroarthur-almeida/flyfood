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
        
        self.dic_indices = {label: index for index, label in enumerate(self.chaves)}

        #cria um dicioonario relacionando a "letra" com o seu valor
        #Converte as rotas aleatorias para indices
        aleatoriasIndices = []
        for rota_labels in rotasAleatorias:
            rota_indice = [self.dic_indices[label] for label in rota_labels]
            aleatoriasIndices.append(rota_indice)
        # obtém rota NN (já em índices) e junta
        rota_nn = self.NN()

        rotas = aleatoriasIndices + [rota_nn]
        #irá juntar as rotas aleatórias com as rotas do NN
        return rotas


    def opt2(self):
    # Retorna as rotas SEM 2-opt
        return self.juntarRotas()
    
    def get_populacao(self):
        return self.populacao_inicial,self.dic_indices
