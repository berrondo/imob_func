from imob.cartorio import (
    Cartorio,
    criar_cartorio,
    desapropriar,
    obter_propriedades,
    obter_proprietario,
    registrar_compra,
)


def test_criar_cartorio():
    c = criar_cartorio()

    assert isinstance(c, Cartorio)


def test_registrar_compra():
    c = criar_cartorio()

    c = registrar_compra(c, ji=0, pi=0)
    assert c.compras == {(0, 0)}


def test_registrar_compras():
    c = criar_cartorio()

    c = registrar_compra(c, ji=0, pi=0)
    assert c.compras == {(0, 0)}

    c = registrar_compra(c, ji=0, pi=0)
    assert c.compras == {(0, 0)}

    c = registrar_compra(c, ji=0, pi=1)
    assert c.compras == {(0, 0), (0, 1)}

    c = registrar_compra(c, ji=3, pi=19)
    assert c.compras == {(0, 0), (0, 1), (3, 19)}


def test_obter_proprietario():
    c = criar_cartorio()

    c = registrar_compra(c, ji=0, pi=0)
    c = registrar_compra(c, ji=0, pi=1)
    c = registrar_compra(c, ji=3, pi=19)


    assert obter_proprietario(c, 0) == 0
    assert obter_proprietario(c, 1) == 0
    assert obter_proprietario(c, 19) == 3
    assert obter_proprietario(c, 2) is None


def test_obter_propriedades():
    c = criar_cartorio()

    c = registrar_compra(c, ji=0, pi=0)
    c = registrar_compra(c, ji=0, pi=1)
    c = registrar_compra(c, ji=3, pi=19)


    assert set(obter_propriedades(c, 0)) == {0, 1}
    assert obter_propriedades(c, 3) == [19]
    assert obter_propriedades(c, 2) == []
    assert obter_propriedades(c, 18) == []


def test_desapropriar_de():
    c = criar_cartorio()

    c = registrar_compra(c, ji=0, pi=0)
    c = registrar_compra(c, ji=0, pi=1)
    c = registrar_compra(c, ji=3, pi=19)

    assert c.compras == {(0, 0), (0, 1), (3, 19)}

    c = desapropriar(c, 0)
    assert c.compras == {(3, 19)}

    c = desapropriar(c, 3)
    assert c.compras == set()

    c = desapropriar(c, 2)
    assert c.compras == set()
