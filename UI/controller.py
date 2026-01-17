from UI.view import View
from model.model import Model
import flet as ft
import datetime
from database.DB_connect import DBConnect

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.categorie = []
        self.categoria_selezionata = None
        self.prodotti = []
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

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        self.categoria_selezionata = self._view.dd_category.value
        if self.categoria_selezionata is None:
            self._view.show_alert("Selezionare una categoria.")
            return
        self.prodotti = self._model.get_prodotti(self.categoria_selezionata)
        if self._view.dp1.value is None or self._view.dp2.value is None:
            self._view.show_alert("Selezionare le date")
            return
        start_data = str(self._view.dp1.value.date())
        end_data = str(self._view.dp2.value.date())
        self._model.get_vendite(start_data, end_data, self.categoria_selezionata)
        nodi, rami = self._model.crea_grafo()
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f"Date selezionate:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Start date: {start_data}"))
        self._view.txt_risultato.controls.append(ft.Text(f"End date: {end_data}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Grafo correttamente creato"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero nodi: {nodi}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero archi: {rami}"))
        self._view.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        best_seller = self._model.prodotti_best_seller()
        self._view.txt_risultato.controls.append(ft.Text(f" "))
        self._view.txt_risultato.controls.append(ft.Text(f"I cinque prodotti più venduti sono:"))
        for prodotto in best_seller:
            self._view.txt_risultato.controls.append(ft.Text(f"{self._model.prodotto_to_nome(prodotto.product_id)} with score {self._model.calcola_peso_nodo(prodotto.product_id)}"))
        self._view.update()

        self._view.dd_prodotto_iniziale.options.clear()
        self._view.dd_prodotto_finale.options.clear()
        for prodotto in self.prodotti:
            self._view.dd_prodotto_iniziale.options.append(ft.dropdown.Option(prodotto.id, f"{prodotto.product_name} ({prodotto.id})"))
            self._view.dd_prodotto_finale.options.append(ft.dropdown.Option(prodotto.id, f"{prodotto.product_name} ({prodotto.id})"))
        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        lunghezza_cammino = self._view.txt_lunghezza_cammino.value
        prodotto_iniziale = self._view.dd_prodotto_iniziale.value
        prodotto_finale = self._view.dd_prodotto_finale.value
        controllo_inserimento_tastiera = True
        if lunghezza_cammino is None or lunghezza_cammino == "":
            self._view.show_alert("Inserire lunghezza del cammino.")
            controllo_inserimento_tastiera = False
            return
        if prodotto_iniziale is None or prodotto_finale is None:
            self._view.show_alert("selezionare prodotto")
            controllo_inserimento_tastiera = False
            return
        try:
            lunghezza_cammino = int(lunghezza_cammino)
        except (ValueError, TypeError):
            self._view.show_alert("Inserire lunghezza del cammino in un formato corretto")
            controllo_inserimento_tastiera = False
        if controllo_inserimento_tastiera:
            print(self._model.trova_cammino_ottimo(prodotto_iniziale, prodotto_finale, lunghezza_cammino))