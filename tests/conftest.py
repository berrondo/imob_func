import pytest

from imob.banco import criar_banco
from imob.estrategia import estrategias
from imob.jogador import criar_jogador
from imob.propriedade import criar_propriedade

SALDO_INICIAL = 300


@pytest.fixture
def jogadores():
    return [criar_jogador(e, SALDO_INICIAL) for e in estrategias]


@pytest.fixture
def propriedades():
    return [criar_propriedade(preco=100, aluguel=10)] * 20


@pytest.fixture
def banco():
    return criar_banco(len(estrategias), SALDO_INICIAL)
