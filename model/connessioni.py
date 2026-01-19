from dataclasses import dataclass

@dataclass()
class Connessione:
    id: int
    product_name: str
    num_vendite: int


    def __str__(self):
        return f"Connessione({self.id}, {self.product_name}, {self.num_vendite})"


    def __hash__(self):
        return hash(self.id)