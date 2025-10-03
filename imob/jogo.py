import random

from pyrsistent import PRecord, field

from imob import negocio, rodada, tabuleiro

BONUS = 100
MAXIMO = 1000


class Jogo(PRecord):
    tabuleiro = field()
    rodadas = field()
    j = field()
    p = field()


def criar_jogo(propriedades, jogadores):
    for p in propriedades: print(p)
    return Jogo(
        tabuleiro=tabuleiro.criar_tabuleiro(propriedades, jogadores),
        rodadas=rodada.criar_rodada(len(jogadores)),
        j=None,
        p=None,
    )


def jogar(self, maximo=1000, contador=0):
    contador += 1
    if contador > maximo: # 959:
        return self

    self = proxima_rodada(self); print("  '-> prox", list(self.rodadas.removidos), self.rodadas.rodadas, self.rodadas.turno)
    self, jogador_eliminado = jogador_do_turno(self, self.rodadas.turno)
    if jogador_eliminado:
        return jogar(self, maximo, contador)    # pula o jogador eliminado (sem saldo)

    self = mover_jogador(self, self.rodadas.turno)
    self = propriedade_na_posicao(self, self.rodadas.turno)
    j2, p2 = negocio.comprar_ou_alugar(self.j, self.p); print(contador, self.rodadas.turno, j2.nome, j2.saldo, p2.proprietario and p2.proprietario.nome)
    self = atualizar_tabuleiro(self, j2, p2)

    if j2.saldo <= 0:   # jogador perdeu
        print(j2.nome, 'perdeu')
        self = self.set('rodadas', rodada.remover(self.rodadas, self.rodadas.turno))

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


def proxima_rodada(self):
    return self.set('rodadas', rodada.proximo(self.rodadas))


def jogador_do_turno(self, turno):
    self = self.set('j', self.tabuleiro.jogadores[turno])
    eliminado = self.j.saldo <= 0
    return self, eliminado


def propriedade_na_posicao(self, turno):
    return self.set('p', tabuleiro.casa(self.tabuleiro, turno))


def mover_jogador(self, turno):
    return self.set('tabuleiro', tabuleiro.mover_jogador_com_bonus(
            self.tabuleiro, turno, dado(), BONUS
        )
    )


def atualizar_tabuleiro(self, j, p):
    self = atualizar_jogador_no_tabuleiro(self, self.rodadas.turno, j)
    pi = tabuleiro.posicao_do_jogador(self.tabuleiro, self.rodadas.turno)
    return atualizar_propriedade_no_tabuleiro(self, pi, p)


def atualizar_jogador_no_tabuleiro(self, ji, j):
    return self.set('tabuleiro', tabuleiro.atualizar_jogador(self.tabuleiro, ji, j))


def atualizar_propriedade_no_tabuleiro(self, pi, p):
    return self.set('tabuleiro', tabuleiro.atualizar_propriedade(self.tabuleiro, pi, p))
