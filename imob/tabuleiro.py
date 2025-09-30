from pyrsistent import m, v

from imob import jogador

BONUS = 100


def criar_tabuleiro(propriedades, jogadores):
    return m(
        propriedades=v(*propriedades),
        jogadores=m(**{j.nome: j for j in jogadores}),
        posicoes=m(**{j.nome: -1 for j in jogadores}),
    )


def extensao(self):
    return len(self.propriedades)


def posicao_do_jogador(self, j):
    return self.posicoes[j.nome]


def mover_jogador(self, j, passos):
    posicao = posicao_do_jogador(self, j)
    nova_volta, nova_posicao = divmod(posicao + passos, extensao(self))
    if nova_volta:  # bonifica
        j2 = jogador.creditar(self.jogadores[j.nome], BONUS)
        js = self.jogadores.set(j.nome, j2)
        self = self.set('jogadores', js)
    return self.set('posicoes', self.posicoes.set(j.nome, nova_posicao))
