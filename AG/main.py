from convert_matriz_utils import *

from populacao_inicial import *

from algoritmo_genetico import *

import time

import psutil

class Main:
    def __init__(self):
        
        self.inicio = time.time()
        
        pergunta=""
        while pergunta != 1 and pergunta != 2:
            pergunta = int(input("Digite 1 para Brasil58\nDigite 2 para FlyFood\n"))
        if pergunta ==1:
            tm = TratamentoMatriz(usarBR58=True)
        if pergunta == 2:
            tm = TratamentoMatriz()
        self.chaves,self.matriz_adjacencia = tm.get_resultados()
        #chaves=['R', 'A', 'B', 'C', 'D']

       
        pop=PopulacaoInicial(self.chaves,self.matriz_adjacencia)
        self.populacao_inicial,self.dic_indices=pop.get_populacao()

        #self.populacao_inicial==varias populacoes no formato que só utiliza os índices



        ag=AG(self.populacao_inicial,self.chaves,self.matriz_adjacencia,self.dic_indices)
        

        self.melhor_rota=ag.retornar()
        self.melhor_custo=ag.retornar2()
        #melhores será o melhor custo em cada geração
        self.melhores=ag.retornar3()

        self.fim = time.time()
        

    def calcular_distancias_populacao(self):
        """
        Calcula a distância de cada rota na população
        Retorna: lista de tuplas (rota, distancia)
        """
        populacao_avaliada = []
    
        for rota in self.populacao_inicial:
            distancia = self.calcular_distancia_rota(rota)
            populacao_avaliada.append((rota, distancia))
    
        return populacao_avaliada


    def calcular_distancia_rota(self, rota):
        """
        Calcula a distância total de uma única rota
        """
        distancia_total = 0
        for i in range(len(rota) - 1):
            ponto_atual = rota[i]
            ponto_seguinte = rota[i + 1]
            distancia_total += self.matriz_adjacencia[ponto_atual][ponto_seguinte]
        return distancia_total


    def get_melhorrota(self):
        return self.melhor_rota
    
    def get_melhorcusto(self):
        return self.melhor_custo
    
    def get_melhorlist(self):
        return self.melhores
    
    def get_time(self):
        return self.fim-self.inicio
    
   





processo = psutil.Process(os.getpid())

mem_inicial = processo.memory_info().rss / (1024**2)  # MB



main=Main()

#print(main.calcular_distancias_populacao())




print("Melhor Rota:")
print(main.get_melhorrota())
print()
print("Melhor custo")
print(main.get_melhorcusto())
print()
t=main.get_time()
print(f"Tempo de execução:{t}")



mem_final = processo.memory_info().rss / (1024**2)  # MB

custo = mem_final - mem_inicial


print(f"Custo de memória RAM total:{custo}")


#lista=main.get_melhorlist()


#print("Evolucão do algoritmo")
#for i in lista:
    #print(i)



