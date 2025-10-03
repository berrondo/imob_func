from pyrsistent import PRecord, field, v

from imob import jogador


class Tabuleiro(PRecord):
    propriedades = field()
    jogadores = field()
    # proprietarios = field()   # ?
    posicoes = field()


def criar_tabuleiro(propriedades, jogadores):
    return Tabuleiro(
        propriedades=v(*propriedades),
        jogadores=v(*jogadores),
        # proprietarios=v(*(v() for _ in jogadores)),   # ?
        posicoes=v(*(-1 for _ in jogadores)),
    )


def extensao(self):
    return len(self.propriedades)


def posicao_do_jogador(self, ji):
    return self.posicoes[ji]


def casa(self, ji):
    return self.propriedades[posicao_do_jogador(self, ji)]


def mover_jogador_com_bonus(self, ji, passos, bonus):
    nova_volta, self = mover_jogador(self, ji, passos)
    if nova_volta:
        self = _bonificar_jogador(self, ji, bonus)
    return self


def mover_jogador(self, ji, passos):
    posicao = posicao_do_jogador(self, ji)
    nova_volta, nova_posicao = divmod(posicao + passos, extensao(self))
    return nova_volta, self.set('posicoes', self.posicoes.set(ji, nova_posicao))


def _bonificar_jogador(self, ji, bonus):
    return atualizar_jogador(self, ji, jogador.creditar(self.jogadores[ji], bonus))


def atualizar_jogador(self, ji, j):
    return self.set('jogadores', self.jogadores.set(ji, j))


def atualizar_propriedade(self, pi, p):
    return self.set('propriedades', self.propriedades.set(pi, p))
