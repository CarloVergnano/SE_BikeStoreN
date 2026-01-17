from dataclasses import dataclass

@dataclass()
class Categoria:
    id: int
    category_name : str


    def __str__(self):
        return f"Categoria(id={self.id})"

    def __repr__(self):
        return f"Categoria(id={self.id})"

    def __hash__(self):
        return hash(self.id)