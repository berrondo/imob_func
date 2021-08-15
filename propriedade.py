def desapropriada(self):
    return self.proprietario is None


def apossada(self, jogador):
    return self.set('proprietario', jogador)
