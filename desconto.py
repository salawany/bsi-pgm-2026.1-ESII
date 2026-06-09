def calcular_desconto_devolucao_antecipada(
    data_prevista,
    data_devolucao,
    valor_por_dia
):
    dias_adiantados = _calcular_dias_adiantados(
        data_prevista,
        data_devolucao
    )

    return dias_adiantados * valor_por_dia


def _calcular_dias_adiantados(
    data_prevista,
    data_devolucao
):
    return (data_prevista - data_devolucao).days