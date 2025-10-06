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
        case j_prop_i:
            print('-------', j_prop_i, p.proprietario and p.proprietario.nome, p.i)
            return alugar(n, j_prop_i)


def alugar(self, j_prop_i):
    self = self.set('banco_', banco.debitar_de(self.banco_, self.j.i, self.p.aluguel))
    j2 = jogador.debitar(self.j, self.p.aluguel)
    self = self.set('j', j2)  # nao tem saldo para pagar o aluguel

    print('if', j2.saldo, banco.saldo_de(self.banco_, self.j.i), '> 0')
    if banco.saldo_de(self.banco_, self.j.i) >= 0:
        if banco.saldo_de(self.banco_, j_prop_i) > 0:
            if self.p.proprietario:
                self = self.set('banco_', banco.creditar_em(self.banco_, j_prop_i, self.p.aluguel))

                jp2 = jogador.creditar(self.p.proprietario, self.p.aluguel)
                p2 = propriedade.apropriar(self.p, jp2)  # mesmo proprietario, novo objeto.
                self = self.set('p', p2) # .self.set('j', j2)
                self = self.set('tipo', 'ALUGUEL')
                print('*****', jp2.saldo, p2.proprietario.saldo, self.p.proprietario.saldo, banco.saldo_de(self.banco_, j_prop_i))
    elif banco.saldo_de(self.banco_, self.j.i) <= 0:  # se zerou, perdeu, perde as propriedades e nao recebe mais alugueis
        self = self.set('registro', cartorio.desapropriar(self.registro, self.j.i))

    print('ALUGUEL', self.banco_, self.j.i,  self.p.aluguel, j2.saldo, [j.saldo for j in self.js]) #, self.registro)
    return self


def tentar_comprar(self):
    if banco.saldo_de(self.banco_, self.j.i) >= self.p.preco and estrategia_eh_comprar(self.j, self.p):
    # if jogador.tem_saldo_suficiente(self.j, self.p.preco) and estrategia_eh_comprar(self.j, self.p):
        return comprar(self)
    return self


def estrategia_eh_comprar(j, p):
    return j.estrategia(j, p)


def comprar(self):
    self = self.set('banco_', banco.debitar_de(self.banco_, self.j.i, self.p.preco))
    j2 = jogador.debitar(self.j, self.p.preco)
    self = self.set('registro', cartorio.registrar_compra(self.registro, self.j.i, self.p.i))
    self = self.set('j', j2)
    p2 = propriedade.apropriar(self.p, j2)
    self = self.set('p', p2)
    self = self.set('tipo', 'COMPRA')
    print('COMPRA', self.banco_, self.j.i,  self.p.preco, j2.saldo, [j.saldo for j in self.js], self.registro)
    return self


