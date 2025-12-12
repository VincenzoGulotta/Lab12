from model.model import Model
from database.dao import DAO

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
    print(node)
print(counter)

print(model.get_edges_weight_min_max())
print(model.count_edges_by_threshold(4))

print(model.get_mostra_cammino_minimo(4))

print(item for item in model.metodo_dijkstra(4))