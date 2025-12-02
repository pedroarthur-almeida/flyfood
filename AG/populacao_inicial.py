import random



class PopulacaoInicial:
    def __init__(self,chaves,matriz_adj):

        self.chaves=chaves
        self.matriz_adj=matriz_adj
        self.dic_indices = {label: i for i, label in enumerate(chaves)}
        self.populacao_inicial=self.opt2()



        
    def gerar_individuos_aleatorios(self, alvo_por_chave=8, max_tentativas=1000):
        """
        Gera rotas aleatórias. Se `chaves` contém strings (ex: "R","A"...),
        retorna rotas em labels (["R",..., "R"]). Se `chaves` contém números,
        retorna rotas em índices ([0, ..., 0]).
        """
        aleatorios = []
        tentativas = 0
        alvo = alvo_por_chave * len(self.chaves)

        # detecta se chaves são labels (strings) ou índices (int)
        chaves_tipo = None
        if all(isinstance(x, str) for x in self.chaves):
            chaves_tipo = "labels"
        elif all(isinstance(x, int) for x in self.chaves):
            chaves_tipo = "indices"
        else:
            # misto: adotamos índice se a primeira for int
            chaves_tipo = "labels" if isinstance(self.chaves[0], str) else "indices"

        if chaves_tipo == "labels":
            # mantemos o comportamento antigo: remove "R" antes de embaralhar
            base = self.chaves[:]  # ex: ["R","A","B",...]
            if base and base[0] == "R":
                base = base[1:]
            while len(aleatorios) < alvo and tentativas < max_tentativas:
                copia = base[:]
                random.shuffle(copia)
                individuo = ["R"] + copia + ["R"]
                inverso = ["R"] + copia[::-1] + ["R"]
                if individuo not in aleatorios and inverso not in aleatorios:
                    aleatorios.append(individuo)
                tentativas += 1

        else:  # indices
            n = len(self.chaves)  # ex: 58
            base_indices = list(range(1, n))  # 0 é o start/retorno
            while len(aleatorios) < alvo and tentativas < max_tentativas:
                copia = base_indices[:]
                random.shuffle(copia)
                individuo = [0] + copia + [0]
                inverso = [0] + copia[::-1] + [0]
                if individuo not in aleatorios and inverso not in aleatorios:
                    aleatorios.append(individuo)
                tentativas += 1

        return aleatorios


    #Gerar rota Vizinho mais proximo
    def NN(self):
        start = 0
    
        numero_pontos = len(self.matriz_adj)
        rota = [start]
        nao_visitados = set(range(1, numero_pontos)) #os nao visitados, menos o 0
        atual = start

        while nao_visitados:
            menor = None
            melhor_distancia = float("inf") 
            for possibilidade in nao_visitados: #percorsse as possibilidades entre os nao visitados
                distanciaAtual = self.matriz_adj[atual][possibilidade]
                if distanciaAtual < melhor_distancia:
                    melhor_distancia = distanciaAtual
                    menor = possibilidade
            #add o escolhido e atualiza
            rota.append(menor)
            nao_visitados.remove(menor)
            atual = menor
        rota.append(start)

        return rota

    def juntarRotas(self):
        
        """
        Junta rotas aleatórias + rota NN, sempre retornando uma lista de rotas
        em INDICES (não em labels). Ou seja, se gerar_individuos_aleatorios
        entregou rotas em labels, aqui convertemos; se já foram índices,
        mantemos como estão.
        """
        # 1) gerar rotas aleatórias (pode vir em labels ou índices, dependendo de chaves)
        rotas_aleatorias = self.gerar_individuos_aleatorios()

        # 2) se chaves são labels -> precisamos de mapping label->indice
        # converter_matriz(matriz) deve existir e retornar (chaves_list, matriz_convertida)
        chaves_list = self.chaves
        matriz_convertida = self.matriz_adj
        # monta dicionário label->indice ou indice->indice (identidade)
        # se chaves_list forem strings (["R","A",..."]) cria mapping; se já for numérico, cria identidade
        label_to_indice = {}
        if all(isinstance(x, str) for x in chaves_list):
            for idx, label in enumerate(chaves_list):
                label_to_indice[label] = idx
        else:
            # chaves_list são numéricas, mapeamento é identidade (ex: label=0 -> idx=0)
            for idx, label in enumerate(chaves_list):
                label_to_indice[label] = idx

        aleatorias_indices = []
        for rota_labels in rotas_aleatorias:
            # se rota já está em índices (números), detecta e usa diretamente
            if all(isinstance(x, int) for x in rota_labels):
                aleatorias_indices.append(rota_labels)
                continue

            # rota está em labels -> converte cada label em índice
            rota_indice = []
            for label in rota_labels:
                # se label não está no mapa, tentamos converter para int (caso label seja '1' string)
                if label not in label_to_indice:
                    try:
                        key = int(label)
                    except Exception:
                        raise KeyError(f"Label '{label}' não encontrado no dicionário de índices.")
                    if key in label_to_indice:
                        rota_indice.append(label_to_indice[key])
                    else:
                        raise KeyError(f"Label '{label}' (convertido para {key}) não existe em chaves.")
                else:
                    rota_indice.append(label_to_indice[label])

            aleatorias_indices.append(rota_indice)

        # 3) rota NN (já em índices): chamamos NN que retorna índices
        rota_nn = self.NN()  # ajuste: garantir que sua NN retorne índices

        # 4) junta tudo e retorna
        rotas = aleatorias_indices + [rota_nn]
        return rotas


    def opt2(self):
    
        return self.juntarRotas()
    
    def get_populacao(self):
        return self.populacao_inicial,self.dic_indices
