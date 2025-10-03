from pyrsistent import m, v


def criar_rodada(n: int):
    indices = v(*range(n))
    return m(
        turno=-1,
        indices=indices,
        tamanho=len(indices),
        rodadas=0,
        removidos=v(),
    )


def jogando(self):
    return self.tamanho - len(self.removidos)


def proximo(self):
    volta, turno = divmod(self.turno + 1, jogando(self))
    return self \
        .set('turno', self.indices[turno]) \
        .set('rodadas', self.rodadas + volta)


def remover(self, n):
    return self.set('removidos', self.removidos.append(n))
