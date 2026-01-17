from dataclasses import dataclass

@dataclass()
class Prodotto:
    id: int
    product_name : str


    def __str__(self):
        return f"Prodotto(id={self.id})"

    def __repr__(self):
        return f"Prodotto(id={self.id})"

    def __hash__(self):
        return hash(self.id)