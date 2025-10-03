import pytest

from imob.estrategia import estrategias
from imob.jogador import criar_jogador
from imob.propriedade import criar_propriedade


@pytest.fixture
def jogadores():
    return [criar_jogador(e, 300) for e in estrategias]


@pytest.fixture
def propriedades():
    return [criar_propriedade(preco=100, aluguel=10)] * 20
