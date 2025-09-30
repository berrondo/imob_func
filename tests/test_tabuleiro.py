from imob.estrategia import estrategias
from imob.jogador import criar_jogador
from imob.propriedade import criar_propriedade
from imob.tabuleiro import criar_tabuleiro, extensao, mover_jogador, posicao_do_jogador

jogadores = [j for j in [criar_jogador(e, 300) for e in estrategias]]

propriedades = [criar_propriedade(preco=100, aluguel=10)] * 20


def test_criar_tabuleiro():
    t = criar_tabuleiro(propriedades, jogadores)

    assert extensao(t) == 20
    assert len(t.propriedades) == 20
    assert len(t.jogadores) == 4
    assert len(t.posicoes) == 4


def test_move_jogador_um_passo():
    j1 = criar_jogador(estrategias[0], 300)
    t1 = criar_tabuleiro(propriedades=propriedades, jogadores=[j1])

    assert posicao_do_jogador(t1, j1) == -1

    t2 = mover_jogador(t1, j1, 1)

    assert posicao_do_jogador(t2, j1) == 0


def test_jogador_volta_ao_inicio_do_tabuleiro_e_recebe_bonus():
    j1 = criar_jogador(estrategias[0], 300)
    t1 = criar_tabuleiro(propriedades=propriedades, jogadores=[j1])

    assert extensao(t1) == 20
    assert posicao_do_jogador(t1, j1) == -1

    t2 = mover_jogador(t1, j1, 25)

    assert posicao_do_jogador(t2, j1) == 4
    assert t2.jogadores[j1.nome].saldo == 400
