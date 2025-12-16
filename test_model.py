from math import inf

from model.model import Model
from database.dao import DAO
import networkx as nx

model = Model()
for i in range(1,51):
    rifugio = model.traduci_id(i)
    #print(rifugio)
"dao.get_rifugi funziona"
"model.traduci_id funziona"

model.build_weighted_graph(2000)
counter = 0
for node in model.G.nodes():
    counter += 1
    #print(node)
print(counter)

print(model.get_edges_weight_min_max())
print(model.count_edges_by_threshold(4))

print(model.get_mostra_cammino_minimo(4))

# Verifico che il filtro creato in model.metodo_networkx() funzioni contando il numero di tratte presenti
model.metodo_networkX(4)
i = 0
for item in model.G2.edges(data=True):
    #print(item[0],item[1],item[2]["weight"])
    i += 1
print(i)

"""Utilizzo di single_source_dijkstra per iterare in networkx"""

cammino_ottimo = []
peso_minimo = float(inf)
for partenza in model.G2.nodes():
    weight, paths = nx.single_source_dijkstra(model.G2, partenza, weight = "weight")

    for arrivo in paths:
        path = paths[arrivo]
        if arrivo != partenza and len(path) > 2:
            peso = weight[arrivo]
            if peso < peso_minimo:
                peso_minimo = peso
                cammino_ottimo = path

cammino = []
for i in range(len(cammino_ottimo)-1):
    nodo_1 = cammino_ottimo[i]
    nodo_2 = cammino_ottimo[i+1]
    peso = model.G2[nodo_1][nodo_2]
    tupla = nodo_1, nodo_2, peso
    cammino.append(tupla)
#print(cammino)



