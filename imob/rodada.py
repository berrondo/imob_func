from pyrsistent import PClass, field, pvector_field, v


class Rodada(PClass):
    turno = field(type=int, initial=-1, mandatory=True)
    indices = pvector_field(int)
    tamanho = field(type=int)
    rodadas = field(type=int, initial=0)
    removidos = field(initial=v())
    contador = field(type=int, initial=0)


def criar_rodada(n: int):
    indices = v(*range(n))
    return Rodada(
        indices=indices,
        tamanho=len(indices),
    )


def jogando(self):
    return self.tamanho - len(self.removidos)


def proximo(self):
    volta, turno = divmod(self.turno + 1, jogando(self) or 1)  # evita div/0 TODO
    return self \
        .set('turno', self.indices[turno]) \
        .set('rodadas', self.rodadas + volta) \
        .set('contador', self.contador + 1)


def remover(self):
    return self.set('removidos', self.removidos.append(self.turno))


def resta_um(self):
    # len(self.rodadas.removidos) == 3
    return jogando(self) == 1
