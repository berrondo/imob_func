from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EventoJogo:
    tipo: str  # 'compra' ou 'aluguel' ou ''

    contador: int
    turno: int
    rodada: int

    jj: object # JJogador
    pp: object # JPropriedade

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
        self._saldos[jogo.jj.j.nome] = jogo.jj.j.saldo

        evento = EventoJogo(
            tipo=tipo,

            contador=jogo.contador,
            turno=jogo.rodadas.turno,
            rodada=jogo.rodadas.rodadas,


            jj=jogo.jj,
            pp=jogo.pp,

            valor=jogo.pp.p.preco,
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
            desc = f"{e.contador:<5}{e.rodada:>4d}{e.turno:>2d}{e.jj.ji:>2d} {e.jj.j.nome:<10}"
            if e.tipo == 'COMPRA':
                desc += (
                    f"comprou p{e.pp.pi:<3} $ {e.valor}"
                    f"{str(list(e.banco.contas)):>42}"
                )
            elif e.tipo == 'ALUGUEL':
                desc += (
                    f"ALUGOU  p{e.pp.pi:<3}"
                    f"$ {e.valor} -> {e.pp.p.proprietario.nome if e.pp else "alugou de quem?":<10} $ {e.pp.p.proprietario.saldo}"
                    f"{str(list(e.banco.contas)):>24}"
                )
            else:
                desc += (
                    # f"$ {e.valor} -> {e.pp.p.proprietario.nome if e.pp else "sem proprietário":<10}" # $ {e.pp.p.proprietario.saldo}"
                    f"{str(list(e.banco.contas)):>60}"
                )
            linhas.append(desc)

        linhas.extend([
            "\nSALDOS FINAIS:",
            *[f"{j:<10}: $ {saldo}" for j, saldo in self._saldos.items()],
            "\nPROPRIEDADES:",
            *[f"p{pid:<3}: {prop}" for pid, prop in self._propriedades.items()]
        ])

        return "\n".join(linhas)


# Singleton para usar em todo o jogo
relatorio_atual = Relatorio()


def registrar(jogo, tipo: str):
    """Função helper para registrar eventos do jogo."""
    relatorio_atual.registrar_evento(jogo, tipo)
    return jogo  # Retorna o jogo sem modificação para manter a composição funcional
