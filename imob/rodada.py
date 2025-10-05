from pyrsistent import PClass, field, pvector_field, v


class Rodada(PClass):
    turno = field(type=int, initial=-1, mandatory=True)
    indices = pvector_field(int)
    tamanho = field(type=int)
    rodadas = field(type=int, initial=0)
    removidos = field(initial=v())


def criar_rodada(n: int):
    indices = v(*range(n))
    return Rodada(
        indices=indices,
        tamanho=len(indices),
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
