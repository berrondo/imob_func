from pyrsistent import PClass, field

from imob import banco, cartorio, jogador, propriedade


class Negocio(PClass):
    tipo = field(type=str, initial='')
    precondicoes = field(type=bool, initial=False)
    j = field(type=jogador.Jogador)
    p = field(type=propriedade.Propriedade)
    valor = field(type=int)
    debitar_de = field(type=int)
    creditar_para = field(type=(int, type(None)), initial=None)
    seria_eliminado = field(type=bool, initial=False)


def tentar_comprar(j, p, ppi, registro, banco_):
    assert ppi is None, (registro.compras, j.i, p.i)
    valor = p.preco

    c = Negocio(
        tipo='COMPRA',
        precondicoes=all([
            ppi is None,
            banco.saldo_de(banco_, j.i) >= p.preco,
            j.estrategia(banco.saldo_de(banco_, j.i), p)
        ]),
        creditar_para=None,

        j=j, p=p, valor=valor, debitar_de=j.i,
        seria_eliminado=(banco.saldo_de(banco_, j.i) - valor) <= 0,
    )

    match c.precondicoes:
        case True:
            match c.seria_eliminado:
                case False:
                    banco_ = banco.debitar_de(banco_, c.debitar_de, c.valor)
                    registro = cartorio.registrar_compra(registro, c.debitar_de, p.i)
                case True:
                    banco_ = banco.debitar_de(banco_, c.debitar_de, c.valor)
                    registro = cartorio.desapropriar(registro, c.debitar_de)
                    c = c.set('tipo', 'DESPEJO')
        case False:
            c = c.set('seria_eliminado', False)
            c = c.set('tipo', '')

    return c, registro, banco_


def tentar_alugar(j, p, ppi, registro, banco_):
    assert ppi is not None, (registro.compras, j.i, p.i)
    valor = p.aluguel

    a = Negocio(
        tipo='ALUGUEL',
        precondicoes=True,
        creditar_para=ppi,

        j=j, p=p, valor=valor, debitar_de=j.i,
        seria_eliminado=(banco.saldo_de(banco_, j.i) - valor) <= 0,
    )

    match a.seria_eliminado:
        case False:
            banco_ = banco.debitar_de(banco_, a.debitar_de, a.valor)
            banco_ = banco.creditar_em(banco_, a.creditar_para, a.valor)
        case True:
            banco_ = banco.debitar_de(banco_, a.debitar_de, a.valor)
            registro = cartorio.desapropriar(registro, a.debitar_de)
            a = a.set('tipo', 'DESPEJO')

    return a, registro, banco_


def comprar_ou_alugar(j, p, registro, banco_):
    ppi = cartorio.obter_proprietario(registro, p.i)
    match ppi:
        case None:
            return tentar_comprar(j, p, ppi, registro, banco_)
        case _:
            return tentar_alugar(j, p, ppi, registro, banco_)
