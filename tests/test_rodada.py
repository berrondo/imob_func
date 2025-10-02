from imob import rodada


def test_criar_rodada():
    r = rodada.criar_rodada(2)

    assert r.indices == [0, 1]
    assert r.da_vez == 0

    r2 = rodada.proximo(r)
    assert r2.indices == [0, 1]
    assert r2.da_vez == 1
    assert r2.rodadas == 0

    r3 = rodada.proximo(r2)
    assert r3.indices == [0, 1]
    assert r3.da_vez == 0
    assert r3.rodadas == 1

    r4 = rodada.remover(r3, 0)
    assert r4.indices == [1]
    assert r4.da_vez == 1
    assert r4.tamanho == 1
    assert r3.rodadas == 1
