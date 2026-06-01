from models.equipamento import Notebook, Projetor, Cabo


def test_multa_notebook_sem_atraso():
    notebook = Notebook(1, "Notebook Dell", "notebook")

    multa = notebook.calcular_multa(0)

    assert multa == 0.0


def test_multa_notebook_com_atraso():
    notebook = Notebook(1, "Notebook Dell", "notebook")

    multa = notebook.calcular_multa(3)

    assert multa == 30.0


def test_multa_projetor_com_atraso():
    projetor = Projetor(2, "Projetor Epson", "projetor")

    multa = projetor.calcular_multa(2)

    assert multa == 30.0


def test_multa_cabo_com_atraso():
    cabo = Cabo(3, "Cabo HDMI", "cabo")

    multa = cabo.calcular_multa(5)

    assert multa == 10.0