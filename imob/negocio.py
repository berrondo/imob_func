from pyrsistent import PClass, field

from imob import banco, cartorio, jogador, propriedade


class Negocio(PClass):
    tipo = field(type=str, initial='')  # 'compra' ou 'aluguel'
    j = field(jogador.Jogador)
    p = field(propriedade.Propriedade)
    banco_ = field()
    registro = field(type=cartorio.Cartorio)


def criar_negocio(j, p, registro=None, b=None):
    return Negocio(
        j=j,
        p=p,
        banco_=b,
        registro=registro,
    )


def comprar_ou_alugar(j, p, registro=None, b=None):
    n = criar_negocio(j, p, registro, b)
    match cartorio.obter_proprietario(n.registro, p.i):
        case None:
            return tentar_comprar(n)
        case i_proprietario:   # index do jogador proprietario
            return alugar(n, i_proprietario)


def alugar(self, i_proprietario):
    self = debitar_de_jogador(self, self.p.aluguel)

    saldo = banco.saldo_de(self.banco_, self.j.i)
    if saldo >= 0: # jogador nao perdeu
        if banco.saldo_de(self.banco_, i_proprietario) > 0: # proprietario ainda joga
            self = creditar_para_proprietario(self, i_proprietario, self.p.aluguel)
            self = self.set('tipo', 'ALUGUEL')

    if saldo <= 0: # se zerou, perdeu, perde as propriedades e nao recebe mais alugueis
        self = despejar_jogador_de_suas_propriedades(self)

    return self


def tentar_comprar(self):
    if saldo := banco.saldo_de(self.banco_, self.j.i):
        if saldo >= self.p.preco and estrategia_eh_comprar(self.j, saldo, self.p):
            return comprar(self)
    return self


def estrategia_eh_comprar(j,  saldo, p):
    return j.estrategia(saldo, p)


def comprar(self):
    self = self.set('tipo', 'COMPRA')
    self = debitar_de_jogador(self, self.p.preco)
    self = self.set(
        'registro', cartorio.registrar_compra(self.registro, self.j.i, self.p.i)
    )

    if banco.saldo_de(self.banco_, self.j.i) <= 0:
        # se zerou, perdeu, perde as propriedades e nao recebe mais alugueis
        self = despejar_jogador_de_suas_propriedades(self)

    return self


def debitar_de_jogador(self, valor):
    self = self.set('banco_', banco.debitar_de(self.banco_, self.j.i, valor))
    return self


def creditar_para_proprietario(self, jpi, valor):
    self = self.set('banco_', banco.creditar_em(self.banco_, jpi, valor))
    return self


def despejar_jogador_de_suas_propriedades(self):
    print('DESPEJO', self.j.i, self.j.nome)
    self = self.set('registro', cartorio.desapropriar(self.registro, self.j.i))
    assert cartorio.obter_propriedades(
        self.registro, self.j.i
    ) == [], cartorio.obter_propriedades(self.registro, self.j.i)
    self = self.set('tipo', 'DESPEJO')
    return self
