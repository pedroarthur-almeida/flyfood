from convert_matriz_utils import *

from populacao_inicial import *

from algoritmo_genetico import *

class Main:
    def __init__(self):
        

        
        tm = TratamentoMatriz()
        self.perm, self.dist,self.chaves,self.matriz_adjacencia = tm.get_resultados()
        #chaves=['R', 'A', 'B', 'C', 'D']

       
        pop=PopulacaoInicial(self.chaves,self.matriz_adjacencia)
        self.populacao_inicial,self.dic_indices=pop.get_populacao()

        #self.populacao_inicial==varias populacoes no formato que só utiliza os índices



        ag=AG(self.populacao_inicial,self.chaves,self.matriz_adjacencia,self.dic_indices)
        

        self.melhor=ag.retornar()
        self.melhor2=ag.retornar2()
        


    def get_pop(self):
        return self.melhor
    
    def get_pop1(self):
        return self.melhor2
    
   





main=Main()
print(main.get_pop())
print(main.get_pop1())


