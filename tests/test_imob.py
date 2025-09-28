import pytest

from imob.estrategia import aleatorio, cauteloso, exigente, impulsivo
from imob.jogador import criar_jogador
from imob.negocio import comprar_ou_alugar
from imob.propriedade import criar_propriedade

DEZ = 10
CEM = 100


# impulsivo

@pytest.mark.parametrize(
    "preco,comprou",
    [
        (99, True),      # compra quando saldo suficiente
        (100, True),     # compra mesmo gastando todo o saldo
        (101, False),    # não compra quando preço maior que saldo
    ]
)
def test_impulsivo_compra_se_tem_saldo(preco, comprou):
    j1 = criar_jogador(estrategia=impulsivo, saldo=CEM)
    p1 = criar_propriedade(preco=preco, aluguel=DEZ)

    assert p1.proprietario is None

    j2, p2 = comprar_ou_alugar(j1, p1)

    if comprou:
        assert j2.saldo == CEM - preco
        assert p2.proprietario == j2
    else:
        assert j2.saldo == CEM
        assert p2.proprietario is None

# exigente

@pytest.mark.parametrize(
    "preco,comprou",
    [
        (99, True),    # compra quando tem saldo suficiente
        (100, True),      # compra gastando todo o saldo
        (101, False),    # não compra quando não tem saldo suficiente
    ]
)
def test_exigente_compra_se_tem_saldo_e_aluguel_maior_que_50(preco, comprou):
    j1 = criar_jogador(estrategia=exigente, saldo=CEM)
    p1 = criar_propriedade(preco=preco, aluguel=51)

    assert p1.proprietario is None

    j2, p2 = comprar_ou_alugar(j1, p1)

    if comprou:
        assert j2.saldo == CEM - preco
        assert p2.proprietario == j2
    else:
        assert j2.saldo == CEM
        assert p2.proprietario is None

# cauteloso

@pytest.mark.parametrize(
    "preco,comprou",
    [
        (19, True),    # compra quando sobra > 80
        (20, True),    # compra deixando exatos 80
        (21, False),   # não compra quando sobra < 80
    ]
)
def test_cauteloso_compra_se_sobrar_pelo_menos_80(preco, comprou):
    j1 = criar_jogador(estrategia=cauteloso, saldo=CEM)
    p1 = criar_propriedade(preco=preco, aluguel=DEZ)

    assert p1.proprietario is None

    j2, p2 = comprar_ou_alugar(j1, p1)

    if comprou:
        assert j2.saldo == CEM - preco
        assert p2.proprietario == j2
    else:
        assert j2.saldo == CEM
        assert p2.proprietario is None


# aleatorio

@pytest.mark.parametrize("random_choice", [True, False])
def test_aleatorio_compra_conforme_random(monkeypatch, random_choice):
    monkeypatch.setattr('random.choice', lambda _: random_choice)

    j1 = criar_jogador(estrategia=aleatorio, saldo=CEM)
    p1 = criar_propriedade(preco=CEM, aluguel=DEZ)

    assert p1.proprietario is None

    j2, p2 = comprar_ou_alugar(j1, p1)

    if random_choice is True:
        assert j2.saldo == 0
        assert p2.proprietario == j2
    else:
        assert j2.saldo == CEM
        assert p2.proprietario is None


# todos

@pytest.mark.parametrize("estrategia", [impulsivo, exigente, cauteloso, aleatorio])
@pytest.mark.parametrize(
    "aluguel,novo_saldo,novo_saldo_proprietario",
    [
        (99, 1, 199),         # aluguel < saldo
        (100, 0, 200),        # aluguel = saldo
        (101, 100, 100),      # aluguel > saldo
    ]
)
def test_aluga_se_ha_proprietario_e_saldo_suficiente(
        estrategia, aluguel, novo_saldo, novo_saldo_proprietario
    ):
    j1 = criar_jogador(estrategia=estrategia, saldo=CEM)
    jp1 = criar_jogador(estrategia=impulsivo, saldo=CEM)
    p1 = criar_propriedade(preco=30, aluguel=aluguel, proprietario=jp1)

    j2, p2 = comprar_ou_alugar(j1, p1)

    assert j2.saldo == novo_saldo
    assert p2.proprietario.saldo == novo_saldo_proprietario
