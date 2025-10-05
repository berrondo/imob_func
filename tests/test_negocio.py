import pytest
from pyrsistent import InvariantException

from imob.banco import criar_banco
from imob.cartorio import criar_cartorio, registrar_compra
from imob.estrategia import aleatorio, cauteloso, exigente, impulsivo
from imob.jogador import criar_jogador
from imob.negocio import comprar_ou_alugar
from imob.propriedade import criar_propriedade

DEZ = 10
CEM = 300
C = criar_cartorio()


def test_criar_negocio(banco):
    j1 = criar_jogador(estrategia=impulsivo, saldo=CEM)
    p1 = criar_propriedade(preco=30, aluguel=DEZ)

    n = comprar_ou_alugar(j1, p1, 0, 0, C, banco)

    assert n.j is not None
    assert n.p is not None
    assert n.ji == 0
    assert n.pi == 0
    assert n.registro.compras == {(0, 0)}


# impulsivo

@pytest.mark.parametrize(
    "preco,comprou",
    [
        (299, True),      # compra quando saldo suficiente
        (300, True),     # compra mesmo gastando todo o saldo
        (301, False),    # não compra quando preço maior que saldo
    ]
)
def test_impulsivo_compra_se_tem_saldo(preco, comprou, banco):
    j1 = criar_jogador(estrategia=impulsivo, saldo=CEM)
    p1 = criar_propriedade(preco=preco, aluguel=DEZ)

    assert p1.proprietario is None

    n = comprar_ou_alugar(j1, p1, 0, 0, C, banco)

    if comprou:
        assert n.j.saldo == CEM - preco
        assert n.p.proprietario == n.j
    else:
        assert n.j.saldo == CEM
        assert n.p.proprietario is None

# exigente

@pytest.mark.parametrize(
    "preco,comprou",
    [
        (299, True),    # compra quando tem saldo suficiente
        (300, True),      # compra gastando todo o saldo
        (301, False),    # não compra quando não tem saldo suficiente
    ]
)
def test_exigente_compra_se_tem_saldo_e_aluguel_maior_que_50(preco, comprou, banco):
    j1 = criar_jogador(estrategia=exigente, saldo=CEM)
    p1 = criar_propriedade(preco=preco, aluguel=51)

    assert p1.proprietario is None

    n = comprar_ou_alugar(j1, p1, 0, 0, C, banco)

    if comprou:
        assert n.j.saldo == CEM - preco
        assert n.p.proprietario == n.j
    else:
        assert n.j.saldo == CEM
        assert n.p.proprietario is None

# cauteloso

@pytest.mark.parametrize(
    "preco,comprou",
    [
        (219, True),    # compra quando sobra > 80
        (220, True),    # compra deixando exatos 80
        (221, False),   # não compra quando sobra < 80
    ]
)
def test_cauteloso_compra_se_sobrar_pelo_menos_80(preco, comprou, banco):
    j1 = criar_jogador(estrategia=cauteloso, saldo=CEM)
    p1 = criar_propriedade(preco=preco, aluguel=DEZ)

    assert p1.proprietario is None

    n = comprar_ou_alugar(j1, p1, 0, 0, C, banco)

    if comprou:
        assert n.j.saldo == CEM - preco
        assert n.p.proprietario == n.j
    else:
        assert n.j.saldo == CEM
        assert n.p.proprietario is None


# aleatorio

@pytest.mark.parametrize("random_choice", [True, False])
def test_aleatorio_compra_conforme_random(monkeypatch, random_choice, banco):
    monkeypatch.setattr('random.choice', lambda _: random_choice)

    j1 = criar_jogador(estrategia=aleatorio, saldo=CEM)
    p1 = criar_propriedade(preco=CEM, aluguel=DEZ)

    assert p1.proprietario is None

    n = comprar_ou_alugar(j1, p1, 0, 0, C, banco)

    if random_choice is True:
        assert n.j.saldo == 0
        assert n.p.proprietario == n.j
    else:
        assert n.j.saldo == CEM
        assert n.p.proprietario is None


# todos

B = criar_banco(1, CEM)

@pytest.mark.parametrize("estrategia", [impulsivo, exigente, cauteloso, aleatorio])
@pytest.mark.parametrize(
    "aluguel,novo_saldo,novo_saldo_proprietario",
    [
        (299, 1, 599),         # aluguel < saldo
        (300, 0, 300),        # aluguel = saldo
        (301, -1, 300),        # aluguel > saldo
    ]
)
def test_sempre_paga_aluguel_se_ha_proprietario(
        estrategia, aluguel, novo_saldo, novo_saldo_proprietario, banco
    ):
    j1 = criar_jogador(estrategia=estrategia, saldo=CEM)
    jp1 = criar_jogador(estrategia=impulsivo, saldo=CEM)
    p1 = criar_propriedade(preco=30, aluguel=aluguel, proprietario=jp1)
    c = registrar_compra(C, 0, 0)  # proprietario registrado

    # with pytest.raises(InvariantException):
    n = comprar_ou_alugar(j1, p1, 0, 0, c, B)

    assert n.j.saldo == novo_saldo
    assert n.p.proprietario.saldo == novo_saldo_proprietario
