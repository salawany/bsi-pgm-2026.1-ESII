import datetime
from models.emprestimo import Emprestimo
from repositories.interfaces import IRepositorioEmprestimo
from services.interfaces import INotificador


class ServicoEmprestimo:
    def __init__(
        self,
        repositorio: IRepositorioEmprestimo,
        notificador: INotificador
    ):
        self.repositorio = repositorio
        self.notificador = notificador

    def registrar(self, equipamento_id: int, usuario_nome: str,
                  usuario_email: str, dias: int) -> bool:
        equipamento = self.repositorio.buscar_equipamento(equipamento_id)
        if equipamento is None or not equipamento.disponivel:
            print("Equipamento inválido ou indisponível")
            return False

        data_emprestimo = datetime.date.today()
        data_devolucao  = data_emprestimo + datetime.timedelta(days=dias)

        emprestimo = Emprestimo(
            id=self.repositorio.proximo_id_emprestimo(),
            equipamento_id=equipamento_id,
            equipamento_nome=equipamento.nome,
            tipo=equipamento.tipo,
            usuario_nome=usuario_nome,
            usuario_email=usuario_email,
            data_emprestimo=data_emprestimo,
            data_devolucao=data_devolucao,
        )
        self.repositorio.salvar_emprestimo(emprestimo)
        self.repositorio.marcar_indisponivel(equipamento_id)
        self.notificador.notificar_emprestimo(usuario_email, data_devolucao)
        return True

    def devolver(self, emprestimo_id: int) -> None:
        emprestimo = self.repositorio.buscar_emprestimo(emprestimo_id)
        if emprestimo is None or emprestimo.devolvido:
            print("Empréstimo inválido ou já devolvido")
            return

        hoje        = datetime.date.today()
        atraso      = (hoje - emprestimo.data_devolucao).days
        equipamento = self.repositorio.buscar_equipamento(emprestimo.equipamento_id)
        multa       = equipamento.calcular_multa(atraso)

        self.repositorio.marcar_devolvido(emprestimo_id)
        self.repositorio.marcar_disponivel(emprestimo.equipamento_id)
        self.notificador.notificar_devolucao(emprestimo.usuario_email, multa)
        print(f"Devolução registrada. Multa: R${multa:.2f}")

    def listar_atrasados(self) -> None:
        hoje = datetime.date.today()
        atrasados = self.repositorio.listar_em_atraso()
        if not atrasados:
            print("Nenhum empréstimo em atraso.")
            return
        for emprestimo in atrasados:
            atraso      = (hoje - emprestimo.data_devolucao).days
            equipamento = self.repositorio.buscar_equipamento(emprestimo.equipamento_id)
            multa       = equipamento.calcular_multa(atraso)
            print(f"{emprestimo.usuario_nome} — {atraso} dias — R${multa:.2f}")
            self.notificador.notificar_atraso(emprestimo.usuario_email)
