from pyrsistent import PClass, field

from imob import banco, cartorio, jogador, propriedade
from imob.classes_de_dados import JJogador, JPropriedade, JRegistro


class Negocio(PClass):
    tipo = field(type=str, initial='')  # 'compra' ou 'aluguel'

    jj = field(type=(JJogador,), mandatory=True)
    pp = field(type=(JPropriedade,), mandatory=True)

    banco_ = field()
    registro = field(type=cartorio.Cartorio)

    js = field()


def criar_negocio(jj, pp, registro=None, b=None, js=[]):
    return Negocio(
        jj=jj,
        pp=pp,

        banco_=b,
        registro=registro,

        js=js,
    )


def comprar_ou_alugar(jj, pp, registro=None, b=None, js=[]):
    n = criar_negocio(jj, pp, registro, b, js)
    match cartorio.obter_proprietario(n.registro, pp.pi):
        case None:
            return tentar_comprar(n)
        case j_prop_i:
            print('-------', j_prop_i, pp.p.proprietario and pp.p.proprietario.nome, pp.pi)
            return alugar(n, j_prop_i)


def alugar(self, j_prop_i):
    self = self.set('banco_', banco.debitar_de(self.banco_, self.jj.ji, self.pp.p.aluguel))
    j2 = jogador.debitar(self.jj.j, self.pp.p.aluguel)
    self = self.set('jj', JJogador(j=j2, ji=self.jj.ji))  # nao tem saldo para pagar o aluguel

    print('if', j2.saldo, banco.saldo_de(self.banco_, self.jj.ji), '> 0')
    if banco.saldo_de(self.banco_, self.jj.ji) >= 0:
        if banco.saldo_de(self.banco_, j_prop_i) > 0:
            if self.pp.p.proprietario:
                self = self.set('banco_', banco.creditar_em(self.banco_, j_prop_i, self.pp.p.aluguel))

                jp2 = jogador.creditar(self.pp.p.proprietario, self.pp.p.aluguel)
                p2 = propriedade.apropriar(self.pp.p, jp2)  # mesmo proprietario, novo objeto.
                self = self.set('pp', JPropriedade(p=p2, pi=self.pp.pi)) # .set('jj', JJogador(j=j2, ji=self.jj.ji)) \
                self = self.set('tipo', 'ALUGUEL')
                print('*****', jp2.saldo, p2.proprietario.saldo, self.pp.p.proprietario.saldo, banco.saldo_de(self.banco_, j_prop_i))
    elif banco.saldo_de(self.banco_, self.jj.ji) <= 0:  # se zerou, perdeu, perde as propriedades e nao recebe mais alugueis
        self = self.set('registro', cartorio.desapropriar(self.registro, self.jj.ji))

    print('ALUGUEL', self.banco_, self.jj.ji,  self.pp.p.aluguel, j2.saldo, [j.saldo for j in self.js]) #, self.registro)
    return self


def tentar_comprar(self):
    if banco.saldo_de(self.banco_, self.jj.ji) >= self.pp.p.preco and estrategia_eh_comprar(self.jj.j, self.pp.p):
    # if jogador.tem_saldo_suficiente(self.jj.j, self.pp.p.preco) and estrategia_eh_comprar(self.jj.j, self.pp.p):
        return comprar(self)
    return self


def estrategia_eh_comprar(j, p):
    return j.estrategia(j, p)


def comprar(self):
    self = self.set('banco_', banco.debitar_de(self.banco_, self.jj.ji, self.pp.p.preco))
    j2 = jogador.debitar(self.jj.j, self.pp.p.preco)
    self = self.set('registro', cartorio.registrar_compra(self.registro, self.jj.ji, self.pp.pi))
    self = self.set('jj', JJogador(j=j2, ji=self.jj.ji))
    p2 = propriedade.apropriar(self.pp.p, j2)
    self = self.set('pp', JPropriedade(p=p2, pi=self.pp.pi))
    self = self.set('tipo', 'COMPRA')
    print('COMPRA', self.banco_, self.jj.ji,  self.pp.p.preco, j2.saldo, [j.saldo for j in self.js], self.registro)
    return self


