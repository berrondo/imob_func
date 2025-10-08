import random

from pyrsistent import PClass, field

from imob import (
    banco,
    cartorio,
    negocio,
    relatorio,
    rodada,
    tabuleiro,
)

BONUS = 1
MAXIMO = 1000


class Jogo(PClass):
    tabuleiro = field(type=tabuleiro.Tabuleiro, mandatory=True)
    rodadas = field(type=(rodada.Rodada,), mandatory=True)
    j = field()
    p = field()
    banco_ = field(type=(banco.Banco,), mandatory=False)
    registro = field(type=(cartorio.Cartorio,))


def criar_jogo(propriedades, jogadores, saldo_inicial=300):
    jg = Jogo(
        tabuleiro=tabuleiro.criar_tabuleiro(propriedades, jogadores),
        rodadas=rodada.criar_rodada(len(jogadores)),
        banco_=banco.criar_banco(len(jogadores), saldo_inicial),
        registro=cartorio.criar_cartorio(),
    )
    jg = identificar_jogadores(jg)
    return jg


def jogar(self, maximo=1000):
    #
    self = proxima_rodada(self)
    if self.rodadas.contador > maximo:
        return self

    self, jogador_eliminado = jogador_do_turno(self, self.rodadas.turno)
    if jogador_eliminado:
        self = relatorio.registrar(self, '')
        return jogar(self, maximo)    # pula o jogador (sem saldo)

    #
    self = mover_jogador_com_bonus(self, self.rodadas.turno, BONUS)
    self = propriedade_na_posicao(self, self.rodadas.turno)
    n = negocio.comprar_ou_alugar(self.j, self.p, self.registro, self.banco_)
    self = atualizar_registros(self, n.registro, n.banco_)
    if banco.saldo_de(self.banco_, self.j.i) <= 0:
        self = self.set('rodadas', rodada.remover(self.rodadas, self.rodadas.turno))
    self = relatorio.registrar(self, n.tipo)

    #
    if rodada.jogando(self.rodadas) == 1:  # if len(self.rodadas.removidos) == 3:
        return self
    return jogar(self, maximo)


def dado():
    return random.randint(1, 7)


def identificar_jogadores(self):
    jogadores = []
    for i, j in enumerate(self.tabuleiro.jogadores):
        jogadores.append(j.set('i', i))
    return self.set('tabuleiro', self.tabuleiro.set('jogadores', jogadores))


def proxima_rodada(self):
    return self.set('rodadas', rodada.proximo(self.rodadas))


def jogador_do_turno(self, turno):
    j = self.tabuleiro.jogadores[turno]
    assert j.i == turno
    self = self.set('j', j)  # .set('i', turno))
    eliminado = banco.saldo_de(self.banco_, self.j.i) <= 0
    return self, eliminado


def propriedade_na_posicao(self, turno):
    p = tabuleiro.casa(self.tabuleiro, turno)
    pi = tabuleiro.posicao_do_jogador(self.tabuleiro, turno)
    return self.set('p', p.set('i', pi))


def mover_jogador_com_bonus(self, turno, bonus):
    t, nova_volta = tabuleiro.mover_jogador_com_bonus(
        self.tabuleiro, turno, dado(), bonus
    )
    if nova_volta:
        self = self.set('banco_', banco.creditar_em(self.banco_, self.j.i, BONUS))
    return self.set('tabuleiro', t)


def atualizar_registros(self, registro, b):
    return self.set('registro', registro).set('banco_', b)
