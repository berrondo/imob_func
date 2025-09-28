from pyrsistent import m


def criar_propriedade(preco, aluguel, proprietario=None):
    return m(preco=preco, aluguel=aluguel, proprietario=proprietario)


def eh_sem_proprietario(self):
    return self.proprietario is None


def apropriar(self, jogador):
    return self.set('proprietario', jogador)
