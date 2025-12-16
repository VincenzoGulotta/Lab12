from math import inf
import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self.rifugi = DAO.get_rifugi()              # Dizionario -> {id_rifugio : "nome_rifugio (localita)"}
        self.connessioni = self.G.edges(data=True)  # Lista di tuple -> [(id_1, id_2, {"attributo" : float})]
        self.tratte_valide = []
        self.G2 = nx.Graph()
        self.cammino_ottimo = []
        self.peso_minimo = float(inf)

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
        for edge in self.connessioni:
            if edge[2]["weight"] > soglia:
                self.tratte_valide.append(edge)

        # Utilizzando la ricorsione
        #self.ricorsione([], 0)

        # Utilizzando networkX
        self.metodo_networkX(soglia)

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
        for edge in self.G.edges(data=True):        # Creo un nuovo grafo a cui aggiungo solamente gli archi che hanno peso
                                                    # maggiore della soglia, così che posso iterare al suo interno
            if edge[2]["weight"] > soglia:
                self.G2.add_edge(edge[0], edge[1], weight = edge[2]["weight"])
        # Qui ho già il mio nuovo grafo con gli archi filtrati per peso
        # Devo trovare il cammino più breve
        for partenza in self.G2.nodes():        # Itero sui nodi del mio nuovo grafo
            pesi, percorsi = nx.single_source_dijkstra(self.G2, partenza, weight = "weight") # Utilizzo single_source_dijkstra, che restituisce due dizionari
                                                                                             # Aventi chiavi uguali, ad ogni chiave corrisponde un percorso nel secondo dizionario
                                                                                             # e il peso del rispettivo percorso nel primo dizionario

            for arrivo in percorsi:             # Itero tra le chiavi del secondo dizionario, ovvero tra tutti i nodi "destinazione" a cui posso giungere da uno dei
                                                # miei nodi di partenza su cui stavo già iterando

                percorso = percorsi[arrivo]     # Prendo percorso dal mio dizionario percorsi
                if len(percorso) > 2 and arrivo != partenza:    # Verifico che la lunghezza sia > 2, ovvero che siano presenti almeno 3 nodi in quel percorso,
                                                                # quindi almeno 2 tratte
                    peso = pesi[arrivo]                 # Salvo il peso del percorso che sto analizzando
                    if peso < self.peso_minimo:         # Se il peso del percorso è minore del peso ottimo già trovato
                        self.peso_minimo = peso         # Sostituisco il peso ottimo con il peso corrente

                        # SE MI TROVO QUI VUOL DIRE CHE HO DAVANTI UN POTEZIALE PERCORSO OTTIMO

                        # Adesso devo trovare un modo per formattare bene il risultato ottenuto, devo uniformare l'output di questo algoritmo all'output
                        # della ricorsione per non dover modificare view e controller
                        cammino = []
                        for i in range(len(percorso) - 1):  # Itero sugli indici della lunghezza del potenziale percorso migliore
                            nodo_1 = percorso[i]            # Salvo il primo nodo
                            nodo_2 = percorso[i + 1]        # Salvo il secondo nodo
                            peso = self.G2[nodo_1][nodo_2]  # Salvo il peso della tratta
                            tupla = nodo_1, nodo_2, peso    # Creo una tupla (nodo1, nodo2, {"weight" : float})
                            cammino.append(tupla)           # Appendo la tupla al cammino
                        self.cammino_ottimo = cammino       # Aggiorno il cammino ottimo

                        # SE TROVO UN PESO MIGLIORE, QUESTO CAMMINO VERRA' SOVRASCRITTO






