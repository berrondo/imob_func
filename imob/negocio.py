from pyrsistent import PClass, field

from imob import banco, cartorio, jogador, propriedade


class Negocio(PClass):
    tipo = field(type=str, initial='')  # 'compra' ou 'aluguel'
    j = field(jogador.Jogador)
    p = field(propriedade.Propriedade)
    banco_ = field()
    registro = field(type=cartorio.Cartorio)
    js = field()


def criar_negocio(j, p, registro=None, b=None, js=[]):
    return Negocio(
        j=j,
        p=p,
        banco_=b,
        registro=registro,
        js=js,
    )


def comprar_ou_alugar(j, p, registro=None, b=None, js=[]):
    n = criar_negocio(j, p, registro, b, js)
    match cartorio.obter_proprietario(n.registro, p.i):
        case None:
            return tentar_comprar(n)
        case i_proprietario:   # index do jogador proprietario
            print('-----', i_proprietario, p.proprietario and p.proprietario.nome, p.i)
            # try: i_proprietario == p.proprietario.i, (i_proprietario, p.proprietario)
            # except: import pdb; pdb.set_trace()
            # assert p.proprietario and p.proprietario.i == i_proprietario, \
            #        (i_proprietario, p.proprietario)
            return alugar(n, i_proprietario)


def alugar(self, i_proprietario):
    self = debitar_de_jogador(self, self.p.aluguel)

    print('if', self.j.saldo, banco.saldo_de(self.banco_, self.j.i), '> 0')
    if banco.saldo_de(self.banco_, self.j.i) >= 0: # jogador nao perdeu
        if banco.saldo_de(self.banco_, i_proprietario) > 0: # proprietario ainda joga
            if self.p.proprietario: # proprietario ainda esta setado!!!
                if self.p.proprietario.saldo > 0: # objeto nao desapropriado
                    assert self.p.proprietario.i == i_proprietario, (i_proprietario, self.p)
                    self = creditar_para_proprietario(self, self.p.proprietario, self.p.aluguel)
                    self = self.set('tipo', 'ALUGUEL')
            else:
                print('PROPRIETARIO DESAPROPRIADO ANTES DE RECEBER ALUGUEL', self.p.i, i_proprietario)

    elif banco.saldo_de(self.banco_, self.j.i) <= 0:  # se zerou, perdeu, perde as propriedades e nao recebe mais alugueis
        self = despejar_jogador_de_suas_propriedades(self)

    print('ALUGUEL', self.banco_, self.j.i,  self.p.aluguel, self.j.saldo, [j.saldo for j in self.js]) #, self.registro)
    return self


def tentar_comprar(self):
    if banco.saldo_de(self.banco_, self.j.i) >= self.p.preco and estrategia_eh_comprar(self.j, self.p):
    # if jogador.tem_saldo_suficiente(self.j, self.p.preco) and estrategia_eh_comprar(self.j, self.p):
        return comprar(self)
    return self


def estrategia_eh_comprar(j, p):
    return j.estrategia(j, p)


def comprar(self):
    self = self.set('tipo', 'COMPRA')
    self = self.set('registro', cartorio.registrar_compra(self.registro, self.j.i, self.p.i))
    self = debitar_de_jogador(self, self.p.preco)
    self = atualizar_proprietario(self, self.j)
    print('COMPRA', self.banco_, self.j.i,  self.p.preco, self.j.saldo, [j.saldo for j in self.js], self.registro)
    return self


def debitar_de_jogador(self, valor):
    self = self.set('banco_', banco.debitar_de(self.banco_, self.j.i, valor))
    j2 = jogador.debitar(self.j, valor)
    self = self.set('j', j2)
    return self


def creditar_para_proprietario(self, jp, valor):
    if self.p.proprietario:
        self = self.set('banco_', banco.creditar_em(self.banco_, jp.i, valor))
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
    assert cartorio.obter_propriedades(self.registro, self.j.i) == set(), cartorio.obter_propriedades(self.registro, self.j.i)
    print(' ', self.registro)
    ps = []
    for p in self.tabuleiro.propriedades:
        if p.proprietario and p.proprietario.i == self.j.i:
            p = propriedade.apropriar(p, None)
        ps.append(p)
    self = self.set('tabuleiro', self.tabuleiro.set('propriedades', ps))
    return self
