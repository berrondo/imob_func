from pyrsistent import m


def criar_jogador(estrategia, saldo):
    return m(estrategia=estrategia, saldo=saldo)


def tem_saldo(self, valor):
    return self.saldo >= valor


def debitar(self, valor):
    return self.set('saldo', self.saldo - valor)


def creditar(self, valor):
    return self.set('saldo', self.saldo + valor)
