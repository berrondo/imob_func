
from dataclasses import dataclass

from imob import banco, cartorio, jogador, propriedade


@dataclass
class JJogador:
    j: jogador.Jogador
    ji: int


@dataclass
class JPropriedade:
    p: propriedade.Propriedade
    pi: int


@dataclass
class JRegistro:
    cartorio: cartorio.Cartorio | None
    banco: banco.Banco | None
