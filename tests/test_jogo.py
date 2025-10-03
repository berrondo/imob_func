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


















    # from itertools import cycle
    # for j in cycle(self.jogadores):
    #     print(j)

    #     if j not in self.tabuleiro.jogadores:
    #         continue

    #     jogada(self, j, dado())
    #     vez += 1

    #     if len(self.tabuleiro.jogadores) == 1:
    #         break

    #     if vez >= 10:
    #         print(j)
    #         break



# def rodada(js, maximo=None, contador=0):
#     if len(js) == 1:
#         return js
#     if maximo:
#         if maximo == contador:
#             return js
#         else:
#             contador+=1

#     turno = js[0]

#     js2 = js.remove(turno)
#     j1 = jogador.debitar(turno, 100)   # joga

#     if j1.saldo < 0:    # perdeu!
#         return rodada(js2, maximo, contador)
#     else:               # no
#         js3 = js2.set(-1, j1)
#         return rodada(js3, maximo, contador)


# def test_rodada(jogadores):
#     from pyrsistent import v
#     js = v(*jogadores)

#     assert len(js) == 4
#     js2 = rodada(js)
#     assert len(js2) == 1