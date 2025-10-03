from imob import rodada


def test_rodada_proximo():
    r = rodada.criar_rodada(2)

    assert r.indices == [0, 1]
    assert r.da_vez == -1

    rodadas = []
    for _ in range(5):
        r = rodada.proximo(r)
        rodadas.append(r)

    assert rodadas[0].indices == [0, 1]
    assert rodadas[0].da_vez == 0
    assert rodadas[0].rodadas == 0

    assert rodadas[1].da_vez == 1
    assert rodadas[1].rodadas == 0

    assert rodadas[2].da_vez == 0
    assert rodadas[2].rodadas == 1

    assert rodadas[3].da_vez == 1
    assert rodadas[3].rodadas == 1

    assert rodadas[4].da_vez == 0
    assert rodadas[4].rodadas == 2


def test_rodada_proximo_com_remover():
    r = rodada.criar_rodada(2)

    assert r.indices == [0, 1]
    assert r.da_vez == -1

    rodadas = []
    for i in range(5):
        r = rodada.proximo(r)
        if i == 2:
            r = rodada.remover(r, 1)
        rodadas.append(r)

    assert rodadas[0].indices == [0, 1]
    assert rodadas[0].da_vez == 0
    assert rodadas[0].rodadas == 0

    assert rodadas[1].da_vez == 1
    assert rodadas[1].rodadas == 0

    assert rodadas[2].da_vez == 0
    assert rodadas[2].rodadas == 1
    assert rodadas[2].removidos == [1]
    # removeu o 1

    assert rodadas[3].da_vez == 0
    assert rodadas[3].rodadas == 2

    assert rodadas[4].da_vez == 0
    assert rodadas[4].rodadas == 3


def test_rodada_remover():
    r = rodada.criar_rodada(3)

    assert rodada.jogando(r) == 3
    assert r.indices == [0, 1, 2]
    assert r.da_vez == -1
    assert r.tamanho == 3
    assert r.removidos == []
    assert r.rodadas == 0

    r2 = rodada.remover(r, 0)

    assert rodada.jogando(r2) == 2
    assert r2.indices == [0, 1, 2]
    assert r2.da_vez == -1
    assert r2.tamanho == 3
    assert r2.removidos == [0]
    assert r2.rodadas == 0
