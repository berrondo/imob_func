def saldo_suficiente(self, valor):
    return self.saldo >= valor


def debita(self, valor):
    return self.set('saldo', self.saldo - valor)


def credita(self, valor):
    return self.set('saldo', self.saldo + valor)

