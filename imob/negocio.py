from pyrsistent import PClass, field

from imob import banco, cartorio, jogador, propriedade


class Negocio(PClass):
    j = field(type=jogador.Jogador, mandatory=True)
    p = field(type=propriedade.Propriedade, mandatory=True)
    ji = field(type=int, mandatory=True)
    pi = field(type=int, mandatory=True)
    banco_ = field()
    registro = field(type=cartorio.Cartorio)
    js = field()


def criar_negocio(j, p, ji, pi, registro=None, b=None, js=[]):
    return Negocio(
        j=j,
        p=p,
        ji=ji,
        pi=pi,
        banco_=b,
        registro=registro,
        js=js,
    )

def comprar_ou_alugar(j, p, ji, pi, registro=None, b=None, js=[]):
    n = criar_negocio(j, p, ji, pi, registro, b, js)
    match cartorio.obter_proprietario(n.registro, pi):
        case None:
            return tentar_comprar(n)
        case jpi:
            print('-------', jpi, p.proprietario and p.proprietario.nome, pi)
            return alugar(n, jpi)


def alugar(self, jpi):
    self = self.set('banco_', banco.debitar_de(self.banco_, self.ji, self.p.aluguel))
    j2 = jogador.debitar(self.j, self.p.aluguel)
    self = self.set('j', j2)  # nao tem saldo para pagar o aluguel

    print('if', j2.saldo, banco.saldo_de(self.banco_, self.ji), '> 0')
    if banco.saldo_de(self.banco_, self.ji) >= 0:
        if banco.saldo_de(self.banco_, jpi) > 0:
            if self.p.proprietario:
                self = self.set('banco_', banco.creditar_em(self.banco_, jpi, self.p.aluguel))

                jp2 = jogador.creditar(self.p.proprietario, self.p.aluguel)
                p2 = propriedade.apropriar(self.p, jp2)  # mesmo proprietario, novo objeto.
                self = self.set('p', p2) # .set('j', j2) \
                print('*****', jp2.saldo, p2.proprietario.saldo, self.p.proprietario.saldo, banco.saldo_de(self.banco_, jpi))
    elif banco.saldo_de(self.banco_, self.ji) <= 0:  # se zerou, perdeu, perde as propriedades e nao recebe mais alugueis
        self = self.set('registro', cartorio.desapropriar(self.registro, self.ji))

    print('ALUGUEL', self.banco_, self.ji,  self.p.aluguel, j2.saldo, [j.saldo for j in self.js]) #, self.registro)
    return self


def tentar_comprar(self):
    if banco.saldo_de(self.banco_, self.ji) >= self.p.preco and estrategia_eh_comprar(self.j, self.p):
    # if jogador.tem_saldo_suficiente(self.j, self.p.preco) and estrategia_eh_comprar(self.j, self.p):
        return comprar(self)
    return self


def estrategia_eh_comprar(j, p):
    return j.estrategia(j, p)


def comprar(self):
    self = self.set('banco_', banco.debitar_de(self.banco_, self.ji, self.p.preco))
    j2 = jogador.debitar(self.j, self.p.preco)
    self = self.set('registro', cartorio.registrar_compra(self.registro, self.ji, self.pi))
    self = self.set('j', j2).set('p', propriedade.apropriar(self.p, j2))
    print('COMPRA', self.banco_, self.ji,  self.p.preco, j2.saldo, [j.saldo for j in self.js], self.registro)
    return self


