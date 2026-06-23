from dataclasses import dataclass
from models.multa_strategy import MultaStrategy


@dataclass
class Equipamento:
    id: int
    nome: str
    tipo: str
    multa: MultaStrategy
    disponivel: bool = True

    def calcular_multa(self, dias_atraso: int) -> float:
        return self.multa.calcular(dias_atraso)


@dataclass
class Notebook(Equipamento):
    pass


@dataclass
class Projetor(Equipamento):
    pass


@dataclass
class Cabo(Equipamento):
    pass