from pyrsistent import m

from jogador import (
    saldo_suficiente,
    debita,
    apropria,
)

from estrategia import (
    impulsivo,
    deve_comprar,
)

from propriedade import (
    desapropriada,
)


def compra(j, p):
    if saldo_suficiente(j, p.preco) \
            and deve_comprar(j, p) \
            :
        j2 = debita(j, p.preco)
        p2 = apropria(j2, p)
        return j2, p2

    return j, p


def aluga(j, p):
    if saldo_suficiente(j, p.aluguel):
        j2 = debita(j, p.aluguel)
        p2 = p.proprietario.set(
            'saldo',
            p.proprietario.saldo + p.aluguel
        )
        return j2, p2

    return j, p


def compra_ou_aluga(j, p):
    if desapropriada(p):
        return compra(j, p)

    else:
        return aluga(j, p)


def test_impulsivo_compra():
    j1 = m(estrategia=impulsivo, saldo=300)
    p1 = m(preco=30, aluguel=3, proprietario=None)

    j2, p2 = compra_ou_aluga(j1, p1)

    assert j2.saldo == 270
    assert p2.proprietario == j2
