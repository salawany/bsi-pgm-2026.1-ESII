import datetime
from models.equipamento import Notebook, Projetor, Cabo
from models.emprestimo import Emprestimo
from repositories.interfaces import IRepositorioEmprestimo

class RepositorioEmprestimo(IRepositorioEmprestimo):
    def __init__(self):
        self._equipamentos = [
            Notebook(1, "Notebook Dell",  "notebook"),
            Projetor(2, "Projetor Epson", "projetor"),
            Cabo(3,     "Cabo HDMI",      "cabo"),
        ]
        self._emprestimos = []

    def buscar_equipamento(self, id: int):
        return next((e for e in self._equipamentos if e.id == id), None)

    def salvar_emprestimo(self, emprestimo: Emprestimo) -> None:
        self._emprestimos.append(emprestimo)

    def buscar_emprestimo(self, id: int):
        return next((e for e in self._emprestimos if e.id == id), None)

    def marcar_indisponivel(self, equip_id: int) -> None:
        equip = self.buscar_equipamento(equip_id)
        if equip:
            equip.disponivel = False

    def marcar_disponivel(self, equip_id: int) -> None:
        equip = self.buscar_equipamento(equip_id)
        if equip:
            equip.disponivel = True

    def marcar_devolvido(self, emprestimo_id: int) -> None:
        emp = self.buscar_emprestimo(emprestimo_id)
        if emp:
            emp.devolvido = True

    def listar_em_atraso(self):
        hoje = datetime.date.today()
        return [e for e in self._emprestimos
                if not e.devolvido and e.data_devolucao < hoje]

    def proximo_id_emprestimo(self) -> int:
        return len(self._emprestimos) + 1
