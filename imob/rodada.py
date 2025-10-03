from pyrsistent import m, v


def criar_rodada(n: int):
    indices = v(*range(n))
    return m(
        da_vez=-1,
        indices=indices,
        tamanho=len(indices),
        rodadas=0,
        removidos=v(),
    )


def jogando(self):
    return self.tamanho - len(self.removidos)


def proximo(self):
    volta, da_vez = divmod(self.da_vez + 1, jogando(self))
    self = (self
        .set('da_vez', self.indices[da_vez])
        .set('rodadas', self.rodadas + volta)
    )
    print("  '-> prox", list(self.removidos), self.rodadas, self.da_vez)
    return self


def remover(self, n):
    return self.set('removidos', self.removidos.append(n))
