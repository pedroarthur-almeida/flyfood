import random

class AG:
    def __init__(self,pop_inicial,chaves,matriz_adj):
        self.pop_inicial=pop_inicial
        
        self.chaves=chaves
        self.matriz_adj=matriz_adj

        self.menor_custo,self.segundo_menor_custo,self.melhor_rota,self.segunda_melhor_rota=self.selecao()


    def selecao(self):
        
        #irá qual a quantidade total de populações geradas
        qnt_popinicial=len(self.pop_inicial)

        #max entre 2 ou rotas maiores
        qnt_escolhida=max(2,len(self.chaves)//2)

        
       
        lista_selecao = random.sample(self.pop_inicial, k=min(qnt_escolhida, qnt_popinicial))
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

        for rota in lista_selecao:
            #Calcula custo da rota percorrendo cada valor e comparando com a matriz de adjacência
            for i in range(len(rota)-1):
                custo = sum(self.matriz_adj[rota[i]][rota[i+1]])
                        

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
        pass
        


    def mutacao(self):
        pass