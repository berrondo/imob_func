from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EventoJogo:
    rodada: int
    turno: int
    jogador: str
    tipo: str  # 'compra' ou 'aluguel'
    propriedade_id: int
    valor: float
    proprietario: str | None = None


@dataclass
class Relatorio:
    inicio: datetime = field(default_factory=datetime.now)
    eventos: list[EventoJogo] = field(default_factory=list)
    _saldos: dict[str, float] = field(default_factory=dict)
    _propriedades: dict[int, str] = field(default_factory=dict)

    def registrar_evento(self, jogo) -> None:
        """Registra um evento baseado no estado atual do jogo."""
        if not hasattr(jogo, 'contador') or not jogo.j or not jogo.p:
            return

        # Registra saldos
        self._saldos[jogo.j.nome] = jogo.j.saldo

        # Determina o tipo de evento
        if jogo.p.proprietario is None:
            return  # Nada aconteceu nesta rodada

        # Se mudou o proprietário, é uma compra
        prop_id = id(jogo.p)
        atual_prop = self._propriedades.get(prop_id)
        if atual_prop != jogo.p.proprietario:
            self._propriedades[prop_id] = jogo.p.proprietario
            evento = EventoJogo(
                rodada=jogo.contador,
                turno=jogo.rodadas.turno,
                jogador=jogo.j.nome,
                tipo='compra',
                propriedade_id=prop_id,
                valor=jogo.p.preco
            )
        else:
            # Se não mudou o proprietário, é um aluguel
            evento = EventoJogo(
                rodada=jogo.contador,
                turno=jogo.rodadas.turno,
                jogador=jogo.j.nome,
                tipo='aluguel',
                propriedade_id=prop_id,
                valor=jogo.p.aluguel,
                proprietario=jogo.p.proprietario
            )

        self.eventos.append(evento)

    def gerar_relatorio(self) -> str:
        """Gera um relatório textual dos eventos do jogo."""
        linhas = [
            "=== RELATÓRIO DO JOGO ===",
            f"Início: {self.inicio.strftime('%Y-%m-%d %H:%M:%S')}",
            "\nEVENTOS:",
        ]

        for e in self.eventos:
            if e.tipo == 'compra':
                desc = (
                    f"Rodada {e.rodada}, Turno {e.turno}: "
                    f"{e.jogador} comprou propriedade {e.propriedade_id} por ${e.valor}"
                )
            else:
                desc = (
                    f"Rodada {e.rodada}, Turno {e.turno}: "
                    f"{e.jogador} alugou propriedade {e.propriedade_id} "
                    f"pagando ${e.valor} para {e.proprietario}"
                )
            linhas.append(desc)

        linhas.extend([
            "\nSALDOS FINAIS:",
            *[f"{jogador}: ${saldo}" for jogador, saldo in self._saldos.items()],
            "\nPROPRIEDADES:",
            *[f"Propriedade {pid}: {prop}" for pid, prop in self._propriedades.items()]
        ])

        return "\n".join(linhas)


# Singleton para usar em todo o jogo
relatorio_atual = Relatorio()


def registrar(jogo):
    """Função helper para registrar eventos do jogo."""
    relatorio_atual.registrar_evento(jogo)
    return jogo  # Retorna o jogo sem modificação para manter a composição funcional
