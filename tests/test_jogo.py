from imob import jogo


def test_criar_jogo(propriedades, jogadores):
    js = jogadores
    jg = jogo.criar_jogo(propriedades, js) #[js[0], js[1]])

    assert jg.tabuleiro

    assert jogadores[0].nome == 'impulsivo'

    jg1 = jogo.jogar(jg, maximo=1)

    # assert jg1.rodadas.tamanho == 1
    # assert jg1.rodadas.indices == [0]
    assert jg1.rodadas.rodadas == 0

    # assert jg1.rodadas.indices == [0, 1, 2, 3]
    # assert jg1.rodadas.turno == 0
    # assert jg1.tabuleiro.jogadores[0].nome == 'impulsivo'
    # assert jg1.tabuleiro.jogadores[0].saldo == 200

    # jg2 = jogo.jogar(jg1)

    # assert jg2.rodadas.turno == 1

    # jg3 = jogo.jogar(jg2)

    # assert jg3.rodadas.turno == 2

    # jg4 = jogo.jogar(jg3)

    # assert jg4.rodadas.turno == 3
    # assert jg4.rodadas.rodadas == 0

    # jg5 = jogo.jogar(jg4)

    # assert jg5.rodadas.turno == 0
    # assert jg5.rodadas.rodadas == 1


def test_rodadas(propriedades, jogadores):
    jg = jogo.criar_jogo(propriedades, jogadores)

    assert jg.rodadas.tamanho == 4
    assert jg.rodadas.indices == [0, 1, 2, 3]
    assert jg.rodadas.turno == -1
    assert jg.rodadas.rodadas == 0

    jg2 = jogo.proxima_rodada(jg)

    assert jg2.rodadas.tamanho == 4
    assert jg2.rodadas.indices == [0, 1, 2, 3]
    assert jg2.rodadas.turno == 0
    assert jg2.rodadas.rodadas == 0

    jg3 = jogo.proxima_rodada(jg2)

    assert jg3.rodadas.tamanho == 4
    assert jg3.rodadas.indices == [0, 1, 2, 3]
    assert jg3.rodadas.turno == 1
    assert jg3.rodadas.rodadas == 0
