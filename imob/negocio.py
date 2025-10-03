from imob import jogador, propriedade


def comprar_ou_alugar(j, p):
    match (propriedade.tem_proprietario(p)):
        case True:
            return alugar(j, p)
        case False:
            return tentar_comprar(j, p)


def alugar(j, p):
    if not jogador.tem_saldo_suficiente(j, p.aluguel):
        # para tirar o jodador do jogo sem creditar o alguel ao proprietario
        # enquanto nao implementamos uma Invariant
        j2 = jogador.debitar(j, j.saldo)  # zera o saldo
        return j2, p  # nao tem saldo para pagar o aluguel
    j2 = jogador.debitar(j, p.aluguel)
    jp2 = jogador.creditar(p.proprietario, p.aluguel)
    p2 = propriedade.apropriar(p, jp2)  # mesmo proprietario, novo objeto.
    return j2, p2


def tentar_comprar(j, p):
    if jogador.tem_saldo_suficiente(j, p.preco) and estrategia_eh_comprar(j, p):
        return comprar(j, p)
    return j, p


def estrategia_eh_comprar(j, p):
    return j.estrategia(j, p)


def comprar(j, p):
    j2 = jogador.debitar(j, p.preco)
    return j2, propriedade.apropriar(p, j2)


