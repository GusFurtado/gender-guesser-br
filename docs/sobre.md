# Sobre

## Licença

O gender-guesser-br é distribuído sob a
[licença MIT](https://github.com/GusFurtado/gender-guesser-br/blob/main/LICENSE).

## Créditos

Os dados vêm da [API de nomes do IBGE](https://servicodados.ibge.gov.br/api/docs/nomes?versao=2), com as
contagens do Censo Demográfico, consultada por meio do
[DadosAbertosBrasil](https://www.gustavofurtado.com/DadosAbertosBrasil/).

## Como contribuir

O projeto usa o [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/GusFurtado/gender-guesser-br
cd gender-guesser-br
uv sync
uv run pytest
uv run ruff check
```

Os testes consultam a API do IBGE, então precisam de acesso à rede. Esta documentação usa o
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) e o
[mkdocstrings](https://mkdocstrings.github.io/); para visualizá-la localmente, rode
`uv run --group docs mkdocs serve`.
