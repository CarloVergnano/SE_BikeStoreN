from model.model import Model
m = Model()
grafo = m.crea_grafo(7, "2016-01-01 00:00:00", "2018-12-28 00:00:00")
print(grafo)
result = m.calcola_peso_nodo(48)
print(result)