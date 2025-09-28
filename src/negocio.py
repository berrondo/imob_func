from src import jogador, propriedade


def _estrategia_eh_comprar(j, p):
    return j.estrategia(j, p)


def _comprar(j, p):
    if jogador.tem_saldo(j, p.preco) and _estrategia_eh_comprar(j, p):
        j2 = jogador.debitar(j, p.preco)
        p2 = propriedade.apropriar(p, j2)
        return j2, p2
    return j, p


def _alugar(j, p):
    if jogador.tem_saldo(j, p.aluguel):
        j2 = jogador.debitar(j, p.aluguel)
        jp2 = jogador.creditar(p.proprietario, p.aluguel)
        p2 = propriedade.apropriar(p, jp2)  # mesmo proprietario, novo objeto.
        return j2, p2
    return j, p


def comprar_ou_alugar(j, p):
    if not propriedade.tem_proprietario(p):
        return _comprar(j, p)
    else:
        return _alugar(j, p)
