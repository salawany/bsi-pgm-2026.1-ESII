def test_fluxo_completo(servico, repositorio):
    resultado = servico.registrar(
        1,
        "Aluno",
        "aluno@email.com",
        5
    )

    assert resultado is True

    equipamento = repositorio.buscar_equipamento(1)
    assert equipamento.disponivel is False

    servico.devolver(1)

    emprestimo = repositorio.buscar_emprestimo(1)

    assert emprestimo.devolvido is True
    assert equipamento.disponivel is True