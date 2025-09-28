import random


def impulsivo(j, p):
    return True


def exigente(j, p):
    return p.aluguel > 50


def cauteloso(j, p):
    return (j.saldo - p.preco) >= 80


def aleatorio(j, p):
    return random.choice([True, False])


def mandar_comprar(j, p):
    return j.estrategia(j, p)
