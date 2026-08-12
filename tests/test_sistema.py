from app.sistema import SistemaDeEmprestimos


def test_criar_sistema():
    sistema = SistemaDeEmprestimos()

    assert sistema is not None
    assert sistema._repositorio is not None
    assert sistema._servico is not None
    
def test_registrar_emprestimo():
    sistema = SistemaDeEmprestimos()

    sistema._servico.registrar = lambda equipamento_id, nome, email, dias: True

    resultado = sistema.registrar(1, "João", "joao@email.com", 5)

    assert resultado is True