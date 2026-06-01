from abc import ABC, abstractmethod


class IRepositorioEmprestimo(ABC):

    @abstractmethod
    def buscar_equipamento(self, id):
        pass

    @abstractmethod
    def salvar_emprestimo(self, emprestimo):
        pass

    @abstractmethod
    def buscar_emprestimo(self, id):
        pass

    @abstractmethod
    def marcar_indisponivel(self, equip_id):
        pass

    @abstractmethod
    def marcar_disponivel(self, equip_id):
        pass

    @abstractmethod
    def marcar_devolvido(self, emprestimo_id):
        pass

    @abstractmethod
    def listar_em_atraso(self):
        pass

    @abstractmethod
    def proximo_id_emprestimo(self):
        pass