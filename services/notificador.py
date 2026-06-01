from services.interfaces import INotificador

class Notificador(INotificador):
    def notificar_emprestimo(self, email: str, data_devolucao) -> None:
        print(f"[EMAIL] {email} — empréstimo até {data_devolucao}")

    def notificar_devolucao(self, email: str, multa: float) -> None:
        print(f"[EMAIL] {email} — multa R${multa:.2f}")

    def notificar_atraso(self, email: str) -> None:
        print(f"[EMAIL] {email} — você está em atraso!")
