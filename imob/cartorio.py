from pyrsistent import CheckedPSet, PClass, field, s


class Compras(CheckedPSet):
    __type__ = tuple  # (j compra p)


class Cartorio(PClass):
    compras = field(Compras)  # (j compra p)


def criar_cartorio() -> Cartorio:
    return Cartorio(
        compras=s(),  # (j compra p)
    )


def registrar_compra(self, ji: int, pi: int) -> Cartorio:
    return self.set('compras', self.compras.add((ji, pi)))


def obter_proprietario(self, pi: int) -> int | None:
    for (ji, p) in self.compras:
        if p == pi:
            return ji
    return None

def obter_propriedades(self, ji: int) -> list[int] | None:
    ps = [p for (j, p) in self.compras if j == ji]
    return ps if ps else []


def desapropriar(self, ji: int) -> Cartorio:
    compras = s(*((j, p) for (j, p) in self.compras if j != ji))
    return self.set('compras', compras)
