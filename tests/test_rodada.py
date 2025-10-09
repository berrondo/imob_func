from imob import rodada


def test_rodada_proximo():
    r = rodada.criar_rodada(2)

    assert r.indices == [0, 1]
    assert r.turno == -1

    rodadas = []
    for _ in range(5):
        r = rodada.proximo(r)
        rodadas.append(r)

    assert rodadas[0].indices == [0, 1]
    assert rodadas[0].turno == 0
    assert rodadas[0].rodadas == 0

    assert rodadas[1].turno == 1
    assert rodadas[1].rodadas == 0

    assert rodadas[2].turno == 0
    assert rodadas[2].rodadas == 1

    assert rodadas[3].turno == 1
    assert rodadas[3].rodadas == 1

    assert rodadas[4].turno == 0
    assert rodadas[4].rodadas == 2


def test_rodada_proximo_com_remover():
    r = rodada.criar_rodada(2)

    assert r.indices == [0, 1]
    assert r.turno == -1

    # remover nao tem efeito antes da primeira chamada a proximo
    # porque o turno inicial é -1
    # r = rodada.remover(r, 0)
    # assert r.removidos == []

    rodadas = []
    for i in range(5):
        r = rodada.proximo(r)
        if i == 2:
            r = rodada.remover(r, i)
        rodadas.append(r)

    assert rodadas[0].indices == [0, 1]
    assert rodadas[0].turno == 0
    assert rodadas[0].rodadas == 0

    assert rodadas[1].turno == 1
    assert rodadas[1].rodadas == 0

    assert rodadas[2].turno == 0
    assert rodadas[2].rodadas == 1
    assert rodadas[2].removidos == [2]
    # removeu o 0

    assert rodadas[3].turno == 1
    assert rodadas[3].rodadas == 1

    assert rodadas[4].turno == 0
    assert rodadas[4].rodadas == 2


def test_rodada_remover():
    r = rodada.criar_rodada(3)
    r = rodada.proximo(r)

    assert rodada.jogando(r) == 3
    assert r.indices == [0, 1, 2]
    assert r.turno == 0
    assert r.tamanho == 3
    assert r.removidos == []
    assert r.rodadas == 0

    r2 = rodada.remover(r, 1)

    assert rodada.jogando(r2) == 2
    assert r2.indices == [0, 1, 2]
    assert r2.turno == 0
    assert r2.tamanho == 3
    assert r2.removidos == [1]
    assert r2.rodadas == 0

    r3 = rodada.proximo(r2)

    assert rodada.jogando(r3) == 2
    assert r3.indices == [0, 1, 2]
    assert r3.turno == 2
    assert r3.tamanho == 3
    assert r3.removidos == [1]
    assert r3.rodadas == 0
