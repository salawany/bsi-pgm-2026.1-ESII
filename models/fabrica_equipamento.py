from models.equipamento import Equipamento, Notebook, Projetor, Cabo
from models.multa_strategy import MultaPorDia


class FabricaEquipamento:
    _registro = {
        "notebook": (Notebook, MultaPorDia(10.0)),
        "projetor": (Projetor, MultaPorDia(15.0)),
        "cabo": (Cabo, MultaPorDia(2.0)),
    }

    @classmethod
    def criar(cls, tipo: str, id: int, nome: str) -> Equipamento:
        config = cls._registro.get(tipo)

        if config is None:
            raise ValueError(f"Tipo desconhecido: {tipo}")

        classe, estrategia = config

        return classe(id, nome, tipo, estrategia)