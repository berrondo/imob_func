import random


def impulsivo(j, p):
    return True


def exigente(saldo, p):
    return p.aluguel > 50


def cauteloso(saldo, p):
    return (saldo - p.preco) >= 80


def aleatorio(saldo, p):
    return random.choice([True, False])


estrategias = [impulsivo, exigente, cauteloso, aleatorio]
