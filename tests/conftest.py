import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest  # type: ignore

from repositories.repositorio_emprestimo import RepositorioEmprestimo
from services.evento import Evento
from services.observer import Observer
from services.servico_emprestimo import ServicoEmprestimo


class NotificadorSpy(Observer):
    def __init__(self):
        self.eventos = []

    def update(self, evento: Evento) -> None:
        self.eventos.append(evento)


@pytest.fixture
def repositorio():
    return RepositorioEmprestimo()


@pytest.fixture
def notificador_spy():
    return NotificadorSpy()


@pytest.fixture
def servico(repositorio, notificador_spy):
    servico = ServicoEmprestimo(repositorio)
    servico.registrar_observer(notificador_spy)
    return servico