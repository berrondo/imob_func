from imob.banco import Banco, creditar_em, criar_banco, debitar_de, saldo_de


def test_criar_banco(jogadores):
    b = criar_banco(4, 300)
    assert isinstance(b, Banco)
    assert b.contas == [300, 300, 300, 300]


def test_saldo(jogadores):
    b = criar_banco(1, 300)

    assert saldo_de(b, 0) == 300

    b = creditar_em(b, 0, 100)
    assert saldo_de(b, 0) == 400

    b = debitar_de(b, 0, 50)
    assert saldo_de(b, 0) == 350

    # saldo fica negativo
    b = debitar_de(b, 0, 400)
    assert saldo_de(b, 0) == -50
