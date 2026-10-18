# gender-guesser-br

**Adivinhe o gênero de um nome próprio com os dados do Censo do IBGE.**

[![PyPI](https://img.shields.io/pypi/v/gender-guesser-br)](https://pypi.org/project/gender-guesser-br/)
[![Versões do Python](https://img.shields.io/pypi/pyversions/gender-guesser-br)](https://pypi.org/project/gender-guesser-br/)
[![Downloads](https://static.pepy.tech/badge/gender-guesser-br/month)](https://pepy.tech/projects/gender-guesser-br)
[![Licença](https://img.shields.io/pypi/l/gender-guesser-br)](https://github.com/GusFurtado/gender-guesser-br/blob/main/LICENSE)

Versão brasileira do pacote Python para adivinhar o gênero de um nome próprio. O pacote consulta a
API de nomes do IBGE, com os dados do Censo Demográfico, por meio do
[DadosAbertosBrasil](https://www.gustavofurtado.com/DadosAbertosBrasil/), e calcula a proporção de
pessoas com aquele nome que são do sexo feminino ou masculino.

```python
>>> from gender_guesser_br import Genero
>>> Genero("gustavo")()
'masculino'
```

## Por onde começar

- [Instalação](instalacao.md): um `pip install`
- [Primeiros passos](primeiros-passos.md): previsões, previsões por UF, cortes e números brutos
- [Referência](referencia.md): a classe `Genero` e seus parâmetros

## Previsões possíveis

| Previsão | Quando |
|---|---|
| `feminino` / `masculino` | A proporção de um gênero passa de `corte_maioria` (padrão: 80%) |
| `provavelmente_feminino` / `provavelmente_masculino` | A proporção de um gênero fica entre `corte_ambos` (60%) e `corte_maioria` |
| `ambos` | Nenhum gênero passa de `corte_ambos` |
| `desconhecido` | O nome não aparece nos dados do IBGE |
