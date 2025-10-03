from pyrsistent import PRecord, field

from imob.jogador import Jogador


class Propriedade(PRecord):
    preco = field(type=int)
    aluguel = field(type=int)
    proprietario = field()


def criar_propriedade(preco, aluguel, proprietario=None):
    return Propriedade(
        preco=preco,
        aluguel=aluguel,
        proprietario=proprietario
    )


def tem_proprietario(self):
    return self.proprietario is not None


def apropriar(self, jogador):
    return self.set('proprietario', jogador)
