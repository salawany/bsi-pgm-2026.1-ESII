import datetime

from desconto import calcular_desconto_devolucao_antecipada


def test_sem_desconto_quando_devolve_no_prazo():
    data_prevista = datetime.date(2026, 6, 10)
    data_devolucao = datetime.date(2026, 6, 10)

    desconto = calcular_desconto_devolucao_antecipada(
        data_prevista=data_prevista,
        data_devolucao=data_devolucao,
        valor_por_dia=5.0
    )

    assert desconto == 0.0