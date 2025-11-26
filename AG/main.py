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
        self.menor1=ag.retornar3()
        self.menor2=ag.retornar4()


    def get_pop(self):
        return self.dic_indices
    
    def get_pop1(self):
        return self.melhor2
    
    def get_pop2(self):
        return self.menor1
    
    def get_pop3(self):
        return self.menor2

    def get_4(self):
        return self.chaves






main=Main()
print(main.get_pop())
print(main.get_pop1())
print(main.get_pop2())
print(main.get_pop3())
print(main.get_4())


