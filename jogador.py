from pyrsistent import m


def eh_saldo_suficiente(self, valor):
    return self.saldo >= valor


def debitar(self, valor):
    return self.set('saldo', self.saldo - valor)


def creditar(self, valor):
    return self.set('saldo', self.saldo + valor)


def criar_jogador(estrategia, saldo):
    return m(estrategia=estrategia, saldo=saldo)
