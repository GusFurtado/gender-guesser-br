# Primeiros passos

## Fazendo previsões

Crie uma instância de `Genero` com o nome próprio e chame o objeto para obter a previsão.

```python
>>> from gender_guesser_br import Genero

>>> nome = Genero("gustavo")
>>> nome()
'masculino'
```

## Previsões por UF

O argumento `uf` faz a previsão com os dados de uma unidade federativa, o que pode aumentar a
precisão. "Darci" é um nome que pode receber qualquer classificação, dependendo da UF:

```python
>>> Genero(nome="darci", uf="rs")()
'masculino'

>>> Genero(nome="darci", uf="sc")()
'provavelmente_masculino'

>>> Genero(nome="darci", uf="sp")()
'ambos'

>>> Genero(nome="darci", uf="ac")()
'feminino'

>>> Genero(nome="darci", uf="rr")()
'desconhecido'
```

`nome` e `uf` não diferenciam maiúsculas de minúsculas. A UF pode ser a sigla de duas letras ou o
código IBGE de dois dígitos; a lista completa de códigos sai do DadosAbertosBrasil:

```python
>>> from DadosAbertosBrasil import ibge
>>> ibge.localidades(nivel="estados")
```

## Refinando os resultados

Os argumentos `corte_ambos` e `corte_maioria` definem a partir de que proporção o nome é
considerado de um gênero só, e a partir de que proporção há certeza sobre o gênero.

```python
>>> ariel = Genero("Ariel", uf="RJ")
>>> ariel(corte_ambos=0.8, corte_maioria=0.9)
'ambos'

>>> ariel(corte_ambos=0.6, corte_maioria=0.8)
'provavelmente_masculino'

>>> ariel(corte_ambos=0.6, corte_maioria=0.7)
'masculino'
```

Os dois cortes devem estar entre 0,5 e 1,0, e `corte_maioria` deve ser maior que `corte_ambos`;
caso contrário, o pacote levanta `GenderGuesserError`.

## Números brutos

As propriedades `f` e `m` dão acesso aos números do IBGE: o total de pessoas com aquele nome em
cada gênero (`absoluto`) e a proporção do gênero (`percentual`).

```python
>>> camila = Genero("Camila")
>>> camila.f
{'absoluto': 469851.0, 'percentual': 0.9964012147225733}

>>> camila.m
{'absoluto': 1697.0, 'percentual': 0.003598785277426688}
```
