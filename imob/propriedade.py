from pyrsistent import CheckedPVector, PClass, field


class Propriedade(PClass):
    preco = field(type=int, mandatory=True)
    aluguel = field(type=int, mandatory=True)
    i = field(type=int)  # gambiarra!

    def __str__(self):
        return f"${self.preco:>4}/{self.aluguel:<3} " \
               f"{self.proprietario.nome if self.proprietario else 'None':<10}"


def criar_propriedade(preco, aluguel, proprietario=None):
    return Propriedade(
        preco=preco,
        aluguel=aluguel,
    )


class Propriedades(CheckedPVector):
    __type__ = Propriedade
