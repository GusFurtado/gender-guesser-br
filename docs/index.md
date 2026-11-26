<p align="center">
  <img class="hero" src="https://www.gustavofurtado.com/assets/img/projects/gender-guesser-br.png" alt="gender-guesser-br" width="100%">
</p>

**Adivinhe o gênero de um nome próprio com os dados do Censo do IBGE.**

Versão brasileira do pacote Python para adivinhar o gênero de um nome próprio. O pacote consulta a
API de nomes do IBGE, com os dados do Censo Demográfico, por meio do
[DadosAbertosBrasil](https://www.gustavofurtado.com/DadosAbertosBrasil/), e calcula a proporção de
pessoas com aquele nome que são do sexo feminino ou masculino.

[![PyPI](https://img.shields.io/pypi/v/gender-guesser-br)](https://pypi.org/project/gender-guesser-br/)
[![Versões do Python](https://img.shields.io/pypi/pyversions/gender-guesser-br)](https://pypi.org/project/gender-guesser-br/)
[![Downloads](https://static.pepy.tech/badge/gender-guesser-br/month)](https://pepy.tech/projects/gender-guesser-br)
[![Licença](https://img.shields.io/pypi/l/gender-guesser-br)](sobre.md#licenca)

## Recursos

- **Dados oficiais**: as contagens de pessoas por nome e sexo do Censo do IBGE, consultadas na
  hora, sem listas de nomes embutidas no pacote.
- **Previsões por UF**: o mesmo nome pode ter respostas diferentes em cada estado.
- **Cortes ajustáveis**: você decide a partir de que proporção um nome é de um gênero só.
- **Números brutos**: o total de pessoas e a proporção de cada sexo, para quem quer fazer as
  próprias contas.
- **Entrada flexível**: nome e UF não diferenciam maiúsculas de minúsculas, e a UF
  aceita a sigla ou o código do IBGE.

## Exemplo

```python
>>> from gender_guesser_br import Genero
>>> Genero("gustavo")()
'masculino'

>>> Genero(nome="darci", uf="rs")()
'masculino'

>>> Genero(nome="darci", uf="ac")()
'feminino'
```

## Por onde começar

- [Instalação](instalacao.md): um `pip install`
- [Primeiros passos](primeiros-passos.md): previsões, previsões por UF, cortes e números brutos
- [Referência](referencia.md): a classe `Genero` e seus parâmetros
- [Sobre](sobre.md): licença, créditos e como contribuir

## Previsões possíveis

| Previsão | Quando |
|---|---|
| `feminino` / `masculino` | A proporção de um gênero passa de `corte_maioria` (padrão: 80%) |
| `provavelmente_feminino` / `provavelmente_masculino` | A proporção de um gênero fica entre `corte_ambos` (60%) e `corte_maioria` |
| `ambos` | Nenhum gênero passa de `corte_ambos` |
| `desconhecido` | O nome não aparece nos dados do IBGE |
