from pyrsistent import m, v


def criar_tabuleiro(propriedades, jogadores):
    return m(
        propriedades=v(*propriedades),
        jogadores=m(**{j.nome: j for j in jogadores}),
        posicoes=m(**{j.nome: -1 for j in jogadores}),
    )


def posicao_do_jogador(self, j):
    return self.posicoes[j.nome]


def mover_jogador(self, j, passos):
    nova_posicao = posicao_do_jogador(self, j) + passos
    return self.set('posicoes', self.posicoes.set(j.nome, nova_posicao))
