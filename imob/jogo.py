import random

from pyrsistent import m

from imob import negocio
from imob import rodada as rodada
from imob import tabuleiro as tabuleiro

BONUS = 100
MAXIMO = 1000


def criar_jogo(propriedades, jogadores):
    return m(
        tabuleiro=tabuleiro.criar_tabuleiro(propriedades, jogadores),
        rodadas=rodada.criar_rodada(len(jogadores)),
        j=None,
        p=None,
    )


def dado():
    return random.randint(1, 7)


def set_rodada(self):
    return self.set('rodada', rodada.proximo(self.rodadas))


def set_jogador(self, rodada):
    return self.set('j', self.tabuleiro.jogadores[rodada.da_vez])


def set_propriedade(self, j):
    return self.set('p', tabuleiro.casa(self.tabuleiro, j))


def mover_jogador(self, j):
    return self.set(
        'tabuleiro', self.tabuleiro.mover_jogador_com_bonus(
            self.tabuleiro, j, dado(), BONUS
            )
    )


def atualizar_tabuleiro(self, j, p):
    self = atualizar_jogador_no_tabuleiro(self, j)
    return atualizar_propriedade_no_tabuleiro(self, p)


def atualizar_jogador_no_tabuleiro(self, j):
    return self.set('tabuleiro', tabuleiro.atualizar_jogador(self.tabuleiro, j))


def atualizar_propriedade_no_tabuleiro(self, p):
    return self.set('tabuleiro', tabuleiro.atualizar_propriedade(self.tabuleiro, p))


def jogar(self, contador=0, maximo=MAXIMO):
    if contador > maximo:
        return self

    self = set_rodada(self)

    self = set_jogador(self, self.rodada)
    self = mover_jogador(self, self.j)
    self = set_propriedade(self, self.j)

    j2, p2 = negocio.comprar_ou_alugar(self.j, self.p)

    self = atualizar_tabuleiro(j2, p2)

    if j2.saldo < 0:
        self.rodada.remove(self.rodada.da_vez)
        if self.rodada.fim:
            return self

    contador += 1
    return jogar(self, contador)
