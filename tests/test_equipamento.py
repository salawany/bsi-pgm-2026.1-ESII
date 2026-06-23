from models.fabrica_equipamento import FabricaEquipamento


def test_multa_notebook_sem_atraso():
    notebook = FabricaEquipamento.criar(
        "notebook", 1, "Notebook Dell"
    )

    multa = notebook.calcular_multa(0)

    assert multa == 0.0


def test_multa_notebook_com_atraso():
    notebook = FabricaEquipamento.criar(
        "notebook", 1, "Notebook Dell"
    )

    multa = notebook.calcular_multa(3)

    assert multa == 30.0


def test_multa_projetor_com_atraso():
    projetor = FabricaEquipamento.criar(
        "projetor", 2, "Projetor Epson"
    )

    multa = projetor.calcular_multa(2)

    assert multa == 30.0


def test_multa_cabo_com_atraso():
    cabo = FabricaEquipamento.criar(
        "cabo", 3, "Cabo HDMI"
    )

    multa = cabo.calcular_multa(5)

    assert multa == 10.0