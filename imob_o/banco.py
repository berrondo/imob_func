from pyrsistent import PClass, pvector_field, v


class Banco(PClass):
    contas = pvector_field(int)


def criar_banco(n_jogadores, saldo_inicial) -> Banco:
    return Banco(
        contas=v(*(saldo_inicial for _ in range(n_jogadores)))
    )


def saldo_de(self, ji: int) -> int:
    return self.contas[ji]


def creditar_em(self, ji: int, valor: int) -> Banco:
    return self.set('contas', self.contas.set(ji, self.contas[ji] + valor))


def debitar_de(self, ji: int, valor: int) -> Banco:
    return self.set('contas', self.contas.set(ji, self.contas[ji] - valor))


def resta_um(self) -> bool:
    return len([c for c in self.contas if c >= 0]) == 1
