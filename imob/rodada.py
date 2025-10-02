from pyrsistent import m, v


def criar_rodada(n: int):
    indices = v(*range(n))
    return m(
        indices=indices,
        tamanho=len(indices),
        da_vez=0,
        rodadas=0,
        removidos=v(),
    )


def proximo(r):
    nova_volta, nova_posicao = divmod(r.da_vez + 1, r.tamanho)
    return r.set('da_vez', nova_posicao).set('rodadas', nova_volta)


def remover(r, n):
    if n == r.da_vez:
        r = proximo(r)  # sera que o numero de rodadas fica correto depois da remocao?
    r2 = r.set('indices', r.indices.remove(n)).set('tamanho', r.tamanho - 1)
    return r2   # nao deveria remover quando restasse apenas 1!
