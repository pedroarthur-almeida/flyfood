import random

class AG:
    def __init__(self, pop_inicial, chaves, matriz_adj, dic_indices):
        self.populacao = pop_inicial
        self.chaves = chaves
        self.matriz_adj = matriz_adj
        self.dic_indices = dic_indices
        self.melhor_rota_global = None
        self.melhor_custo_global = float('inf')
        self.lista_melhores=[]
        
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
            self.atualizar_melhor_global(geracao,populacao_avaliada)

    def avaliar_populacao(self,populacao=None):
        """Calcula fitness para cada indivíduo"""
        if populacao is None:
            populacao = self.populacao  # ← Usa parâmetro se fornecido
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
    
    @staticmethod
    def distancia(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # ← ESTÁ CORRETO?

    def selecionar_pais(self, populacao_avaliada, geracao):
        """Seleção mista: elitista + aleatória"""
        #populacção avaliada é a lista  que possui tuplas=rota,custo

        tamanho_torneio = 3

        #número de pais será a metade da população inicial,pois cada par de pais gerar 2 filhos
        num_pais = len(populacao_avaliada) 
        
        pais = []
        
        #elitismo pega os melhores
        if geracao % 10 == 0:  # A cada 10 gerações-->apenas para diversificar
            elitismo = 0.2  # 30% elitista
        else:
            elitismo = 0.1  # 20% elitista
            
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
        genes1 = pai1[1:-1]  
        genes2 = pai2[1:-1]
        size = len(genes1)
    
        start, end = sorted(random.sample(range(size), 2))
    
        # FILHO 1 (herda segmento do pai1)
        filho1 = [None] * size
        filho1[start:end+1] = genes1[start:end+1]
    
        pointer = (end + 1) % size
        for gene in genes2:
            if gene not in filho1:
                while filho1[pointer] is not None:
                    pointer = (pointer + 1) % size
                filho1[pointer] = gene
    
        # FILHO 2 (herda segmento do pai2) ← CORREÇÃO AQUI!
        filho2 = [None] * size
        filho2[start:end+1] = genes2[start:end+1]  # Herda de pai2
    
        pointer = (end + 1) % size
        for gene in genes1:  # Preenche com pai1 ← CORREÇÃO AQUI!
            if gene not in filho2:
                while filho2[pointer] is not None:
                    pointer = (pointer + 1) % size
                filho2[pointer] = gene
    
        return [0] + filho1 + [0], [0] + filho2 + [0]  # Ambos com crossover

    def mutar(self, filhos):
        """Aplica mutação por swap"""
        #quantidade de filhos que vai mutar
        taxa_mutacao = 0.2 #30%
        
        for filho in filhos:
            if random.random() < taxa_mutacao:
                # Escolhe dois pontos aleatórios (excluindo depósitos)
                idx1, idx2 = random.sample(range(1, len(filho) - 1), 2)
                filho[idx1], filho[idx2] = filho[idx2], filho[idx1]
                
        return filhos

    def substituir_populacao(self, populacao_avaliada, filhos):
        elitismo = 2
        nova_populacao = []
    
        # 1. ELITE - sempre mantém os melhores
        for i in range(elitismo):
            if i < len(populacao_avaliada):
                nova_populacao.append(populacao_avaliada[i][0])
    
    # 2. FILHOS - adiciona até completar população
    
        espaco_restante = len(self.populacao) - elitismo
    
        if len(filhos) > espaco_restante:
            # Escolhe filhos ALEATORIAMENTE ← TESTE ESTA MUDANÇA
            melhores_filhos = random.sample(filhos, espaco_restante)
            nova_populacao.extend(melhores_filhos)
        
        
        return nova_populacao

    def gerar_individuo_aleatorio(self):
        """Gera indivíduo aleatório para manter diversidade"""
        pontos = list(range(1, len(self.chaves)))  #Exclui (0)
        random.shuffle(pontos)
        return [0] + pontos + [0]

    def atualizar_melhor_global(self, geracao, populacao_avaliada):
        """Registra a evolução real do algoritmo"""
        if not populacao_avaliada:
            return
    
        # Melhor da GERAÇÃO ATUAL (não necessariamente o global)
        melhor_rota_atual, melhor_custo_atual = populacao_avaliada[0]
    
        # Verifica se é uma melhoria GLOBAL
        if melhor_custo_atual < self.melhor_custo_global:
            self.melhor_rota_global = melhor_rota_atual
            self.melhor_custo_global = melhor_custo_atual
            print(f"🎉 Geração {geracao}: NOVO RECORDE = {melhor_custo_atual}")
    
        # ✅ MUDANÇA CRÍTICA: Registra o MELHOR DA GERAÇÃO, não só o global
        self.lista_melhores.append([
            geracao, 
            melhor_rota_atual,           # Melhor desta geração
            melhor_custo_atual,          # Custo desta geração  
            self.melhor_custo_global     # Melhor global (para referência)
        ])
    
    

    def retornar(self):
        return self.melhor_rota_global

    def retornar2(self):
        return self.melhor_custo_global
    
    def  retornar3(self):
        return self.lista_melhores