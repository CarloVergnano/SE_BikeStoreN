from UI.view import View
from model.model import Model
import flet as ft
import datetime
from database.DB_connect import DBConnect

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._connessione_db = DBConnect.get_connection()
        if self._connessione_db is None:
            self._view.show_alert("❌ Errore di connessione al database")

    def set_dates(self):
        if self._connessione_db is None:
            self._view.show_alert("❌ Errore di connessione al database")
            return
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

        self.categorie = self._model.get_categorie()
        self._view.dd_category.options.clear()
        if self.categorie:
            for categoria in self.categorie:
                self._view.dd_category.options.append(ft.dropdown.Option(categoria.id, f"{categoria.category_name} ({categoria.id})"))
        else:
            self._view.show_alert("Errore nel caricamento deglle categorie.")
        self._view.dd_category.disabled = False
        self._view.update()

    def popola_categorie(self):
        self._view.dd_category.options.clear()

        categorie = self._model.get_categorie()

        if categorie:
            for c in categorie:
                self._view.dd_category.options.append(ft.dropdown.Option(key=c.id, text=c.category_name))
        else:
            self._view.show_alert("Errore nel caricamento categorie.")

        self._view.update()

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        categoria_selezionata = self._view.dd_category.value
        data_inizio = self._view.dp1.value
        data_fine = self._view.dp2.value
        grafo = self._model.crea_grafo(categoria_selezionata, data_inizio, data_fine)
        num_nodi = grafo.number_of_nodes()
        num_archi = grafo.number_of_edges()
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(
            ft.Text(f"Date selezionate: "))
        self._view.txt_risultato.controls.append(
            ft.Text(f"Start date: {data_inizio.year}-{data_inizio.month}-{data_inizio.day}"))
        self._view.txt_risultato.controls.append(
            ft.Text(f"End date: {data_fine.year}-{data_fine.month}-{data_fine.day}"))
        self._view.txt_risultato.controls.append(
            ft.Text("Grafo correttamente creato")
        )
        self._view.txt_risultato.controls.append(
            ft.Text(f"Numero di nodi: {num_nodi}")
        )
        self._view.txt_risultato.controls.append(
            ft.Text(f"Numero di archi: {num_archi}")
        )
        self._view.update()


    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        valori = {}
        categoria_selezionata = self._view.dd_category.value
        data_inizio = self._view.dp1.value
        data_fine = self._view.dp2.value
        prodotti = self._model.get_prodotti(categoria_selezionata)
        grafo = self._model.crea_grafo(categoria_selezionata, data_inizio, data_fine)
        for prodotto in grafo:
            valore = self._model.calcola_peso_nodo(prodotto)
            valori[prodotto] = valore
        sorted_valori = sorted(valori.items(), key=lambda x: x[1], reverse=True)
        self._view.txt_risultato.controls.append(
            ft.Text("I 5 prodotti più venduti sono:")
        )
        count = 0
        sorted_valori_id = []
        for i in range (len(sorted_valori)):
            sorted_valori_id.append(sorted_valori[i][0])

        prodotti_dict = {}
        for i in range(len(prodotti)):
            prodotti_dict[prodotti[i].id] = prodotti[i].product_name


        for prodotto in sorted_valori_id:
            if prodotto in prodotti_dict and count < 5:

                count += 1
                self._view.txt_risultato.controls.append(
                    ft.Text(f"{prodotti_dict[prodotto]} with score {valori[prodotto]}")
                )
        self._view.update()



    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
