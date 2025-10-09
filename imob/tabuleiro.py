from pyrsistent import PClass, field, pvector_field, v

from imob import jogador, propriedade


class Tabuleiro(PClass):
    propriedades = field(propriedade.Propriedades, mandatory=True)
    jogadores = field(jogador.Jogadores, mandatory=True)
    posicoes = pvector_field(int)


def criar_tabuleiro(propriedades, jogadores):
    return Tabuleiro(
        propriedades=v(*propriedades),
        jogadores=v(*jogadores),
        posicoes=v(*(-1 for _ in jogadores)),
    )


def extensao(self):
    return len(self.propriedades)


def posicao_do_jogador(self, ji):
    return self.posicoes[ji]


def casa(self, ji):
    return self.propriedades[posicao_do_jogador(self, ji)]


def mover_jogador_com_bonus(self, ji, passos, bonus):
    self, nova_volta = mover_jogador(self, ji, passos)
    return self, nova_volta


def mover_jogador(self, ji, passos):
    posicao = posicao_do_jogador(self, ji)
    nova_volta, nova_posicao = divmod(posicao + passos, extensao(self))
    return self.set('posicoes', self.posicoes.set(ji, nova_posicao)), nova_volta
