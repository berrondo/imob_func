from imob.estrategia import estrategias, impulsivo
from imob.jogador import criar_jogador
from imob.propriedade import criar_propriedade
from imob.tabuleiro import criar_tabuleiro, mover_jogador, posicao_do_jogador

jogadores = [j for j in [criar_jogador(e, 300) for e in estrategias]]

propriedades = [criar_propriedade(preco=0, aluguel=0)] * 20


def test_criar_tabuleiro():
    t = criar_tabuleiro(propriedades, jogadores)

    assert len(t.propriedades) == 20
    assert len(t.jogadores) == 4
    assert len(t.posicoes) == 4


def test_move_jogador_um_passo():
    j1 = criar_jogador(impulsivo, 300)
    t1 = criar_tabuleiro(propriedades=[], jogadores=[j1])

    assert posicao_do_jogador(t1, j1) == -1

    t2 = mover_jogador(t1, j1, 1)

    assert posicao_do_jogador(t2, j1) == 0
