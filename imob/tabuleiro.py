from pyrsistent import m, v

from imob import jogador


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


def casa(self, j):
    return self.propriedades[posicao_do_jogador(j)]


def mover_jogador_com_bonus(self, j, passos, bonus):
    nova_volta, self = mover_jogador(self, j, passos)
    if nova_volta:
        self = _bonificar_jogador(self, j, bonus)
    return self


def mover_jogador(self, j, passos):
    posicao = posicao_do_jogador(self, j)
    nova_volta, nova_posicao = divmod(posicao + passos, extensao(self))
    return nova_volta, self.set('posicoes', self.posicoes.set(j.nome, nova_posicao))


def _bonificar_jogador(self, j, bonus):
    return atualizar_jogador(self, jogador.creditar(self.jogadores[j.nome], bonus))


def atualizar_jogador(self, j):
    return self.set('jogadores', self.jogadores.set(j.nome, j))


def atualizar_propriedade(self, p):
    return self.set('propriedades', self.propriedades.set(idx, p))
