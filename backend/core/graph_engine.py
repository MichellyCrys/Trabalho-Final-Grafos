import networkx as nx
import random
import json
from collections import Counter
from typing import List, Tuple

def load_graph_hin(filepath: str, user_name: str, user_genres: list[str]) -> nx.Graph:
    """
    Constrói a Rede de Informação Heterogênea (HIN) baseada nos dados em JSON.
    """
    G = nx.Graph()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Inclusão tipada de vértices
    G.add_node(user_name, tipo='usuario')
    
    for genero in data['generos']:
        G.add_node(genero, tipo='genero')
        
    for musica in data['musicas']:
        G.add_node(musica['titulo'], tipo='musica_bts', artista=musica['tipo'])

    # Inserção Direcional de Relacionamentos: Usuário <-> Gênero
    for genero in user_genres:
        if genero in data['generos']:
            G.add_edge(user_name, genero)

    # Inserção Direcional de Relacionamentos: Música <-> Gênero
    for musica in data['musicas']:
        G.add_edge(musica['titulo'], musica['genero'])

    return G

def run_random_walk(G: nx.Graph, target_node: str, steps: int = 25000, alpha: float = 0.15) -> List[Tuple[str, int]]:
    """
    Executa o Random Walk with Restart (RWR) nas Cadeias de Markov.
    """
    if target_node not in G:
        raise ValueError("Nó alvo não existe no grafo inicializado.")

    current_node = target_node
    visits = Counter()

    for _ in range(steps):
        # Gatilho de teletransporte (Restart)
        if random.random() < alpha:
            current_node = target_node
        else:
            neighbors = list(G.neighbors(current_node))
            if neighbors:
                current_node = random.choice(neighbors)

        # Contabiliza apenas se o agente parar em uma música do BTS
        if G.nodes[current_node].get('tipo') == 'musica_bts':
            visits[current_node] += 1

    # Retorna rankeado em ordem decrescente
    return sorted(visits.items(), key=lambda x: x[1], reverse=True)