import random

from pyrsistent import PClass, field

from imob_o import (
    cartorio,
    negocio,
    relatorio,
    rodada,
    tabuleiro,
)

BONUS = 100
MAXIMO = 1000


class Jogo(PClass):
    tabuleiro = field(type=tabuleiro.Tabuleiro, mandatory=True)
    rodadas = field(type=(rodada.Rodada,), mandatory=True)
    j = field()
    p = field()
    registro = field(type=(cartorio.Cartorio,))


def criar_jogo(propriedades, jogadores):
    jg = Jogo(
        tabuleiro=tabuleiro.criar_tabuleiro(propriedades, jogadores),
        rodadas=rodada.criar_rodada(len(jogadores)),
        registro=cartorio.criar_cartorio(),
    )
    jg = identificar_jogadores(jg)
    return jg


def jogar(self, maximo=1000):
    self, turno = proxima_rodada(self)
    if self.rodadas.contador > maximo:
        return self

    self = jogador_do_turno(self, self.rodadas.turno)
    self = mover_jogador(self, self.rodadas.turno)
    self = propriedade_na_posicao(self, self.rodadas.turno)
    n = negocio.comprar_ou_alugar(self.j, self.p, self.registro, self.tabuleiro.jogadores)

    self = atualizar_tabuleiro(self, n.j, n.p)

    self = atualizar_registros(self, n.registro)

    if n.j.saldo <= 0:
        self = self.set('rodadas', rodada.remover(self.rodadas, self.rodadas.turno))

    self = relatorio.registrar(self, n.tipo)
    if rodada.resta_um(self.rodadas):
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
    self = self.set('rodadas', rodada.proximo(self.rodadas))
    return self, self.rodadas.turno


def jogador_do_turno(self, turno):
    j = self.tabuleiro.jogadores[turno]
    assert j.i == turno
    self = self.set('j', j)  # .set('i', turno))
    eliminado = self.j.saldo <= 0
    if eliminado:
        self = relatorio.registrar(self, '')
    return self


def propriedade_na_posicao(self, turno):
    p = tabuleiro.casa(self.tabuleiro, turno)
    pi = tabuleiro.posicao_do_jogador(self.tabuleiro, turno)
    return self.set('p', p.set('i', pi))


def mover_jogador(self, turno):
    return self.set('tabuleiro', tabuleiro.mover_jogador_com_bonus(
            self.tabuleiro, turno, dado(), BONUS
        )
    )


def atualizar_tabuleiro(self, j, p):
    self = atualizar_jogador_no_tabuleiro(self, j)
    return atualizar_propriedade_no_tabuleiro(self, p)


def atualizar_jogador_no_tabuleiro(self, j):
    return self.set('tabuleiro', tabuleiro.atualizar_jogador(self.tabuleiro, j.i, j))


def atualizar_propriedade_no_tabuleiro(self, p):
    self = self.set('tabuleiro', tabuleiro.atualizar_propriedade(self.tabuleiro, p.i, p))
    if p.proprietario:
        self = atualizar_jogador_no_tabuleiro(self, p.proprietario)
    return self


def atualizar_registros(self, registro):
    return self.set('registro', registro)
