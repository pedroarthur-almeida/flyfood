# FlyFood
Desenvolvido como projeto do segundo período do Bacharelado em Sistemas de Informação.
Trata-se de uma aplicação acadêmica que simula entregas por drones, buscando a melhor rota possível em um ambiente urbano.
___________________________________________________________________________________

<p align="center">
  <img src="imgs/drone4.png" width="650" height="500" /><br>
  <em>Imagem meramente ilustrativa, gerada por inteligência artificial.</em>
</p>

# Descrição:
O FlyFood apresenta a ideia de drones realizando entregas em uma cidade. Esses drones partem de um ponto de origem carregados com vários pedidos e precisam visitar diferentes locais de entrega antes de retornar à base. No entanto, um dos grandes         desafios é a limitação da bateria, que exige que o percurso seja planejado da forma mais eficiente possível. Para resolver essa problemática, o projeto trabalha com uma matriz que representa a cidade e os pontos de entrega. A partir dessa matriz, o      algoritmo busca, por meio de força bruta, todas as rotas possíveis e identifica a de menor custo, garantindo que o drone consiga realizar todas as entregas e retornar ao ponto inicial.

# Tecnologias utilizadas:
- Python 3.12.3

# Funcionalidades do código: 
- 📄 Leitura de matriz a partir de arquivo.
- 📍 Identificação de pontos de interesse.
- 📏 Cálculo de distâncias.
- 🔀 Geração de permutações de rotas (força bruta).
- 💰 Cálculo do custo total das rotas.

# Estrutura do Projeto

O FlyFood segue uma organização modular, separando o código em arquivos de acordo com sua responsabilidade.
```
fly-f/
│
├─ entrada.txt
├─ main.py
├─ matriz_utils.py
│ ├─ ler_matriz_arquivo()
│ └─ encontrar_pontos()
├─ rotas_utils.py
│ ├─ distancia()
│ ├─ gerar_permutacoes()
│ └─ calcular_rotas()
```

# Exemplo de Uso (Simplificado)

Este é um exemplo simplificado para ilustrar como o FlyFood funciona com uma matriz pequena.

Entrada:
```
5 5
R 0 0 0 A
0 0 B 0 0
0 0 0 0 0
0 C 0 0 0
0 0 0 D 0
```

Saída esperada:
```
(Matriz lida)
R 0 0 0 A
0 0 B 0 0
0 0 0 0 0
0 C 0 0 0
0 0 0 D 0

(Pontos encontrados)
R: (0, 0)
A: (0, 4)
B: (1, 2)
C: (3, 1)
D: (4, 3)
Total de rotas: 24

(Melhores rotas (menor custo = 18))
R -> A -> B -> D -> C -> R
R -> A -> D -> C -> B -> R
R -> B -> A -> D -> C -> R
R -> B -> C -> D -> A -> R
R -> C -> D -> A -> B -> R
R -> C -> D -> B -> A -> R
```
💡 Observação: Este exemplo utiliza uma matriz menor e poucas entregas apenas para demonstrar a funcionalidade do programa. Em matrizes maiores e com mais pontos, o número de rotas cresce rapidamente.

# Instalação
1. Clone o repositório:
```
git clone https://github.com/pedroarthur-almeida/flyfood.git
```
2. Execute:
```
python main.py
```

# Crie um ambiente virtual (recomendado):
- No Windows:
```
python -m venv venv
venv\Scripts\activate
```
- No Mac/Linux:
```
python -m venv venv
source venv/bin/activate
```

## Desenvolvedores Responsáveis
Pedro Arthur M. de Almeida
GitHub:
```
https://github.com/pedroarthur-almeida
```
Matheus de Castro Pecora
GitHub:
```
https://github.com/Matheuscastro1903
```
Samuel Andrade Adelino da Silva
GitHub:
```
https://github.com/samuelandradea
```
Matheus Henrique Filgueira Cintra
GitHub:
```
https://github.com/CintraMatheus
```


