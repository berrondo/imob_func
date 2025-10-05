import imob.jogador as jogador
from imob.estrategia import impulsivo


def test_criar_jogador():
    j = jogador.criar_jogador(estrategia=impulsivo, saldo=300)

    assert j.estrategia == impulsivo
    assert j.saldo == 300
    assert j.nome == 'impulsivo'


def test_str():
    j = jogador.criar_jogador(estrategia=impulsivo, saldo=300)

    assert str(j) == "impulsivo  $ 300"


def test_creditar():
    j = jogador.criar_jogador(estrategia=impulsivo, saldo=300)

    j2 = jogador.creditar(j, 100)

    assert jogador.tem_saldo_suficiente(j2, 400)
    assert not jogador.tem_saldo_suficiente(j2, 401)
    assert j2.saldo == 400


def test_debitar():
    j = jogador.criar_jogador(estrategia=impulsivo, saldo=300)

    j2 = jogador.debitar(j, 100)

    assert jogador.tem_saldo_suficiente(j2, 200)
    assert not jogador.tem_saldo_suficiente(j2, 201)
    assert j2.saldo == 200
