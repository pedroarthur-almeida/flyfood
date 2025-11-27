import random

class AG:
    def __init__(self,pop_inicial,chaves,matriz_adj,dic_indices):
        self.pop_inicial=pop_inicial
        
        self.chaves=chaves
        self.matriz_adj=matriz_adj
        self.dic_indices=dic_indices

        """
        {'R': 0, 
        'A': 1, 
        'B': 2, 
        'C': 3, 
        'D': 4}
        """

        self.loop_geracoes()
        

        

        #avaliação das rotas deve ser feito logo com a população inicial,depois fazendo cruzamento 
        # e achando os filhos,se 



    def loop_geracoes(self):
        """Controla o número de gerações do algoritmo (1000 gerações)"""
        # Faz uma cópia da população inicial para não modificar a original
        populacao_atual = []
    
        for rota in self.pop_inicial:
            populacao_atual.append(rota)

        # Inicializa o melhor custo e rota com a população inicial
        
    
        for geracao in range(1000):
            
            # Processa uma geração e atualiza a população
            self.soma_pop_ini()
        
           

    def soma_pop_ini(self):

        menor_custo=float("inf")
        melhor_rota=None


        for rota in self.pop_inicial:
            custo_total=0
            for i in range(len(rota) - 1):
                
                ponto_atual = rota[i]
                ponto_seguinte = rota[i + 1]
                # Adiciona a distância entre o ponto atual e o próximo
                #serrá feito  rota = [0, 1, 2, 3, 0] -> custo = 
                # matriz_adj[0][1] + matriz_adj[1][2] + matriz_adj[2][3] + matriz_adj[3][0]
                custo_total += self.matriz_adj[ponto_atual][ponto_seguinte]


                """
                Exemplo de execução para o entendimento
             [0, 2, 1, 3, 0]

                #ponto atual=0
                ponto seguinte=2
                custo+=valor que equivale na matriz de adjacência[0][2]        
                """


                

            if custo_total<=melhor_rota:
                menor_custo=custo_total
                melhor_rota=rota
        
        self.melhor_rota=melhor_rota
        self.menor_custo=menor_custo

        self.selecao_atualizada()

        

    

    def selecao_atualizada(self):
        #seleção é a parte que iremos escolher os pais

        """
        A seleção pode ser feita de várias formas: aleatória, elitista, por torneio, etc.
        Você mencionou que não quer usar termos técnicos da biologia, então vamos pensar em 
        termos de como escolher as rotas para cruzar.

        Vou explicar as opções:

        Seleção aleatória: Escolhemos pares de pais aleatoriamente da população inicial.

        Seleção elitista: Escolhemos os melhores (menor custo) para serem pais.

        Seleção por torneio: Escolhemos aleatoriamente um pequeno grupo e desse grupo selecionamos o 
        melhor para ser pai.
        
        """

        pass
        
    

    def selecao(self):
        
        #irá qual a quantidade total de populações geradas
        qnt_popinicial=len(self.pop_inicial) #formato de listas

        #max entre 2 ou rotas maiores
        qnt_escolhida=max(2,len(self.chaves)//2) #quantas rotas máximas será escolhida

        
       
        lista_selecao = random.sample(self.pop_inicial, k=min(qnt_escolhida, qnt_popinicial))
        #lista gerada aleatoriamente a partir do self.pop_inicial que veio da outra classe


        """
        Objetivo: escolher k elementos aleatórios de uma sequência, sem repetir elementos.

        Parâmetros:

        população → qualquer lista, tupla ou conjunto iterável de onde você quer tirar os elementos.

        k → quantidade de elementos que você quer selecionar.

        qnt_escolhida → número de indivíduos que você quer selecionar.

        qnt_popinicial → número total de indivíduos disponíveis na população.

        Usar min(qnt_escolhida, qnt_popinicial) garante que você nunca tente selecionar mais indivíduos do que 
        existem, evitando erro.

        random.sample() não repete elementos

        """

        # Inicializa variáveis
        menor_custo = float("inf") #inicia com valor infinito,para que seja garantido que as primeiras rotas serão melhores
        segundo_menor_custo = float("inf")
        melhor_rota = None
        segunda_melhor_rota = None

        custo=0

        for rota in lista_selecao:
            #Calcula custo da rota percorrendo cada valor e comparando com a matriz de adjacência
            for i in range(len(rota)-1):
                custo +=self.matriz_adj[rota[i]][rota[i+1]]
                        

            # Verifica se é o menor
            if custo < menor_custo:
                #  segundo menor antes
                segundo_menor_custo = menor_custo
                segunda_melhor_rota = melhor_rota

                # Atualiza menor
                menor_custo = custo
                melhor_rota = rota

            elif custo < segundo_menor_custo:
                # Atualiza apenas o segundo menor
                segundo_menor_custo = custo
                segunda_melhor_rota = rota

        
        return menor_custo,segundo_menor_custo,melhor_rota,segunda_melhor_rota 

            




    def cruzamento(self):
        
        self.pai1=[]
        self.pai2=[]

        
        #processo de passar de índice para o nome da rota
        indice_to_valor = {}

        for chave in self.dic_indices:
            valor = self.dic_indices[chave]
            indice_to_valor[valor] = chave

            """
            {
            0: "A",
            1: "B",
            2: "C",
            3: "D"
            }

            """

        for a in self.melhor_rota:
            valor=indice_to_valor[a]
            self.pai1.append(valor)

        for b in self.segunda_melhor_rota:
            valor=indice_to_valor[b]
            self.pai2.append(b)

        tamanho = len(self.pai1)
        filho1 = [None] * tamanho
        filho2 = [None] * tamanho

        

        # delimitadores
        i = random.randint(0, tamanho-2)
        j = random.randint(i+1, tamanho-1)

        #FILHO 1 

        seguimento1 = self.pai1[i:j]

        for p in range(i, j):
            filho1[p] = self.pai1[p]

        
        preenchimento1 = self.pai2[:]  

        for x in seguimento1:
            preenchimento1.remove(x)

# preenchimento cíclico
        pos = j
        tamanho_f = len(filho1)

        for elemento in preenchimento1:
            while filho1[pos] is not None:
                pos = (pos + 1) % tamanho_f

            filho1[pos] = elemento
            pos = (pos + 1) % tamanho_f


        # FILHO 2 

        seguimento2 = self.pai2[i:j]

        for p in range(i, j):
            filho2[p] = self.pai2[p]

        preenchimento2 = self.pai1[:]   # também copia!

        for x in seguimento2:
            preenchimento2.remove(x)

        pos = j
        tamanho_f2 = len(filho2)

        for elemento in preenchimento2:
            while filho2[pos] is not None:
                pos = (pos + 1) % tamanho_f2

            filho2[pos] = elemento
            pos = (pos + 1) % tamanho_f2


        return filho1,filho2






        
        #processo de cruzamento de ordem OX
        """
        De Ordem (OX)
        Diferente do PMX, que se foca na posição absoluta de um segmento, o OX se foca em preservar a ordem 
        relativa das cidades no restante da rota.

        A principal vantagem do OX é sua simplicidade e a garantia de que a rota filha será sempre uma permutação válida.
        
        1. Cópia do Segmento Central (Bloco de Cidades)
        O segmento central do Pai 1 é copiado diretamente para o Filho 1.

        PAI 1: A B C D E F G H
        PAI 2: H G E B A C F D
        FILHO:_ _  _ D E F _ _ _

        2. Criação da Lista de Preenchimento (Cidades Restantes)
        O algoritmo identifica quais cidades de Pai 2 não foram copiadas para o F1 (as cidades que não são C, E, ou B). 
        Essas cidades são listadas na ordem em que aparecem no Pai 2.

        H G E B A C F D
        Lista de Preenchimento (Ordem Relativa): {H, G, B, A, C}

        3. Preenchimento do Filho (Preservando a Ordem)

        O algoritmo preenche os espaços vazios de F1 usando a Lista de Preenchimento, começando imediatamente após o 
        segmento copiado do Pai 1 (ou seja, a partir da Posição 7) e ciclando para o início se necessário.

        POSIÇÃO
        7=H
        8=G
        1=B
        2=A
        3=C
        Resultado final= B A C D E F H G  


        
        
        
        Faremos dois filho=um começando com o pai1=[0,1,2,4,3,0]
        e o outro com o pai2=[0, 3, 4, 1, 2, 0]

        Geralmente se escolhe um segmento central de 30% a 70% do total de cidades

        4 pontos 

        #chaves=['R', 'A', 'B', 'C', 'D']
        [0, 1, 2, 4, 3, 0]
        [0, 3, 4, 1, 2, 0]  
        18
        36

        """
        
        #gerando filho 1

        #PAI 1: A B C D E F G H
        #PAI 2: H G E B A C F D


    def mutacao_swap(self):

        pass

    def mutacao_inversao(self):
        pass

    def mutacao_deslocamento(self):
        pass

    def retornar(self):
        return self.melhor_rota
    def retornar2(self):
        return self.segunda_melhor_rota
    
    def retornar3(self):
        return self.menor_custo
    def retornar4(self):
        return self.segundo_menor_custo