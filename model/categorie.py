from dataclasses import dataclass

@dataclass()
class Categoria:
    id: int
    category_name: str


    def __str__(self):
        return f"Categoria({self.id}, {self.category_name}"


    def __hash__(self):
        return hash(self.id)