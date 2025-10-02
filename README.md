# 🎲 Monopoly Funcional em Python

## 🌟 Inspiração

Tudo começou com os vídeos do Rich Hickey sobre Clojure. Como um desenvolvedor Python, me vi fascinado pelo paradigma funcional, mas ao mesmo tempo desafiado pelos seus conceitos fundamentais:

- 🔒 Imutabilidade
- 🎯 Funções puras
- 🚫 Ausência de efeitos colaterais

O contraste com a programação orientada a objetos que eu estava acostumado era enorme. A forma de pensar era completamente diferente.

## 💡 A Ideia

Em vez de mergulhar direto em Clojure, com sua sintaxe e ambiente totalmente novos, decidi fazer uma abordagem gradual:

1. Manter o conforto da sintaxe Python
2. Adotar princípios funcionais
3. Usar estruturas de dados imutáveis
4. Focar em funções puras

## 🛠 A Implementação

Descobri a biblioteca `pyrsistent`, que traz estruturas de dados imutáveis para Python. Com ela em mãos, precisava de um projeto para experimentar.

Por coincidência, estávamos organizando uma sessão de mob programming online para desenvolver um desafio clássico de orientação a objetos: o jogo Monopoly. Vi aí a oportunidade perfeita para tentar uma abordagem diferente.

Comecei da maneira mais simples possível, utilizando as estruturas `m` e `v` do `pyrsistent` para criar uma versão puramente funcional do jogo.

## 🎮 O Resultado

O resultado é este projeto: uma implementação do Monopoly seguindo princípios funcionais, mas mantendo a familiaridade do Python. É uma demonstração interessante de como podemos adotar conceitos de programação funcional mesmo em linguagens que não são puramente funcionais.

## 🔍 O Que Aprendi

- Como pensar em termos de transformações de dados em vez de mutações de estado
- O valor da imutabilidade para raciocinar sobre o código
- Como estruturar um programa sem efeitos colaterais
- Que é possível adotar princípios funcionais mesmo em Python

## 🚀 Próximos Passos

Esse projeto continua evoluindo conforme exploro mais conceitos funcionais e descubro novas formas de aplicá-los em Python.
