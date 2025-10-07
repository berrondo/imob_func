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

BONUS = 100
MAXIMO = 1000


class Jogo(PClass):
    tabuleiro = field(type=tabuleiro.Tabuleiro, mandatory=True)
    rodadas = field(type=(rodada.Rodada,), mandatory=True)
    j = field()
    p = field()
    banco_ = field(type=(banco.Banco,), mandatory=False)
    registro = field(type=(cartorio.Cartorio,))
    # reg = field(type=JRegistro)
    contador = field(type=int, initial=0)


def criar_jogo(propriedades, jogadores):
    return Jogo(
        tabuleiro=tabuleiro.criar_tabuleiro(propriedades, jogadores),
        rodadas=rodada.criar_rodada(len(jogadores)),
        banco_=banco.criar_banco(len(jogadores), jogadores[0].saldo),
        registro=cartorio.criar_cartorio(),
        # reg=JRegistro(
        #     cartorio=cartorio.criar_cartorio(),
        #     banco=banco.criar_banco(len(jogadores), jogadores[0].saldo),
        # ),
    )


def jogar(self, maximo=1000, contador=None):
    self = self.set('contador', self.contador + 1 if contador is None else contador + 1)
    if self.contador > maximo:
        return self

    self = identificar_jogadores(self)

    self = proxima_rodada(self)
    self, jogador_eliminado = jogador_do_turno(self, self.rodadas.turno)
    if jogador_eliminado:
        # self = self.set(
        #     'tabuleiro', tabuleiro.desapropriar_propriedade(self.tabuleiro, self.j.i)
        # )
        return jogar(self, maximo, self.contador)    # pula o jogador (sem saldo)

    self = mover_jogador(self, self.rodadas.turno)
    self = propriedade_na_posicao(self, self.rodadas.turno)

    n = negocio.comprar_ou_alugar(
        self.j, self.p, self.registro, self.banco_, self.tabuleiro.jogadores
    )

    self = atualizar_tabuleiro(self, n.j, n.p)

    if banco.saldo_de(self.banco_, self.j.i) <= 0:   # jif n.j.saldo <= 0:
        self = self.set('rodadas', rodada.remover(self.rodadas, self.rodadas.turno))

    self = atualizar_registros(self, n.registro, n.banco_)
    self = relatorio.registrar(self, n.tipo)
    if banco.resta_um(self.banco_):  # if rodada.jogando(self.rodadas) == 1:
        return self

    return jogar(self, maximo, self.contador)


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
    eliminado = self.j.saldo <= 0
    return self, eliminado


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


def atualizar_registros(self, registro, b):
    return self.set('registro', registro).set('banco_', b)
