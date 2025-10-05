import imob.jogador as jogador
import imob.propriedade as propriedade
from imob.estrategia import impulsivo


def test_criar_propriedade():
    p = propriedade.criar_propriedade(preco=100, aluguel=10)

    assert p.preco == 100
    assert p.aluguel == 10
    assert p.proprietario is None


def test_apropriar():
    p = propriedade.criar_propriedade(preco=100, aluguel=10)
    j = jogador.criar_jogador(estrategia=impulsivo, saldo=300)

    # assert not propriedade.tem_proprietario(p)

    p2 = propriedade.apropriar(p, j)

    # assert propriedade.tem_proprietario(p2)
    assert p2.proprietario is j

