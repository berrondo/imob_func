from pyrsistent import CheckedPVector, PClass, field


class Jogador(PClass):
    estrategia = field(mandatory=True)
    saldo = field(
        type=int,
        mandatory=True,
        # invariant=lambda saldo: (saldo >= 0, 'saldo negativo'),
    )
    nome = field(type=str)

    def __str__(self):
        return f"{self.nome:<10} $ {self.saldo}"


def criar_jogador(estrategia, saldo):
    return Jogador(
        estrategia=estrategia,
        saldo=saldo,
        nome=estrategia.__name__
    )


def tem_saldo_suficiente(self, valor):
    return self.saldo >= valor


def debitar(self, valor):
    return self.set('saldo', self.saldo - valor)


def creditar(self, valor):
    return self.set('saldo', self.saldo + valor)


class Jogadores(CheckedPVector):
    __type__ = Jogador
