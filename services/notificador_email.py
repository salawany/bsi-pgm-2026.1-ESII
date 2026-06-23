from services.evento import Evento
from services.observer import Observer


class NotificadorEmail(Observer):
    def update(self, evento: Evento) -> None:
        if evento.tipo == "emprestimo":
            print(f"[EMAIL] {evento.email} — empréstimo até {evento.data}")

        elif evento.tipo == "devolucao":
            print(f"[EMAIL] {evento.email} — multa R${evento.multa:.2f}")

        elif evento.tipo == "atraso":
            print(f"[EMAIL] {evento.email} — você está em atraso!")