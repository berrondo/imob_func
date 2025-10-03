import random

from imob.estrategia import estrategias
from imob.jogador import criar_jogador
from imob.jogo import criar_jogo, jogar
from imob.propriedade import criar_propriedade


def gerar_propriedades(how_many=20, median=5, stdv=1, price_scale=10, rent_scale=1):
    distribution = (round(random.gauss(median, stdv)) for _ in range(how_many))
    params = ((value * price_scale, value * rent_scale) for value in distribution)
    return [criar_propriedade(preco=price, aluguel=rent) for price, rent in params]


# propriedades = [criar_propriedade(preco=50, aluguel=5)] * 20
random.shuffle(estrategias)
jogadores = [criar_jogador(e, 420) for e in estrategias]

jg = criar_jogo(gerar_propriedades(), jogadores)

jg = jogar(jg, maximo=500)
