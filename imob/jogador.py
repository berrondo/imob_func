from pyrsistent import CheckedPVector, PClass, field


class Jogador(PClass):
    estrategia = field(mandatory=True)
    nome = field(type=str)
    i = field(type=int)  # gambiarra!

    def __str__(self):
        return f"{self.nome:<10}"


def criar_jogador(estrategia):
    return Jogador(
        estrategia=estrategia,
        nome=estrategia.__name__
    )


class Jogadores(CheckedPVector):
    __type__ = Jogador
