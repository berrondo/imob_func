from pyrsistent import CheckedPVector, PClass, field


class Propriedade(PClass):
    preco = field(type=int, mandatory=True)
    aluguel = field(type=int, mandatory=True)
    proprietario = field(initial=None)


def criar_propriedade(preco, aluguel, proprietario=None):
    return Propriedade(
        preco=preco,
        aluguel=aluguel,
        proprietario=proprietario
    )


# def tem_proprietario(self):
#     return self.proprietario is not None


def apropriar(self, jogador):
    return self.set('proprietario', jogador)


def desapropriar(self):
    return self.set('proprietario', None)


class Propriedades(CheckedPVector):
    __type__ = Propriedade
