from pyrsistent import PRecord, field


class Jogador(PRecord):
    estrategia = field()
    saldo = field(type=int)
    nome = field(type=str)


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
