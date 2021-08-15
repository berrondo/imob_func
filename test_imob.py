from pyrsistent import m

from jogador import (
    saldo_suficiente,
    debita,
    credita,
)

from estrategia import (
    impulsivo,
    deve_comprar,
)

from propriedade import (
    desapropriada,
    apossada,
)


def compra(j, p, jp):
    if saldo_suficiente(j, p.preco) \
            and deve_comprar(j, p) \
            :
        j2 = debita(j, p.preco)
        p2 = apossada(p, j2)
        return j2, p2, jp

    return j, p, jp


def aluga(j, p, jp):
    if saldo_suficiente(j, p.aluguel):
        j2 = debita(j, p.aluguel)
        jp2 = credita(p.proprietario, p.aluguel)
        p2 = p.set('proprietario', jp2)  # ????? !!!!!
        return j2, p2, jp2

    return j, p, jp


def compra_ou_aluga(j, p, jp):
    if desapropriada(p):
        return compra(j, p, jp)

    else:
        return aluga(j, p, jp)


def test_impulsivo_compra():
    j1 = m(estrategia=impulsivo, saldo=300)
    p1 = m(preco=30, aluguel=3, proprietario=None)

    assert p1.proprietario is None

    j2, p2, _ = compra_ou_aluga(j1, p1, None)

    assert j2.saldo == 270
    assert p2.proprietario == j2


def test_impulsivo_sem_saldo_pra_compra_aluga():
    j1 = m(estrategia=impulsivo, saldo=29)
    jp1 = m(estrategia=impulsivo, saldo=1)
    p1 = m(preco=30, aluguel=3, proprietario=jp1)

    j2, p2, jp2 = compra_ou_aluga(j1, p1, jp1)

    assert j2.saldo == 26
    assert p2.proprietario == jp2
    assert jp2.saldo == 4


def test_aluga_transfere_valor_do_aluguel():
    j = m(estrategia=impulsivo, saldo=29)
    jp = m(estrategia=impulsivo, saldo=3000000)
    p = m(preco=30, aluguel=3, proprietario=jp)

    j2, p2, jp2 = aluga(j, p, jp)

    assert j2.saldo == 26
    assert p2.proprietario == jp2
    assert jp2.saldo == 3000003
