def calcular_multa_com_carencia(
    dias_atraso,
    valor_por_dia,
    carencia
):
    dias_cobrados = max(0, dias_atraso - carencia)
    return dias_cobrados * valor_por_dia