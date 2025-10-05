import random

from pyrsistent import PClass, field

from imob import (
    banco,
    cartorio,
    jogador,
    negocio,
    propriedade,
    relatorio,
    rodada,
    tabuleiro,
)

BONUS = 100
MAXIMO = 1000


class Jogo(PClass):
    tabuleiro = field(type=tabuleiro.Tabuleiro, mandatory=True)
    rodadas = field(type=(rodada.Rodada,), mandatory=True)
    banco_ = field(type=(banco.Banco,), mandatory=False)
    registro = field(type=(cartorio.Cartorio,))
    j = field(type=(jogador.Jogador, type(None)), initial=None)
    p = field(type=(propriedade.Propriedade, type(None)), initial=None)
    ji = field(type=(int, type(None)), initial=None)
    pi = field(type=(int, type(None)), initial=None)
    contador = field(type=int, initial=0)


def criar_jogo(propriedades, jogadores):
    for p in propriedades: print(p)
    print([j.nome for j in jogadores])
    return Jogo(
        tabuleiro=tabuleiro.criar_tabuleiro(propriedades, jogadores),
        rodadas=rodada.criar_rodada(len(jogadores)),
        banco_=banco.criar_banco(len(jogadores), jogadores[0].saldo),
        registro=cartorio.criar_cartorio(),
    )


def jogar(self, maximo=1000, contador=None):
    self = self.set('contador', self.contador + 1 if contador is None else contador + 1)
    if self.contador > maximo:
        print("\nJogo finalizado por limite de rodadas")
        print(relatorio.relatorio_atual.gerar_relatorio())
        return self

    self = proxima_rodada(self)
    self, jogador_eliminado = jogador_do_turno(self, self.rodadas.turno)
    if jogador_eliminado:
        self = self.set('tabuleiro', tabuleiro.desapropriar_propriedade(self.tabuleiro, self.ji))
        return jogar(self, maximo, self.contador)    # pula o jogador eliminado (sem saldo)

    self = mover_jogador(self, self.rodadas.turno)
    self = propriedade_na_posicao(self, self.rodadas.turno)

    n = negocio.comprar_ou_alugar(self.j, self.p, self.ji, self.pi, self.registro, self.banco_, self.tabuleiro.jogadores)
    self = self.set('registro', n.registro)
    self = self.set('banco_', n.banco_)

    self = atualizar_tabuleiro(self, n.j, n.p)
    self = relatorio.registrar(self)

    if banco.saldo_de(self.banco_, self.ji) <= 0:   # jif n.j.saldo <= 0:
        self = self.set('rodadas', rodada.remover(self.rodadas, self.rodadas.turno))

    if banco.resta_um(self.banco_):# if rodada.jogando(self.rodadas) == 1:
        print("\nJogo finalizado - Temos um vencedor!")
        print(relatorio.relatorio_atual.gerar_relatorio())
        return self

    return jogar(self, maximo, self.contador)


def dado():
    return random.randint(1, 7)


def proxima_rodada(self):
    return self.set('rodadas', rodada.proximo(self.rodadas))


def jogador_do_turno(self, turno):
    self = self.set('j', self.tabuleiro.jogadores[turno])
    self = self.set('ji', turno)
    eliminado = self.j.saldo <= 0
    return self, eliminado


def propriedade_na_posicao(self, turno):
    return self \
        .set('p', tabuleiro.casa(self.tabuleiro, turno)) \
        .set('pi', tabuleiro.posicao_do_jogador(self.tabuleiro, turno))


def mover_jogador(self, turno):
    return self.set('tabuleiro', tabuleiro.mover_jogador_com_bonus(
            self.tabuleiro, turno, dado(), BONUS
        )
    )


def atualizar_tabuleiro(self, j, p):
    self = atualizar_jogador_no_tabuleiro(self, self.rodadas.turno, j)
    return atualizar_propriedade_no_tabuleiro(self, self.pi, p)


def atualizar_jogador_no_tabuleiro(self, ji, j):
    return self.set('tabuleiro', tabuleiro.atualizar_jogador(self.tabuleiro, ji, j))


def atualizar_propriedade_no_tabuleiro(self, pi, p):
    return self.set('tabuleiro', tabuleiro.atualizar_propriedade(self.tabuleiro, pi, p))
