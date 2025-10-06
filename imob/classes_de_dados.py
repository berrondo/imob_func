
from dataclasses import dataclass

from imob import banco, cartorio


@dataclass
class JRegistro:
    cartorio: cartorio.Cartorio | None
    banco: banco.Banco | None
