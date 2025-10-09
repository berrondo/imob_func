from pyrsistent import PClass, field

from imob import banco, cartorio, jogador, propriedade


class Negocio(PClass):
    tipo = field(type=str, initial='')
    j = field(jogador.Jogador)
    p = field(propriedade.Propriedade)
    banco_ = field()
    registro = field(type=cartorio.Cartorio)


def criar_negocio(j, p, registro=None, b=None):
    return Negocio(j=j, p=p, banco_=b, registro=registro)


def comprar_ou_alugar(j, p, registro=None, b=None):
    n = criar_negocio(j, p, registro, b)

    match cartorio.obter_proprietario(n.registro, p.i):
        case None:
            n = tentar_comprar(n)
        case i_proprietario:
            n = alugar(n, i_proprietario)

    if saldo_de(n, n.j.i) <= 0:
        return despejar_jogador_de_suas_propriedades(n), True  # eliminado!

    return n, False


def tentar_comprar(n):
    saldo = saldo_de(n, n.j.i)
    if saldo >= n.p.preco and estrategia_eh_comprar(n.j, saldo, n.p):
        n = comprar(n)
    return n


def comprar(n):
    n = debitar_de_jogador(n, n.p.preco)
    n = n.set('registro', cartorio.registrar_compra(n.registro, n.j.i, n.p.i))
    return n.set('tipo', 'COMPRA')


def alugar(n, i_proprietario):
    n = debitar_de_jogador(n, n.p.aluguel)
    saldo = saldo_de(n, n.j.i)
    if saldo >= 0 and saldo_de(n, i_proprietario) > 0:  # proprietario ainda joga
        n = creditar_para_proprietario(n, i_proprietario, n.p.aluguel)
        n = n.set('tipo', 'ALUGUEL')
    return n


def saldo_de(n, ji):
    return banco.saldo_de(n.banco_, ji)


def estrategia_eh_comprar(j,  saldo, p):
    return j.estrategia(saldo, p)


def debitar_de_jogador(n, valor):
    return n.set('banco_', banco.debitar_de(n.banco_, n.j.i, valor))


def creditar_para_proprietario(n, jpi, valor):
    return n.set('banco_', banco.creditar_em(n.banco_, jpi, valor))


def despejar_jogador_de_suas_propriedades(n):
    n = n.set('registro', cartorio.desapropriar(n.registro, n.j.i))
    return n.set('tipo', 'DESPEJO')
