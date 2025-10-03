from imob.estrategia import estrategias
from imob.jogador import criar_jogador
from imob.tabuleiro import (
    criar_tabuleiro,
    extensao,
    mover_jogador_com_bonus,
    posicao_do_jogador,
)

BONUS = 100


def test_criar_tabuleiro(propriedades, jogadores):
    t = criar_tabuleiro(propriedades, jogadores)

    assert extensao(t) == 20
    assert len(t.propriedades) == 20
    assert len(t.jogadores) == 4
    assert len(t.posicoes) == 4


def test_posicoes():
    t = criar_tabuleiro(['p'], ['j1', 'j2'])

    assert t.posicoes == [-1, -1]
    assert posicao_do_jogador(t, 0) == -1
    assert posicao_do_jogador(t, 1) == -1


def test_move_jogador_um_passo(propriedades):
    j1 = criar_jogador(estrategias[0], 300)
    t1 = criar_tabuleiro(propriedades=propriedades, jogadores=[j1])

    assert posicao_do_jogador(t1, 0) == -1

    t2 = mover_jogador_com_bonus(t1, 0, 1, BONUS)

    assert posicao_do_jogador(t2, 0) == 0


def test_jogador_volta_ao_inicio_do_tabuleiro_e_recebe_bonus(propriedades):
    j1 = criar_jogador(estrategias[0], 300)
    t1 = criar_tabuleiro(propriedades=propriedades, jogadores=[j1])

    assert extensao(t1) == 20
    assert posicao_do_jogador(t1, 0) == -1

    t2 = mover_jogador_com_bonus(t1, 0, 25, BONUS)

    assert posicao_do_jogador(t2, 0) == 4
    assert t2.jogadores[0].saldo == 400
