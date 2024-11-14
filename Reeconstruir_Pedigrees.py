import heapq

class Pedigree:
    def __init__(self, n_individuos):
        self.n_individuos = n_individuos
        self.arestas = []  # Lista de conexões pai-filho
        self.conectado = [False] * n_individuos  # Rastreamento de indivíduos conectados
        self.valor = 0  # Valor total de pontuação do pedigree
        self.fixo = 0  # Índice de fixação usado para o particionamento
        self.indices_usados = set()  # Armazena os índices das pontuações utilizadas
    
    def adicionar_conexao(self, pai, filho, pontuacao, indice):
        self.arestas.append((pai, filho, pontuacao))
        self.conectado[pai] = True
        self.conectado[filho] = True
        self.valor += pontuacao
        self.indices_usados.add(indice)
    
    def esta_completo(self):
        return all(self.conectado)
    
    def __lt__(self, other):
        # Permite a comparação entre objetos Pedigree pelo valor de pontuação
        return self.valor < other.valor
    
    def __str__(self):
        return f"Pedigree com arestas: {self.arestas} e valor: {self.valor}"

def particionamento_exclusivo(pontuacoes, n_individuos, k):
    fila_prioridade = []
    ped_lista = []
    seen_pedigrees = set()  # Para armazenar pedigrees únicos
    
    # Ordenar as pontuações locais em ordem decrescente
    pontuacoes_ordenadas = sorted(pontuacoes, key=lambda x: x[2], reverse=True)
    
    # Construir o primeiro pedigree e adicioná-lo à fila de prioridades
    pedigree_inicial = construir_pedigree(pontuacoes_ordenadas, n_individuos, 0)
    heapq.heappush(fila_prioridade, (-pedigree_inicial.valor, pedigree_inicial))
    seen_pedigrees.add(tuple(sorted(pedigree_inicial.arestas)))
    
    # Particionamento e busca
    while fila_prioridade and len(ped_lista) < k:
        _, pedigree_atual = heapq.heappop(fila_prioridade)
        ped_lista.append(pedigree_atual)
        
        # Realizar particionamento exclusivo no pedigree atual
        for i in range(pedigree_atual.fixo, len(pontuacoes_ordenadas)):
            novo_pedigree = construir_pedigree_com_particao(pedigree_atual, pontuacoes_ordenadas, i)
            if novo_pedigree and tuple(sorted(novo_pedigree.arestas)) not in seen_pedigrees:
                heapq.heappush(fila_prioridade, (-novo_pedigree.valor, novo_pedigree))
                seen_pedigrees.add(tuple(sorted(novo_pedigree.arestas)))
    
    return ped_lista

def construir_pedigree(pontuacoes, n_individuos, fixo):
    pedigree = Pedigree(n_individuos)
    
    for i, (pai, filho, pontuacao) in enumerate(pontuacoes):
        if i < fixo:
            pedigree.adicionar_conexao(pai, filho, pontuacao, i)
        elif i not in pedigree.indices_usados and not forma_ciclo(pedigree, pai, filho):
            pedigree.adicionar_conexao(pai, filho, pontuacao, i)
            if pedigree.esta_completo():
                break
    
    pedigree.fixo = fixo
    return pedigree

def construir_pedigree_com_particao(pedigree_atual, pontuacoes, fixo):
    # Cria uma cópia do pedigree atual para o novo particionamento
    novo_pedigree = Pedigree(pedigree_atual.n_individuos)
    novo_pedigree.arestas = pedigree_atual.arestas[:]
    novo_pedigree.valor = pedigree_atual.valor
    novo_pedigree.indices_usados = pedigree_atual.indices_usados.copy()
    novo_pedigree.fixo = fixo + 1
    
    # Tenta adicionar novas conexões a partir da posição 'fixo' para construir uma nova partição
    for i in range(fixo, len(pontuacoes)):
        pai, filho, pontuacao = pontuacoes[i]
        if i not in novo_pedigree.indices_usados and not forma_ciclo(novo_pedigree, pai, filho):
            novo_pedigree.adicionar_conexao(pai, filho, pontuacao, i)
            if novo_pedigree.esta_completo():
                return novo_pedigree
    return None

def forma_ciclo(pedigree, pai, filho):
    # Função para verificar se adicionar uma conexão criará um ciclo
    visitados = set()
    return tem_caminho(pedigree, filho, pai, visitados)

def tem_caminho(pedigree, inicio, fim, visitados):
    # Busca em profundidade para verificar se há um caminho do 'inicio' ao 'fim'
    if inicio == fim:
        return True
    visitados.add(inicio)
    for p, f, _ in pedigree.arestas:
        if p == inicio and f not in visitados:
            if tem_caminho(pedigree, f, fim, visitados):
                return True
    return False

# Exemplo de uso
pontuacoes = [
    (0, 1, 0.9),
    (1, 2, 0.85),
    (2, 3, 0.8),
    (3, 4, 0.75),
    (0, 2, 0.6),
    (1, 3, 0.5),
    (2, 4, 0.4)
]

n_individuos = 5
k = 3  # Número de pedigrees de alta pontuação que queremos encontrar

# Executa a busca com particionamento exclusivo
pedigrees_encontrados = particionamento_exclusivo(pontuacoes, n_individuos, k)

# Exibe os pedigrees encontrados
for i, pedigree in enumerate(pedigrees_encontrados, 1):
    print(f"Pedigree {i}:\n{pedigree}\n")
