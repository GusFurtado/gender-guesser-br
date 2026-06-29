"""Testes automatizados para o pacote gender-guesser-br."""

import pytest

from gender_guesser_br import Genero
from gender_guesser_br.errors import GenderGuesserError


def test_guesser() -> None:
    """Testa se o guesser retorna o genêro feminino para Camila em SP."""
    camila = Genero("Camila", uf=35)
    assert camila() == "feminino"


def test_resultado() -> None:
    """Testa se as propriedades f e m possuem as chaves esperadas."""
    gustavo = Genero("Gustavo", uf="SC")
    assert "absoluto" in gustavo.m
    assert "percentual" in gustavo.f


def test_cortes() -> None:
    """Testa diferentes valores de corte e seus resultados."""
    edir = Genero("Edir")
    assert edir() == "ambos"
    assert edir(corte_ambos=0.5, corte_maioria=0.6) == "provavelmente_feminino"

    darci = Genero("Darci")
    assert darci() == "provavelmente_masculino"
    assert darci(corte_ambos=0.5, corte_maioria=0.6) == "masculino"

    geralt = Genero("Geralt")
    assert geralt() == "desconhecido"
    assert geralt.f == {"absoluto": 0, "percentual": 0}
    assert geralt.m == geralt.f


def test_erros() -> None:
    """Testa se exceções são levantadas para valores de corte inválidos."""
    charlotte = Genero("Charlotte")

    with pytest.raises(GenderGuesserError):
        charlotte(corte_ambos=0.8, corte_maioria=1.2)

    with pytest.raises(GenderGuesserError):
        charlotte(corte_ambos=0.4, corte_maioria=0.8)

    with pytest.raises(GenderGuesserError):
        charlotte(corte_ambos=0.9, corte_maioria=0.8)


def test_uf_invalida() -> None:
    """Testa que uma UF inválida levanta GenderGuesserError."""
    with pytest.raises(GenderGuesserError):
        Genero("João", uf="XX")


def test_nome_vazio() -> None:
    """Testa que um nome vazio levanta GenderGuesserError."""
    with pytest.raises(GenderGuesserError):
        Genero("")


def test_nome_nao_string() -> None:
    """Testa que um nome que não é string levanta GenderGuesserError."""
    with pytest.raises(GenderGuesserError):
        Genero(123)


def test_case_insensitive() -> None:
    """Testa que nome e UF são case insensitive."""
    nome1 = Genero("GUSTAVO", uf="sc")
    nome2 = Genero("gustavo", uf="SC")
    assert nome1() == nome2()


def test_uf_com_espacos() -> None:
    """Testa que UF com espaços é tratada corretamente."""
    nome = Genero("Darci", uf=" RS ")
    assert nome() == "masculino"


def test_nome_com_espacos() -> None:
    """Testa que nome com espaços extras é tratado corretamente."""
    nome = Genero("  Gustavo  ")
    assert nome() == "masculino"


def test_corte_ambos_limite() -> None:
    """Testa valores limites para corte_ambos."""
    nome = Genero("Ariel")

    resultado = nome(corte_ambos=0.5, corte_maioria=0.6)
    assert resultado in [
        "feminino",
        "masculino",
        "ambos",
        "provavelmente_feminino",
        "provavelmente_masculino",
    ]

    with pytest.raises(GenderGuesserError):
        nome(corte_ambos=0.49, corte_maioria=0.6)


def test_corte_maioria_limite() -> None:
    """Testa valores limites para corte_maioria."""
    nome = Genero("Ariel")

    resultado = nome(corte_ambos=0.5, corte_maioria=1.0)
    assert resultado in [
        "feminino",
        "masculino",
        "ambos",
        "provavelmente_feminino",
        "provavelmente_masculino",
    ]

    with pytest.raises(GenderGuesserError):
        nome(corte_ambos=0.5, corte_maioria=1.1)


def test_cortes_iguais() -> None:
    """Testa que corte_ambos >= corte_maioria levanta erro."""
    nome = Genero("Ariel")
    with pytest.raises(GenderGuesserError):
        nome(corte_ambos=0.7, corte_maioria=0.7)


def test_propriedades_f_m() -> None:
    """Testa que as propriedades f e m retornam a estrutura correta."""
    nome = Genero("Maria")
    assert isinstance(nome.f, dict)
    assert "absoluto" in nome.f
    assert "percentual" in nome.f
    assert isinstance(nome.f["absoluto"], (int, float))
    assert isinstance(nome.f["percentual"], float)
    assert 0 <= nome.f["percentual"] <= 1

    assert isinstance(nome.m, dict)
    assert "absoluto" in nome.m
    assert "percentual" in nome.m


def test_sem_uf() -> None:
    """Testa que a previsão funciona sem UF."""
    nome = Genero("Ana")
    assert nome() == "feminino"


def test_com_uf_int() -> None:
    """Testa que a UF pode ser passada como inteiro (código IBGE)."""
    nome = Genero("Ana", uf=35)
    assert nome() == "feminino"


def test_com_uf_str() -> None:
    """Testa que a UF pode ser passada como string (sigla)."""
    nome = Genero("Ana", uf="SP")
    assert nome() == "feminino"
