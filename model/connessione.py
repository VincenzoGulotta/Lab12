from dataclasses import dataclass

@dataclass
class Connessione:
    id_rifugio1 : int
    id_rifugio2 : int
    peso : float

    def __str__(self):
        return f"{self.id_rifugio1}, {self.id_rifugio2}, {self.peso}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id_rifugio1 == other.id_rifugio1 and self.id_rifugio2 == other.id_rifugio2

    def __lt__(self, other):
        return self.peso < other.peso

    def __hash__(self):
        return hash(self.peso)

