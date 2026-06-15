from models.equipamento import Equipamento, Notebook, Projetor, Cabo


class FabricaEquipamento:
    _registro = {
        "notebook": Notebook,
        "projetor": Projetor,
        "cabo": Cabo,
    }

    @classmethod
    def criar(cls, tipo: str, id: int, nome: str) -> Equipamento:
        classe = cls._registro.get(tipo)

        if classe is None:
            raise ValueError(f"Tipo desconhecido: {tipo}")

        return classe(id, nome, tipo)