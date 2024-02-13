# Gender Guesser Brasil
### [Powered by DadosAbertosBrasil](https://www.gustavofurtado.com/dab.html)

Versão brasileira do pacote Python para adivinhar o gênero de um nome próprio.

Este pacote utiliza o DadosAbertosBrasil para capturar informações do Censo Demográfico das APIs oficiais do IBGE e calcula a probabilidade de que determinado nome próprio seja feminino ou masculino.

## Instalação

```pip install gender-guesser-br```

## Fazendo previsões

Após importar o pacote, crie uma instância do objeto `Genero` usando o nome próprio como argumento. Por fim, utilize o método `__call__` para conferir a previsão.

```python
>>> from gender_guesser_br import Genero

>>> nome = Genero("gustavo")
>>> nome()
'masculino'
```

É possível utilizar o argumento `uf` para fazer uma previsão por unidade federativa, o que pode aumentar a precisão. Veja que "Darci" é um nome que pode receber qualquer classificação, dependendo da UF.

```python
>>> rs = Genero(nome="darci", uf="rs")
>>> rs()
'masculino'

>>> sc = Genero(nome="darci", uf="sc")
>>> sc()
'provavelmente_masculino'

>>> sp = Genero(nome="darci", uf="sp")
>>> sp()
'ambos'

>>> ac = Genero(nome="darci", uf="ac")
>>> ac()
'feminino'

>>> rr = Genero(nome="darci", uf="rr")
>>> rr()
'desconhecido'
```

Os argumentos `nome` e `uf` são case insensitive, então você pode usar letras maiúsculas e minúsculas como quiser, desde que uf seja a sigla de duas letras da UF ou o código IBGE de dois dígitos. Utilize a função `localidade` do DadosAbertosBrasil para obter uma lista completa dos códigos das UFs.

```python
>>> from DadosAbertosBrasil import ibge
>>> ibge.localidades(nivel="estados")
```

## Refinando resultados

Ao fazer a previsão, utilize os argumentos `corte_ambos` e `corte_maioria` para definir qual é a proporção mínima em que o objeto para a ter certeza de que o nome é de determinado gênero ou que é considerado de ambos os gêneros.

```python
>>> ariel = Genero("Ariel", uf="RJ")
>>> ariel(corte_ambos=0.8, corte_maioria=0.9)
'ambos'

>>> ariel(corte_ambos=0.6, corte_maioria=0.8)
'provavelmente_masculino'

>>> ariel(corte_ambos=0.6, corte_maioria=0.7)
'masculino'
```

Para ter ainda mais controle, utilize as propriedades `f` e `m` para obter acesso aos números brutos.

Essas propriedades são dicionários contendo o número total de habitantes do gênero correspondente que possuem aquele nome e a proporção do gênero.

```python
>>> camila = Genero("Camila")
>>> camila.f
{'absoluto': 469851, 'percentual': 0.9964012147225733}

>>> camila.m
{'absoluto': 1697, 'percentual': 0.003598785277426688}
```
