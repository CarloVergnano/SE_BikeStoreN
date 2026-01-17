from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.categorie = []
        self.prodotti = []
        self.vendite = []

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categorie(self):
        self.categorie = DAO.get_categorie()
        return self.categorie

    def get_prodotti(self, categoria):
        self.prodotti = DAO.get_prodotti(categoria)
        return self.prodotti

    def get_vendite(self, start, end, categoria):
        self.vendite = DAO.get_vendite(start, end, categoria)
        return self.vendite

    def crea_grafo(self):
        self.G.clear()
        #self.G.add_nodes_from(self.prodotti)
        for vendita1 in self.vendite:
            for vendita2 in self.vendite:
                if vendita1 != vendita2:
                    peso = int(vendita1.num_vendite + vendita2.num_vendite)
                    if vendita1.num_vendite > vendita2.num_vendite:
                            self.G.add_edge(vendita1.product_id, vendita2.product_id, weight = peso)
                    if vendita1.num_vendite < vendita2.num_vendite:
                            self.G.add_edge(vendita2.product_id, vendita1.product_id, weight = peso)
                    if vendita1.num_vendite == vendita2.num_vendite:
                            self.G.add_edge(vendita1.product_id, vendita2.product_id, weight=peso)
                            self.G.add_edge(vendita2.product_id, vendita1.product_id, weight=peso)
        nodi = list(self.G.nodes())
        for prodotto in self.prodotti:
            for nodo in nodi:
                if nodo != prodotto.id:
                   self.G.add_node(prodotto.id)
        return self.G.number_of_nodes(), self.G.number_of_edges()

    def prodotti_best_seller(self):
        self.vendite.sort(key=lambda x: x.num_vendite, reverse=True)
        return self.vendite[:5]

    def prodotto_to_nome(self, id):
        product_name = id
        for prodotto in self.prodotti:
            if prodotto.id == id:
                product_name = prodotto.product_name
        return product_name

    def calcola_peso_nodo(self, product_id):
        valore = 0
        for arco_out in self.G.out_edges(product_id, data=True):
                valore = valore + arco_out[2]["weight"]
        for arco_in in self.G.in_edges(product_id, data=True):
                valore = valore - arco_in[2]["weight"]
        return valore

    """
        peso_in_tot = 0.0
        peso_out_tot = 0.0
        for nodo in self.G.successors(product_id):
            peso_in = (self.G[product_id][nodo]['weight'])
            peso_in_tot += peso_in
            if self.G.has_edge(nodo, product_id):
                peso_out = self.G[nodo][product_id]['weight']
            else:
                peso_out = 0
            peso_out_tot += peso_out
        peso = peso_in_tot-peso_out_tot
        return peso
        """

    def trova_cammino_ottimo(self, prodotto_iniziale, prodotto_finale, lunghezza_cammino):
        self.best_path = []
        self.best_weight = 0

        # avvio ricorsione
        self._ricorsione(
            nodo_corrente=prodotto_iniziale,
            nodo_finale=prodotto_finale,
            L=lunghezza_cammino,
            cammino=[prodotto_iniziale],
            peso_corrente=0,
            visitati={prodotto_iniziale}
        )

        return self.best_path, self.best_weight

    def _ricorsione(self, nodo_corrente, nodo_finale, L,
                    cammino, peso_corrente, visitati):

        # 🔹 caso base: lunghezza cammino raggiunta
        if len(cammino) == L:
            if nodo_corrente == nodo_finale:
                if peso_corrente > self.best_weight:
                    self.best_weight = peso_corrente
                    self.best_path = cammino.copy()
            return

        # 🔹 esplorazione archi uscenti
        for succ in self.G.successors(nodo_corrente):

            if succ not in visitati:
                peso_arco = self.G[nodo_corrente][succ]['weight']

                # scelta
                visitati.add(succ)
                cammino.append(succ)

                self._ricorsione(
                    nodo_corrente=succ,
                    nodo_finale=nodo_finale,
                    L=L,
                    cammino=cammino,
                    peso_corrente=peso_corrente + peso_arco,
                    visitati=visitati
                )

                # backtracking
                visitati.remove(succ)
                cammino.pop()
