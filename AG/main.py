from convert_matriz_utils import *

from populacao_inicial import *

from algoritmo_genetico import *

class Main:
    def __init__(self):
        
        tm = TratamentoMatriz()
        self.perm, self.dist,self.chaves,self.matriz_adjacencia = tm.get_resultados()

        print("Melhor permutação:", self.perm)
        print("Distância total:", self.dist)

        pop=PopulacaoInicial(self.chaves,self.matriz_adjacencia)
        self.populacao_inicial=pop.get_populacao()

        ag=AG(self.populacao_inicial,self.chaves,self.matriz_adjacencia)
    
    def get_pop(self):
        return self.populacao_inicial


print("Nome do módulo:", __name__)


main=Main()
print(main.get_pop())

