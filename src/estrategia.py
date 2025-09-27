def impulsivo(j, p):
    return True


def exigente(j, p):
    return p.aluguel > 50


def mandar_comprar(j, p):
    return j.estrategia(j, p)
