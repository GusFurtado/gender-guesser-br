from pytest import raises

from gender_guesser_br import Genero
from gender_guesser_br.errors import GenderGuesserError


def test_guesser():
    camila = Genero("Camila", uf=35)
    assert camila() == "feminino"


def test_resultado():
    gustavo = Genero("Gustavo", uf="SC")
    assert "absoluto" in gustavo.m
    assert "percentual" in gustavo.f


def test_cortes():
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


def test_erros():
    with raises(GenderGuesserError):
        charlotte = Genero("Charlotte")
        charlotte(corte_ambos=0.8, corte_maioria=1.2)

    with raises(GenderGuesserError):
        charlotte = Genero("Charlotte")
        charlotte(corte_ambos=0.4, corte_maioria=0.8)

    with raises(GenderGuesserError):
        charlotte = Genero("Charlotte")
        charlotte(corte_ambos=0.9, corte_maioria=0.8)
