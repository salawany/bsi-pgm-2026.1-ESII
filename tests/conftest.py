import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest  # type: ignore

from repositories.repositorio_emprestimo import RepositorioEmprestimo
from services.notificador import Notificador
from services.servico_emprestimo import ServicoEmprestimo


@pytest.fixture
def repositorio():
    return RepositorioEmprestimo()


@pytest.fixture
def notificador():
    return Notificador()


@pytest.fixture
def servico(repositorio, notificador):
    return ServicoEmprestimo(repositorio, notificador)