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

SALDO_INICIAL = 300
BONUS = 1
MAXIMO = 1000


class Jogo(PClass):
    tabuleiro = field(type=tabuleiro.Tabuleiro, mandatory=True)
    rodadas = field(type=(rodada.Rodada,), mandatory=True)
    j = field()
    p = field()
    banco_ = field(type=(banco.Banco,), mandatory=False)
    registro = field(type=(cartorio.Cartorio,))


def criar_jogo(propriedades, jogadores, saldo_inicial=SALDO_INICIAL):
    return identificar_jogadores(
        Jogo(
            tabuleiro=tabuleiro.criar_tabuleiro(propriedades, jogadores),
            rodadas=rodada.criar_rodada(len(jogadores)),
            banco_=banco.criar_banco(len(jogadores), saldo_inicial),
            registro=cartorio.criar_cartorio(),
        )
    )


def jogar(g, maximo=1000):
    if rodada.resta_um(g.rodadas):
        return g

    g, turno = proxima_rodada(g)
    if g.rodadas.contador > maximo:
        return g

    g = jogador_do_turno(g, turno)
    g, volta = mover_jogador(g, turno, BONUS)
    if volta:
        g = creditar_bonus_ao_jogador(g)

    g = propriedade_na_posicao(g, turno)
    n, eliminado = negocio.comprar_ou_alugar(g.j, g.p, g.registro, g.banco_)
    if eliminado:
        g = remover_jogador_da_rodada(g)

    g = atualizar_registros(g, n.registro, n.banco_)
    g = relatorio.registrar(g, n.tipo)

    return jogar(g, maximo)


def dado():
    return random.randint(1, 7)


def identificar_jogadores(g):
    jogadores = [j.set('i', i) for i, j in enumerate(g.tabuleiro.jogadores)]
    return g.set('tabuleiro', g.tabuleiro.set('jogadores', jogadores))


def proxima_rodada(g):
    g = g.set('rodadas', rodada.proximo(g.rodadas))
    return g, g.rodadas.turno


def jogador_do_turno(g, turno):
    j = g.tabuleiro.jogadores[turno]
    assert j.i == turno
    g = g.set('j', j)
    eliminado = banco.saldo_de(g.banco_, g.j.i) <= 0
    if eliminado:
        g = relatorio.registrar(g, '')
    return g


def propriedade_na_posicao(g, turno):
    p = tabuleiro.casa(g.tabuleiro, turno)
    pi = tabuleiro.posicao_do_jogador(g.tabuleiro, turno)
    return g.set('p', p.set('i', pi))


def mover_jogador(g, turno, bonus):
    t, volta = tabuleiro.mover_jogador_com_bonus(g.tabuleiro, turno, dado(), bonus)
    return g.set('tabuleiro', t), volta


def creditar_bonus_ao_jogador(g):
    return g.set('banco_', banco.creditar_em(g.banco_, g.j.i, BONUS))


def remover_jogador_da_rodada(g):
    return g.set('rodadas', rodada.remover(g.rodadas, g.rodadas.turno))


def atualizar_registros(g, registro, banco_):
    return g.set('registro', registro).set('banco_', banco_)
