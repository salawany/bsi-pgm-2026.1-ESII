from repositories.repositorio_emprestimo import RepositorioEmprestimo
from services.notificador import Notificador
from services.servico_emprestimo import ServicoEmprestimo


class SistemaDeEmprestimos:
    """Fachada: esconde a montagem do subsistema e expõe operações simples."""

    def __init__(self):
        self._repositorio = RepositorioEmprestimo()
        self._notificador = Notificador()
        self._servico = ServicoEmprestimo(
            self._repositorio,
            self._notificador
        )

    def registrar(self, equipamento_id, nome, email, dias):
        return self._servico.registrar(equipamento_id, nome, email, dias)

    def devolver(self, emprestimo_id):
        return self._servico.devolver(emprestimo_id)

    def listar_atrasados(self):
        return self._servico.listar_atrasados()