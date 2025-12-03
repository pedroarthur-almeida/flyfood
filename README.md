# FlyFood
Desenvolvido como projeto do segundo período do Bacharelado em Sistemas de Informação.  
Trata-se de uma aplicação acadêmica que simula entregas por drones, buscando a melhor rota possível em um ambiente urbano.

___________________________________________________________________________________

<p align="center">
  <img src="imgs/drone4.png" width="650" height="500" /><br>
  <em>Imagem meramente ilustrativa, gerada por inteligência artificial.</em>
</p>

# Descrição
O FlyFood apresenta a ideia de drones realizando entregas em uma cidade. Os drones partem de um ponto inicial carregando pedidos e precisam visitar diversos locais de entrega antes de retornar à base.  
A matriz fornecida representa o ambiente urbano, os pontos de entrega e o ponto inicial, permitindo ao sistema calcular a melhor rota possível.

Inicialmente, o projeto utilizava somente uma abordagem de **força bruta**, gerando todas as rotas possíveis e identificando a de menor custo.  
Agora o sistema também conta com uma implementação de **Algoritimo Genético (AG)**, permitindo:

- Otimizar rotas no problema do FlyFood em matrizes maiores.  
- Resolver a instância **brazil58** da TSPLIB, um caso clássico do Problema do Caixeiro Viajante (TSP).

Com essa ampliação, o projeto suporta tanto soluções exatas (força bruta) quanto heurísticas (AG).

# Tecnologias utilizadas
- Python 3.12.3

# Funcionalidades
- Leitura da matriz de entrada  
- Identificação dos pontos relevantes no mapa  
- Cálculo de distâncias  
- Geração e avaliação de rotas usando força bruta  
- **Otimização de rotas usando Algoritimo Genético**  
- **Aplicação do AG no TSP brazil58**  
- Exibição da melhor rota e custo total conforme o método escolhido

# Instalação
Clone o repositório:
