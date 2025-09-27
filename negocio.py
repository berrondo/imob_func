import jogador
import propriedade
import estrategia


def comprar(j, p, jp):
    if jogador.eh_saldo_suficiente(j, p.preco) \
        and estrategia.mandar_comprar(j, p):
            j2 = jogador.debitar(j, p.preco)
            p2 = propriedade.apropriar(p, j2)
            return j2, p2, jp

    return j, p, jp


def alugar(j, p, jp):
    if jogador.eh_saldo_suficiente(j, p.aluguel):
        j2 = jogador.debitar(j, p.aluguel)
        jp2 = jogador.creditar(p.proprietario, p.aluguel)
        # proprietario (jp2) eh um novo objeto,
        # entao precisamos atualizar a proprieade com ele:
        p2 = propriedade.apropriar(p, jp2)
        return j2, p2, jp2

    return j, p, jp


def comprar_ou_alugar(j, p, jp):
    if propriedade.eh_sem_proprietario(p):
        return comprar(j, p, jp)

    else:
        return alugar(j, p, jp)
