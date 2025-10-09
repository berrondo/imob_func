from pyrsistent import PClass, field, pvector_field, v

from imob_o import jogador, propriedade


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


def desapropriar_propriedade(self, ji):
    for pi, p in enumerate(self.propriedades):
        if p.proprietario and p.proprietario == self.jogadores[ji]:
            p = propriedade.desapropriar(p)
            self = atualizar_propriedade(self, pi, p)
    return self