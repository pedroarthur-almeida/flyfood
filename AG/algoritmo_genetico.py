import random

class AG:
    def __init__(self, pop_inicial, chaves, matriz_adj, dic_indices):
        self.populacao = pop_inicial
        self.chaves = chaves
        self.matriz_adj = matriz_adj
        self.dic_indices = dic_indices
        self.melhor_rota_global = None
        self.melhor_custo_global = float('inf')
        
        self.executar_evolucao()

    def executar_evolucao(self):
        """Executa 100 gerações do algoritmo genético"""
        for geracao in range(1000):
            #Analisar as rotas e custos da população inicial
            populacao_avaliada = self.avaliar_populacao()
            
            #Processo de seleçaõ
            pais = self.selecionar_pais(populacao_avaliada, geracao)
            
            # 3. Cruzamento
            filhos = self.cruzar(pais)
            
            # 4. Mutação
            filhos = self.mutar(filhos)
            
            # 5. Substituição
            self.populacao = self.substituir_populacao(populacao_avaliada, filhos)
            
            # 6. Atualizar melhor global
            self.atualizar_melhor_global(populacao_avaliada)

    def avaliar_populacao(self ):
        """Calcula fitness para cada indivíduo"""
        populacao_avaliada = []
        for rota in self.populacao:
            custo = self.calcular_custo(rota)
            populacao_avaliada.append((rota, custo))
        return sorted(populacao_avaliada, key=lambda x: x[1])
        #x[1] é utilizado para ordernar de forma que ordene do menor custo até o maior custo

    def calcular_custo(self, rota):
        """Calcula custo total de uma rota"""
        custo = 0
        for i in range(len(rota) - 1):
            custo += self.matriz_adj[rota[i]][rota[i + 1]]
        return custo

    def selecionar_pais(self, populacao_avaliada, geracao):
        """Seleção mista: elitista + aleatória"""
        #populacção avaliada é a lista  que possui tuplas=rota,custo

        tamanho_torneio = 3

        #número de pais será a metade da população inicial,pois cada par de pais gerar 2 filhos
        num_pais = len(populacao_avaliada) // 2
        
        pais = []
        
        #elitismo pega os melhores
        if geracao % 10 == 0:  # A cada 10 gerações-->apenas para diversificar
            elitismo = 0.3  # 30% elitista
        else:
            elitismo = 0.4  # 20% elitista
            
        num_elite = int(num_pais * elitismo)#-->pegar a quantidade de pais que serão selecionados por elitismo
        #gerações especiais


        for i in range(num_elite):
            if i < len(populacao_avaliada):
                    #população avalida já está ordenada,logo só é necessário pegar os primeiros

                individuo = populacao_avaliada[i]  #pega a tupla (rota, custo)
                rota = individuo[0]  #extrai apenas a rota (primeiro elemento)
                pais.append(rota)
        
        # Torneio para o restante
        while len(pais) < num_pais:
            #tamanho torneio define quantos indivíduos disputam em cada "batalha"
            competidores = random.sample(populacao_avaliada, tamanho_torneio)
            #vai escolher 3 entre o população avaliada
            #e aqui vai escolher o melhor entre eles em relação ao custo
            vencedor = min(competidores, key=lambda x: x[1])
            pais.append(vencedor[0])
            #irá repetir o processo até pais se igualar com o num pais
            
        return pais

    def cruzar(self, pais):
        """cruzamento de ordem OX """

        filhos = [] #lista vazia para armazenar os filhos
        random.shuffle(pais) #embaralha a lista de pais,pois antes estava ordenado
        
        for i in range(0, len(pais) - 1, 2):
            pai1, pai2 = pais[i], pais[i + 1]
            filho1, filho2 = self.crossover_ox(pai1, pai2)
            filhos.extend([filho1, filho2])
            
        return filhos

    def crossover_ox(self, pai1, pai2):
        
        tamanho = len(pai1)
        
        
        genes1 = pai1[1:-1]  
        genes2 = pai2[1:-1]
        
        #escolher 2 pontos de core,começo e final
        comeco, final = sorted(random.sample(range(len(genes1)), 2))
        
        # Herda segmento do pai1
        filho1 = [None] * len(genes1)
        filho1[comeco:final+1] = genes1[comeco:final+1]
        
        # Preenche com genes do pai2
        pointer = (final + 1) % len(genes1)
        for gene in genes2[final+1:] + genes2[:final+1]:
            if gene not in filho1:
                filho1[pointer] = gene
                pointer = (pointer + 1) % len(genes1)
        
        # Adiciona depósitos
        return [0] + filho1 + [0], [0] + genes2 + [0]  # Segundo filho simplificado

    def mutar(self, filhos):
        """Aplica mutação por swap"""
        taxa_mutacao = 0.1
        
        for filho in filhos:
            if random.random() < taxa_mutacao:
                # Escolhe dois pontos aleatórios (excluindo depósitos)
                idx1, idx2 = random.sample(range(1, len(filho) - 1), 2)
                filho[idx1], filho[idx2] = filho[idx2], filho[idx1]
                
        return filhos

    def substituir_populacao(self, populacao_avaliada, filhos):
        """Substituição com elitismo"""
        # Mantém os melhores da geração anterior
        elitismo = 2  # Mantém os 2 melhores
    
        nova_populacao = []
    
        # FOR CLÁSSICO - Adiciona os melhores indivíduos (elitismo)
        for i in range(elitismo):
            if i < len(populacao_avaliada):
                rota = populacao_avaliada[i][0]  # Pega apenas a rota (sem o custo)
                nova_populacao.append(rota)
    
        
        for filho in filhos:
            nova_populacao.append(filho)
    
        # FOR CLÁSSICO - Completa com indivíduos aleatórios se necessário
        while len(nova_populacao) < len(self.populacao):
            individuo = self.gerar_individuo_aleatorio()
            nova_populacao.append(individuo)
    
        # Retorna apenas o tamanho original da população
        return nova_populacao[:len(self.populacao)]

    def gerar_individuo_aleatorio(self):
        """Gera indivíduo aleatório para manter diversidade"""
        pontos = list(range(1, len(self.chaves)))  # Exclui depósito (0)
        random.shuffle(pontos)
        return [0] + pontos + [0]

    def atualizar_melhor_global(self, populacao_avaliada):
        """Atualiza a melhor solução encontrada"""
        melhor_rota, melhor_custo = populacao_avaliada[0]
        
        if melhor_custo < self.melhor_custo_global:
            self.melhor_rota_global = melhor_rota
            self.melhor_custo_global = melhor_custo

    def retornar(self):
        return self.melhor_rota_global

    def retornar2(self):
        return self.melhor_custo_global