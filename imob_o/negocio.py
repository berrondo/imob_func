from pyrsistent import PClass, field

from imob_o import cartorio, jogador, propriedade


class Negocio(PClass):
    tipo = field(type=str, initial='')  # 'compra' ou 'aluguel'
    j = field(jogador.Jogador)
    p = field(propriedade.Propriedade)
    registro = field(type=cartorio.Cartorio)
    js = field()


def criar_negocio(j, p, registro=None, b=None, js=[]):
    return Negocio(
        j=j,
        p=p,
        registro=registro,
        js=js,
    )


def comprar_ou_alugar(j, p, registro=None, b=None, js=[]):
    n = criar_negocio(j, p, registro, b, js)
    match cartorio.obter_proprietario(n.registro, p.i):
        case None:
            return tentar_comprar(n)
        case i_proprietario:   # index do jogador proprietario
            # assert p.proprietario and p.proprietario.i == i_proprietario, \
            #        (i_proprietario, p.proprietario)
            return alugar(n, i_proprietario)


def alugar(self, i_proprietario):
    self = debitar_de_jogador(self, self.p.aluguel)

    if self.j.saldo >= 0:
        if self.p.proprietario.saldo > 0:
            self = creditar_para_proprietario(self, self.p.proprietario, self.p.aluguel)
            self = self.set('tipo', 'ALUGUEL')

    if self.j.saldo <= 0:
        self = despejar_jogador_de_suas_propriedades(self)

    return self


def tentar_comprar(self):
    if jogador.tem_saldo_suficiente(self.j, self.p.preco) and estrategia_eh_comprar(self.j, self.p):
        return comprar(self)
    return self


def estrategia_eh_comprar(j, p):
    return j.estrategia(j, p)


def comprar(self):
    self = self.set('tipo', 'COMPRA')
    self = debitar_de_jogador(self, self.p.preco)
    self = atualizar_proprietario(self, self.j)

    if self.j.saldo <= 0:
        self = despejar_jogador_de_suas_propriedades(self)

    return self


def debitar_de_jogador(self, valor):
    j2 = jogador.debitar(self.j, valor)
    self = self.set('j', j2)
    return self


def creditar_para_proprietario(self, jp, valor):
    if self.p.proprietario:
        assert self.p.proprietario.i == jp.i, (jp.i, self.p.proprietario.i)
        jp2 = jogador.creditar(self.p.proprietario, valor)
        self = atualizar_proprietario(self, jp2)
    return self


def atualizar_proprietario(self, jp):
    p2 = propriedade.apropriar(self.p, jp)
    assert p2.proprietario == jp
    self = self.set('p', p2)
    assert self.p.proprietario == jp
    return self


def despejar_jogador_de_suas_propriedades(self):
    print('DESPEJO', self.j.i, self.j.nome, self.j.saldo)
    self = self.set('registro', cartorio.desapropriar(self.registro, self.j.i))
    assert cartorio.obter_propriedades(
        self.registro, self.j.i) == [], cartorio.obter_propriedades(self.registro, self.j.i
    )
    # ps = []
    # for p in self.tabuleiro.propriedades:
    #     if p.proprietario and p.proprietario.i == self.j.i:
    #         p = propriedade.apropriar(p, None)
    #     ps.append(p)
    # self = self.set('tabuleiro', self.tabuleiro.set('propriedades', ps))
    self = self.set('tipo', 'DESPEJO')
    return self
