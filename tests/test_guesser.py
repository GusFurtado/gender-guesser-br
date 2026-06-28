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


def test_uf_invalida():
    """Test that invalid UF raises GenderGuesserError."""
    with raises(GenderGuesserError):
        Genero("João", uf="XX")


def test_nome_vazio():
    """Test that empty name raises GenderGuesserError."""
    with raises(GenderGuesserError):
        Genero("")


def test_nome_nao_string():
    """Test that non-string name raises GenderGuesserError."""
    with raises(GenderGuesserError):
        Genero(123)


def test_case_insensitive():
    """Test that nome and uf are case insensitive."""
    nome1 = Genero("GUSTAVO", uf="sc")
    nome2 = Genero("gustavo", uf="SC")
    assert nome1() == nome2()


def test_uf_com_espacos():
    """Test that UF with spaces is handled correctly."""
    nome = Genero("Darci", uf=" RS ")
    assert nome() == "masculino"


def test_nome_com_espacos():
    """Test that nome with leading/trailing spaces is handled."""
    nome = Genero("  Gustavo  ")
    assert nome() == "masculino"


def test_corte_ambos_limite():
    """Test corte_ambos boundary values."""
    nome = Genero("Ariel")
    # corte_ambos = 0.5 should be valid
    resultado = nome(corte_ambos=0.5, corte_maioria=0.6)
    assert resultado in [
        "feminino",
        "masculino",
        "ambos",
        "provavelmente_feminino",
        "provavelmente_masculino",
    ]

    # corte_ambos = 0.49 should raise error
    with raises(GenderGuesserError):
        nome(corte_ambos=0.49, corte_maioria=0.6)


def test_corte_maioria_limite():
    """Test corte_maioria boundary values."""
    nome = Genero("Ariel")
    # corte_maioria = 1.0 should be valid
    resultado = nome(corte_ambos=0.5, corte_maioria=1.0)
    assert resultado in [
        "feminino",
        "masculino",
        "ambos",
        "provavelmente_feminino",
        "provavelmente_masculino",
    ]

    # corte_maioria = 1.1 should raise error
    with raises(GenderGuesserError):
        nome(corte_ambos=0.5, corte_maioria=1.1)


def test_cortes_iguais():
    """Test that corte_ambos >= corte_maioria raises error."""
    nome = Genero("Ariel")
    with raises(GenderGuesserError):
        nome(corte_ambos=0.7, corte_maioria=0.7)


def test_propriedades_f_m():
    """Test that f and m properties return correct structure."""
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


def test_sem_uf():
    """Test that predictions work without UF."""
    nome = Genero("Ana")
    assert nome() == "feminino"


def test_com_uf_int():
    """Test that UF can be passed as integer."""
    nome = Genero("Ana", uf=35)  # SP
    assert nome() == "feminino"


def test_com_uf_str():
    """Test that UF can be passed as string."""
    nome = Genero("Ana", uf="SP")
    assert nome() == "feminino"
