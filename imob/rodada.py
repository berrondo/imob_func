from pyrsistent import m, v


def criar_rodada(n: int):
    indices = v(*range(n))
    return m(
        da_vez=0,
        indices=indices,
        tamanho=len(indices),
        rodadas=0,
        removidos=v(),   # TODO
    )


def proximo(r):
    numero_de_rodadas, da_vez = divmod(r.da_vez + 1, r.tamanho)
    return r.set('da_vez', da_vez).set('rodadas', numero_de_rodadas)


def remover(r, n):
    if n == r.da_vez:   # nao deveria remover quando restasse apenas 1!
        r = proximo(r)  # sera que o numero de rodadas fica correto depois da remocao?
    return r.set('indices', r.indices.remove(n)).set('tamanho', r.tamanho - 1)
