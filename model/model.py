from math import inf
import networkx as nx
from networkx.algorithms.shortest_paths.weighted import all_pairs_dijkstra_path

from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self.rifugi = DAO.get_rifugi()              # Dizionario -> {id_rifugio : "nome_rifugio (localita)"}
        self.connessioni = self.G.edges(data=True)  # Lista di tuple -> [(id_1, id_2, {"attributo" : float})]
        self.tratte_valide = []

        # TODO

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        connessioni = DAO.get_connessioni_anno(year)    #lista di oggetti Connessione
        for arco in connessioni:
            rifugio1 = self.traduci_id(arco.id_rifugio1)
            rifugio2 = self.traduci_id(arco.id_rifugio2)
            self.G.add_edge(rifugio1, rifugio2, weight = arco.peso) # Creo il grafo già con "nome_rifugio (località)" per
                                                                    # facilitare la stampa al punto 2

    def traduci_id(self, id_rifugio):
        return self.rifugi[id_rifugio]      # prendo dalla lista dei rifugi (dizionario) il nome e la località

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        max_edge = -1
        min_edge = float(inf)
        for edge in self.connessioni:
            if edge[2]["weight"] > max_edge:
                max_edge = edge[2]["weight"]
            if edge[2]["weight"] < min_edge:
                min_edge = edge[2]["weight"]
        return min_edge, max_edge

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        counter_plus = 0
        counter_minus = 0
        for edge in self.connessioni:
            if edge[2]["weight"] < soglia:
                counter_minus += 1
            elif edge[2]["weight"] > soglia:
                counter_plus += 1

        # Qui preparo già le tratte valide per la ricerca del cammino più breve

        return counter_minus, counter_plus

    """Implementare la parte di ricerca del cammino minimo"""

    def get_mostra_cammino_minimo(self, soglia):
        self.cammino_ottimo = []
        self.peso_minimo = float(inf)
        for edge in self.connessioni:
            if edge[2]["weight"] > soglia:
                self.tratte_valide.append(edge)

        # Utilizzando la ricorsione
        self.ricorsione([], 0)
        # Utilizzando un metodo di NetworkX
        #self.metodo_dijkstra(soglia)
        return self.cammino_ottimo   # Ritorna una tupla con una lista di tratte e un valore numerico "peso"


    def ricorsione(self, cammino_parziale, peso_parziale):
        if len(cammino_parziale) >= 2 and peso_parziale < self.peso_minimo:
            self.cammino_ottimo = cammino_parziale
            self.peso_minimo = peso_parziale


        for tratta in self.tratte_valide:
            if len(cammino_parziale) != 0 and tratta[0] == cammino_parziale[-1][1]:
                nuovo_peso = peso_parziale + tratta[2]['weight']
                nuovo_cammino = cammino_parziale + [tratta]
                self.ricorsione(nuovo_cammino, nuovo_peso)

            elif len(cammino_parziale) == 0:
                nuovo_peso = peso_parziale + tratta[2]['weight']
                nuovo_cammino = cammino_parziale + [tratta]
                self.ricorsione(nuovo_cammino, nuovo_peso)

    def metodo_networkX(self, soglia):
        G2 = nx.Graph()
        for edge in self.G.edges(data=True):        # Creo un nuovo grafo a cui aggiungo solamente gli archi che hanno peso
                                                    # maggiore della soglia, così che posso iterare al suo interno
            if edge[2]["weight"] > soglia:
                G2.add_edge(edge[0], edge[1], weight = edge[2]["weight"])
        # TODO
