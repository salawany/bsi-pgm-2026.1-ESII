def test_registrar_emprestimo(servico, repositorio):
    resultado = servico.registrar(
        1,
        "Sávila",
        "savila@email.com",
        7
    )

    assert resultado is True

    equipamento = repositorio.buscar_equipamento(1)

    assert equipamento.disponivel is False

import datetime


def test_registrar_emprestimo(servico, repositorio):
    resultado = servico.registrar(
        1,
        "Sávila",
        "savila@email.com",
        7
    )

    assert resultado is True

    equipamento = repositorio.buscar_equipamento(1)

    assert equipamento.disponivel is False


def test_registrar_equipamento_indisponivel(servico):
    servico.registrar(
        1,
        "Primeiro",
        "primeiro@email.com",
        7
    )

    resultado = servico.registrar(
        1,
        "Segundo",
        "segundo@email.com",
        7
    )

    assert resultado is False


def test_devolver_emprestimo(servico, repositorio):
    servico.registrar(
        1,
        "Sávila",
        "savila@email.com",
        7
    )

    servico.devolver(1)

    equipamento = repositorio.buscar_equipamento(1)
    emprestimo = repositorio.buscar_emprestimo(1)

    assert equipamento.disponivel is True
    assert emprestimo.devolvido is True


def test_listar_atrasados_sem_registros(servico):
    servico.listar_atrasados()


def test_emprestimo_fica_registrado(servico, repositorio):
    servico.registrar(
        2,
        "Aluno",
        "aluno@email.com",
        5
    )

    emprestimo = repositorio.buscar_emprestimo(1)

    assert emprestimo is not None
    assert emprestimo.usuario_nome == "Aluno"


def test_emprestimo_atrasado_aparece_na_lista(servico, repositorio):
    servico.registrar(
        3,
        "Aluno",
        "aluno@email.com",
        1
    )

    emprestimo = repositorio.buscar_emprestimo(1)

    emprestimo.data_devolucao = (
        datetime.date.today() - datetime.timedelta(days=3)
    )

    atrasados = repositorio.listar_em_atraso()

    assert len(atrasados) == 1