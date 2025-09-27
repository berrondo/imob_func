from jogador import (
    criar_jogador,
)

from estrategia import (
    impulsivo,
)

from propriedade import (
    criar_propriedade,
)

from negocio import (
    comprar_ou_alugar,
    alugar,
)


def test_impulsivo_compra():
    j1 = criar_jogador(estrategia=impulsivo, saldo=300)
    p1 = criar_propriedade(preco=30, aluguel=3)

    assert p1.proprietario is None

    j2, p2, _ = comprar_ou_alugar(j1, p1, None)

    assert j2.saldo == 270
    assert p2.proprietario == j2


def test_impulsivo_sem_saldo_pra_comprar_aluga():
    j1 = criar_jogador(estrategia=impulsivo, saldo=29)
    jp1 = criar_jogador(estrategia=impulsivo, saldo=1)
    p1 = criar_propriedade(preco=30, aluguel=3, proprietario=jp1)

    j2, p2, jp2 = comprar_ou_alugar(j1, p1, jp1)

    assert j2.saldo == 26
    assert p2.proprietario == jp2
    assert jp2.saldo == 4


def test_aluga_transfere_valor_do_aluguel():
    j1 = criar_jogador(estrategia=impulsivo, saldo=29)
    jp1 = criar_jogador(estrategia=impulsivo, saldo=3000000)
    p1 = criar_propriedade(preco=30, aluguel=3, proprietario=jp1)

    j2, p2, jp2 = alugar(j1, p1, jp1)

    assert j2.saldo == 26
    assert p2.proprietario == jp2
    assert jp2.saldo == 3000003
