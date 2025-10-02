from imob import jogador, jogo
from imob.estrategia import estrategias
from imob.jogador import criar_jogador
from imob.propriedade import criar_propriedade

jogadores = [j for j in [criar_jogador(e, 300) for e in estrategias]]

propriedades = [criar_propriedade(preco=100, aluguel=10)] * 20


def rodada(js, maximo=None, contador=0):
    if len(js) == 1:
        return js
    if maximo:
        if maximo == contador:
            return js
        else:
            contador+=1

    da_vez = js[0]

    js2 = js.remove(da_vez)
    j1 = jogador.debitar(da_vez, 100)   # joga

    if j1.saldo < 0:    # perdeu!
        return rodada(js2, maximo, contador)
    else:               # no
        js3 = js2.set(-1, j1)
        return rodada(js3, maximo, contador)


def test_rodada():
    from pyrsistent import v
    js = v(*jogadores)

    assert len(js) == 4
    js2 = rodada(js)
    assert len(js2) == 1


def test_criar_jogo():
    jg = jogo.criar_jogo(propriedades, jogadores)

    assert jg.tabuleiro

    # jogo.jogar(jg)




    from itertools import cycle
    for j in cycle(self.jogadores):
        print(j)

        if j not in self.tabuleiro.jogadores:
            continue

        jogada(self, j, dado())
        vez += 1

        if len(self.tabuleiro.jogadores) == 1:
            break

        if vez >= 10:
            print(j)
            break
