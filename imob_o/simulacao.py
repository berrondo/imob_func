import random

from imob_o import relatorio
from imob_o.estrategia import estrategias
from imob_o.jogador import criar_jogador
from imob_o.jogo import criar_jogo, jogar
from imob_o.propriedade import criar_propriedade


def gerar_propriedades(how_many=20, median=5, stdv=1, price_scale=5, rent_scale=1):
    distribution = (round(random.gauss(median, stdv)) for _ in range(how_many))
    params = ((value * price_scale, value * rent_scale) for value in distribution)
    return [criar_propriedade(preco=price, aluguel=rent) for price, rent in params]


propriedades = [criar_propriedade(preco=50, aluguel=5)] * 20
# random.shuffle(estrategias)
jogadores = [criar_jogador(e, 300) for e in estrategias]

# jg = criar_jogo(gerar_propriedades(), jogadores)
jg = criar_jogo(propriedades, jogadores)

jg = jogar(jg, maximo=300)

print(relatorio.relatorio_atual.gerar_relatorio())
