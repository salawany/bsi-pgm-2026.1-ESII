def calcular_desconto_devolucao_antecipada(
    data_prevista,
    data_devolucao,
    valor_por_dia
):
    dias_adiantados = (data_prevista - data_devolucao).days
    return dias_adiantados * valor_por_dia