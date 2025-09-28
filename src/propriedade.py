from pyrsistent import m


def criar_propriedade(preco, aluguel, proprietario=None):
    return m(preco=preco, aluguel=aluguel, proprietario=proprietario)


def tem_proprietario(self):
    return self.proprietario is not None


def apropriar(self, jogador):
    return self.set('proprietario', jogador)
