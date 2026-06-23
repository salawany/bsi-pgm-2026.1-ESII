from abc import ABC, abstractmethod


class MultaStrategy(ABC):
    @abstractmethod
    def calcular(self, dias_atraso: int) -> float:
        pass


class MultaPorDia(MultaStrategy):
    def __init__(self, valor_dia: float):
        self.valor_dia = valor_dia

    def calcular(self, dias_atraso: int) -> float:
        return max(0.0, dias_atraso * self.valor_dia)