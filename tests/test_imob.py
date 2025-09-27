import pytest

from src.jogador import criar_jogador
from src.estrategia import impulsivo, exigente
from src.propriedade import criar_propriedade
from src.negocio import comprar_ou_alugar


# impulsivo

@pytest.mark.parametrize(
    "saldo,preco,aluguel,novo_saldo,comprou",
    [
        (300, 30, 3, 270, True),     # compra quando tem saldo suficiente
        (29, 30, 3, 29, False),      # não compra quando saldo insuficiente
        (100, 100, 10, 0, True),     # compra mesmo gastando todo o saldo
        (100, 101, 10, 100, False),  # não compra quando preço maior que saldo
    ]
)
def test_impulsivo_compra_se_tem_saldo(saldo, preco, aluguel, novo_saldo, comprou):
    j1 = criar_jogador(estrategia=impulsivo, saldo=saldo)
    p1 = criar_propriedade(preco=preco, aluguel=aluguel)

    assert p1.proprietario is None

    j2, p2, _ = comprar_ou_alugar(j1, p1, None)

    assert j2.saldo == novo_saldo
    if comprou:
        assert p2.proprietario == j2
    else:
        assert p2.proprietario is None


@pytest.mark.parametrize(
    "saldo,saldo_proprietario,aluguel,novo_saldo,novo_saldo_proprietario",
    [
        (29, 1, 3, 26, 4),          # aluga quando tem saldo suficiente
        (2, 100, 3, 2, 100),        # não aluga quando saldo insuficiente
        (10, 50, 10, 0, 60),        # aluga gastando todo o saldo
        (9, 200, 10, 9, 200),       # não aluga quando aluguel maior que saldo
    ]
)
def test_impulsivo_aluga_se_ha_proprietario_e_saldo_suficiente(
        saldo, saldo_proprietario, aluguel, novo_saldo, novo_saldo_proprietario
    ):
    j1 = criar_jogador(estrategia=impulsivo, saldo=saldo)
    jp1 = criar_jogador(estrategia=impulsivo, saldo=saldo_proprietario)
    p1 = criar_propriedade(preco=30, aluguel=aluguel, proprietario=jp1)

    j2, p2, jp2 = comprar_ou_alugar(j1, p1, jp1)

    assert j2.saldo == novo_saldo
    assert p2.proprietario == jp2
    assert jp2.saldo == novo_saldo_proprietario


# exigente

@pytest.mark.parametrize(
    "saldo,preco,aluguel,novo_saldo,comprou",
    [
        (500, 300, 51, 200, True),    # compra quando aluguel > 50 e saldo suficiente
        (500, 300, 50, 500, False),    # não compra quando aluguel = 50
        (500, 300, 49, 500, False),    # não compra quando aluguel < 50
        (500, 500, 51, 0, True),      # compra quando aluguel > 50 e saldo suficiente
        (500, 501, 51, 500, False),    # não compra quando não tem saldo suficiente
    ]
)
def test_exigente_compra_se_tem_saldo_e_aluguel_maior_que_50(
        saldo, preco, aluguel, novo_saldo, comprou
    ):
    j1 = criar_jogador(estrategia=exigente, saldo=saldo)
    p1 = criar_propriedade(preco=preco, aluguel=aluguel)

    assert p1.proprietario is None

    j2, p2, _ = comprar_ou_alugar(j1, p1, None)

    assert j2.saldo == novo_saldo
    if comprou:
        assert p2.proprietario == j2
    else:
        assert p2.proprietario is None
