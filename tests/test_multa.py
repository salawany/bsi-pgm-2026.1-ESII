from multa import calcular_multa_com_carencia


def test_multa_zero_quando_sem_atraso():
    assert calcular_multa_com_carencia(
        dias_atraso=0,
        valor_por_dia=10.0,
        carencia=2
    ) == 0.0