from dataclasses import dataclass

@dataclass()
class Vendita:
    product_id: str
    num_vendite: int


    def __str__(self):
        return f"Vendita(id={self.product_id})"

    def __repr__(self):
        return f"Vendita(id={self.product_id})"

    def __hash__(self):
        return hash(self.product_id)