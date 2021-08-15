def saldo_suficiente(j, valor):
    return j.saldo >= valor


def debita(j, valor):
    return j.set('saldo', j.saldo - valor)


def apropria(j, p):
    return p.set('proprietario', j)
