from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EventoJogo:
    tipo: str  # 'compra' ou 'aluguel' ou ''

    contador: int
    turno: int
    rodada: int

    saldos: list[int]
    cartorio: list[tuple[int, int]]
    j: object # Jogador
    p: object # Propriedade

    valor: int
    banco: str | None = None


@dataclass
class Relatorio:
    inicio: datetime = field(default_factory=datetime.now)
    eventos: list[EventoJogo] = field(default_factory=list)
    _saldos: dict[str, float] = field(default_factory=dict)
    _propriedades: dict[int, str] = field(default_factory=dict)

    def registrar_evento(self, jogo, tipo: str) -> None:
        """Registra um evento baseado no estado atual do jogo."""

        # Registra saldos
        # self._saldos[jogo.j.nome] = jogo.j.saldo

        valor = jogo.p.preco if tipo == 'COMPRA' else jogo.p.aluguel if tipo == 'ALUGUEL' else 0

        evento = EventoJogo(
            tipo=tipo,

            contador=jogo.rodadas.contador,
            turno=jogo.rodadas.turno,
            rodada=jogo.rodadas.rodadas,

            # saldos=[j.saldo for j in jogo.tabuleiro.jogadores],
            saldos=jogo.banco_.contas,
            cartorio=list(jogo.registro.compras),
            j=jogo.j,
            p=jogo.p,

            valor=valor,
            banco=jogo.banco_,
        )

        self.eventos.append(evento)

    def gerar_relatorio(self, msg="") -> str:
        """Gera um relatório textual dos eventos do jogo."""
        linhas = [
            f"=== RELATÓRIO DO JOGO: {msg}",
            f"Início: {self.inicio.strftime('%Y-%m-%d %H:%M:%S')}",
            "\nEVENTOS:",
        ]

        for e in self.eventos:
            desc = f"{e.contador:<5}{e.rodada:>4d}{e.turno:>2d}{e.j.i:>2d} " # {e.j:<10}"
            if e.tipo == 'COMPRA':
                desc += (
                    f"_C_ p{e.p.i:<3} $ {e.valor}"
                    f"{str(list(e.banco.contas)):>24}"
                    # f"{str(e.saldos):>24}"
                    f"  {str(e.cartorio)}"
                )
            elif e.tipo == 'ALUGUEL':
                desc += (
                    f"_a_ p{e.p.i:<3} $ {e.valor}"
                    f"{str(list(e.banco.contas)):>25}"
                    # f"{str(e.saldos):>24}"
                    # f" -> {str(e.p.proprietario) if e.p else "alugou de quem?":<10}" #$ {e.p.proprietario.saldo}"
                    f"  {str(e.cartorio)}"
                )
            elif e.tipo == 'DESPEJO':
                desc += (
                    f"_D_"
                    f"{str(list(e.banco.contas)):>34}"
                    # f"{str(e.saldos):>24}"
                    f"  {str(e.cartorio)}"
                )
            else:
                desc += (
                    # f"$ {e.valor} -> {e.p.proprietario.nome if e.p else "sem proprietário":<10}" # $ {e.p.proprietario.saldo}"
                    f"{str(list(e.banco.contas)):>37}"
                    # f"{str(e.saldos):>24}"
                    f"  {str(e.cartorio)}"
                )
            linhas.append(desc)

        # linhas.extend([
        #     "\nSALDOS FINAIS:",
        #     *[f"{j:<10}: $ {saldo}" for j, saldo in self._saldos.items()],
        #     "\nPROPRIEDADES:",
        #     *[f"p{pid:<3}: {prop}" for pid, prop in self._propriedades.items()]
        # ])

        return "\n".join(linhas)


# Singleton para usar em todo o jogo
relatorio_atual = Relatorio()


def registrar(jogo, tipo: str):
    """Função helper para registrar eventos do jogo."""
    relatorio_atual.registrar_evento(jogo, tipo)
    return jogo  # Retorna o jogo sem modificação para manter a composição funcional
