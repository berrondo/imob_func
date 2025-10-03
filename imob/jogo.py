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


def jogar(self, maximo, contador=0):
    contador += 1
    if contador > maximo: #959:
        return self

    self = set_rodada(self)

    self = set_jogador(self, self.rodadas.da_vez)
    if self.j.saldo <= 0:   # pula o jogador que perdeu (sem saldo)
        return jogar(self, maximo, contador)

    self = mover_jogador(self, self.rodadas.da_vez)
    self = set_propriedade(self, self.rodadas.da_vez)

    j2, p2 = negocio.comprar_ou_alugar(self.j, self.p)
    print(contador, self.rodadas.da_vez, j2.nome, j2.saldo, p2.proprietario and p2.proprietario.nome)

    pi = tabuleiro.posicao_do_jogador(self.tabuleiro, self.rodadas.da_vez)
    self = atualizar_tabuleiro(self, self.rodadas.da_vez, j2, pi, p2)

    if j2.saldo <= 0:   # jogador perdeu
        print(j2.nome, 'perdeu')
        self = self.set('rodadas', rodada.remover(self.rodadas, self.rodadas.da_vez))

    if rodada.jogando(self.rodadas) == 1:   # sobrou o vencedor!
        for p in self.tabuleiro.propriedades:
            if p.proprietario:
                print(p.proprietario.nome, p.proprietario.saldo)
            else:
                print(p.proprietario)
        return self

    return jogar(self, maximo, contador)


def dado():
    return random.randint(1, 7)


def set_rodada(self):
    return self.set('rodadas', rodada.proximo(self.rodadas))


def set_jogador(self, da_vez):
    return self.set('j', self.tabuleiro.jogadores[da_vez])


def set_propriedade(self, da_vez):
    return self.set('p', tabuleiro.casa(self.tabuleiro, da_vez))


def mover_jogador(self, da_vez):
    return self.set(
        'tabuleiro', tabuleiro.mover_jogador_com_bonus(
            self.tabuleiro, da_vez, dado(), BONUS
        )
    )


def atualizar_tabuleiro(self, ji, j, pi, p):
    self = atualizar_jogador_no_tabuleiro(self, ji, j)
    return atualizar_propriedade_no_tabuleiro(self, pi, p)


def atualizar_jogador_no_tabuleiro(self, ji, j):
    return self.set('tabuleiro', tabuleiro.atualizar_jogador(self.tabuleiro, ji, j))


def atualizar_propriedade_no_tabuleiro(self, pi, p):
    return self.set('tabuleiro', tabuleiro.atualizar_propriedade(self.tabuleiro, pi, p))
