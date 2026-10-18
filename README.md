<p align="center">
  <a href="https://www.gustavofurtado.com/gender-guesser-br/"><img src="https://www.gustavofurtado.com/assets/img/projects/gender-guesser-br.png" alt="gender-guesser-br" width="640"></a>
</p>

<p align="center">
  <b>Adivinhe o gênero de um nome próprio com os dados do Censo do IBGE.</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/gender-guesser-br/"><img src="https://img.shields.io/pypi/v/gender-guesser-br" alt="PyPI"></a>
  <a href="https://pypi.org/project/gender-guesser-br/"><img src="https://img.shields.io/pypi/pyversions/gender-guesser-br" alt="Versões do Python"></a>
  <a href="https://pepy.tech/projects/gender-guesser-br"><img src="https://static.pepy.tech/badge/gender-guesser-br/month" alt="Downloads"></a>
  <a href="https://github.com/GusFurtado/gender-guesser-br/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/gender-guesser-br" alt="Licença"></a>
</p>

<p align="center">
  <b><a href="https://www.gustavofurtado.com/gender-guesser-br/">Documentação</a></b>
</p>

Versão brasileira do pacote Python para adivinhar o gênero de um nome próprio. Os dados vêm da
API de nomes do IBGE, por meio do [DadosAbertosBrasil](https://www.gustavofurtado.com/DadosAbertosBrasil/).

## Instalação

```sh
pip install gender-guesser-br
```

## Principais recursos

- **`Genero(nome)()`**: previsão entre `feminino`, `masculino`, `provavelmente_*`, `ambos` e `desconhecido`.
- **`Genero(nome, uf=...)`**: previsão com os dados de uma UF, pela sigla ou pelo código IBGE.
- **`corte_ambos` e `corte_maioria`**: ajuste dos limites de cada previsão.
- **`.f` e `.m`**: os números brutos do IBGE, com o total e a proporção de cada gênero.

Veja os [primeiros passos](https://www.gustavofurtado.com/gender-guesser-br/primeiros-passos/) e a
[referência](https://www.gustavofurtado.com/gender-guesser-br/referencia/).
