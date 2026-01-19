from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.categorie = []
        self.prodotti = []
        self.connessioni = []

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categorie(self):
        self.categorie = DAO.get_categorie()
        return self.categorie

    def get_prodotti(self, categoria):
        self.prodotti = DAO.get_prodotti(categoria)
        return self.prodotti

    def crea_grafo(self, categoria, data_inizio, data_fine):
        self.connessioni = DAO.get_connessioni(categoria, data_inizio, data_fine)
        self.prodotti = DAO.get_prodotti(categoria)
        for c1 in self.connessioni:
            for c2 in self.connessioni:
                if c1.id != c2.id:
                    if c1.num_vendite > c2.num_vendite:
                        peso = c1.num_vendite+c2.num_vendite
                        self.G.add_edge(c1.id, c2.id, weight=peso)
                    if c2.num_vendite > c1.num_vendite:
                        peso = c1.num_vendite+c2.num_vendite
                        self.G.add_edge(c2.id, c1.id, weight=peso)
                    if c1.num_vendite == c2.num_vendite:
                        peso = c1.num_vendite+c2.num_vendite
                        self.G.add_edge(c1.id, c2.id, weight=peso)
                        self.G.add_edge(c2.id, c1.id, weight=peso)
        for c in self.prodotti:
            if c not in self.connessioni:
                self.G.add_node(c.id)


        return self.G

    def calcola_peso_nodo(self, product_id):
        valore = 0
        for arco_out in self.G.out_edges(product_id, data=True):
            valore = valore + arco_out[2]["weight"]

        for arco_in in self.G.in_edges(product_id, data=True):
            valore = valore - arco_in[2]["weight"]

        return valore
