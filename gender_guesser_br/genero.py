"""
Módulo principal do gender-guesser-br.

Fornece a classe Genero para identificar o gênero de um nome próprio
com base nos dados do Censo IBGE (API DadosAbertosBrasil).
"""

from __future__ import annotations

from functools import lru_cache

from DadosAbertosBrasil import ibge

from ._ufs import UFS
from .errors import GenderGuesserError

# Valores padrão de corte
DEFAULT_CORTE_AMBOS: float = 0.6
DEFAULT_CORTE_MAIORIA: float = 0.8
LIMITE_MIN_CORTE: float = 0.5
LIMITE_MAX_CORTE: float = 1.0


@lru_cache(maxsize=256)
def _gender_freq(nome: str, sexo: str, uf: int | None = None) -> float:
    """
    Obtém a frequência de um nome por gênero na API do IBGE.

    Parameters
    ----------
    nome : str
        Nome próprio a ser consultado.
    sexo : str
        Gênero a ser consultado ("f" para feminino, "m" para masculino).
    uf : int, optional
        Código IBGE da Unidade Federativa.

    Returns
    -------
    float
        Frequência total do nome para o gênero especificado.
        Retorna 0.0 se o nome não for encontrado.

    """
    try:
        freq = ibge.nomes(nome, sexo=sexo, localidade=uf)
        return float(freq.squeeze().sum())

    except Exception:
        return 0.0


class Genero:
    """
    Identificador de gênero baseado em dados do IBGE.

    Utiliza o Censo Demográfico do IBGE para calcular a probabilidade
    de determinado nome próprio ser feminino ou masculino.

    Parameters
    ----------
    nome : str
        Nome próprio que se deseja conhecer o gênero.
    uf : int | str, optional
        Sigla ou código IBGE da Unidade Federativa.

    Properties
    ----------
    f : dict[str, float]
        Proporções do gênero feminino.
    m : dict[str, float]
        Proporções do gênero masculino.

    Methods
    -------
    __call__(corte_ambos: float = 0.6, corte_maioria: float = 0.8) -> str
        Retorna um texto com a previsão de gênero.

    Examples
    --------
    >>> nome = Genero("gustavo")
    >>> nome()
    'masculino'

    >>> rs = Genero(nome="darci", uf="rs")
    >>> rs()
    'masculino'

    """

    def __init__(self, nome: str, uf: int | str | None = None) -> None:
        """
        Inicializa o identificador de gênero.

        Parameters
        ----------
        nome : str
            Nome próprio que se deseja conhecer o gênero.
        uf : int | str, optional
            Sigla ou código IBGE da Unidade Federativa.

        Raises
        ------
        GenderGuesserError
            Se o nome for vazio ou inválido, ou se a UF for inválida.

        """
        if not isinstance(nome, str):
            raise GenderGuesserError(
                GenderGuesserError.MSG_NOME_DEVE_SER_STRING,
            )
        if not nome.strip():
            raise GenderGuesserError(GenderGuesserError.MSG_NOME_VAZIO)

        # Converte a sigla da UF em código IBGE
        if isinstance(uf, str):
            uf_upper = uf.upper().strip()
            if uf_upper not in UFS:
                msg = GenderGuesserError.MSG_UF_INVALIDA.format(uf)
                raise GenderGuesserError(msg)
            uf = UFS[uf_upper]

        self._nome = nome.strip()
        self._uf = uf
        self._f = _gender_freq(nome, sexo="f", uf=uf)
        self._m = _gender_freq(nome, sexo="m", uf=uf)

    def __call__(
        self,
        corte_ambos: float = DEFAULT_CORTE_AMBOS,
        corte_maioria: float = DEFAULT_CORTE_MAIORIA,
    ) -> str:
        """
        Retorna um texto com a previsão de gênero.

        Parameters
        ----------
        corte_ambos : float, optional
            A partir de que proporção o nome é considerado de um gênero só
            ao invés de ambos. Deve estar entre 0.5 e 1.0.
            (padrão: 0.6)
        corte_maioria : float, optional
            A partir de que proporção temos certeza de que um nome pertence
            a tal gênero. Deve estar entre 0.5 e 1.0 e maior que corte_ambos.
            (padrão: 0.8)

        Returns
        -------
        str
            Uma das seis possíveis previsões, baseado nos valores de corte:
            - "desconhecido"
            - "feminino"
            - "provavelmente_feminino"
            - "masculino"
            - "provavelmente_masculino"
            - "ambos"

        Raises
        ------
        GenderGuesserError
            Se os valores de corte forem inválidos.

        """
        if not LIMITE_MIN_CORTE <= corte_ambos <= LIMITE_MAX_CORTE:
            raise GenderGuesserError(
                GenderGuesserError.MSG_CORTE_AMBOS_INVALIDO,
            )
        if not LIMITE_MIN_CORTE <= corte_maioria <= LIMITE_MAX_CORTE:
            raise GenderGuesserError(
                GenderGuesserError.MSG_CORTE_MAIORIA_INVALIDO,
            )
        if corte_ambos >= corte_maioria:
            raise GenderGuesserError(
                GenderGuesserError.MSG_CORTE_MAIORIA_MENOR,
            )

        if not (self._f + self._m):
            return "desconhecido"
        elif self.f["percentual"] > corte_maioria:
            return "feminino"
        elif self.f["percentual"] > corte_ambos:
            return "provavelmente_feminino"
        elif self.m["percentual"] > corte_maioria:
            return "masculino"
        elif self.m["percentual"] > corte_ambos:
            return "provavelmente_masculino"
        else:
            return "ambos"

    @property
    def f(self) -> dict[str, float]:
        """
        Proporções do gênero feminino.

        Returns
        -------
        dict[str, float]
            Dicionário com 'absoluto' (contagem total) e 'percentual'
            (proporção entre 0 e 1).

        """
        p = 0.0 if not self._f + self._m else self._f / (self._f + self._m)
        return {
            "absoluto": self._f,
            "percentual": p,
        }

    @property
    def m(self) -> dict[str, float]:
        """
        Proporções do gênero masculino.

        Returns
        -------
        dict[str, float]
            Dicionário com 'absoluto' (contagem total) e 'percentual'
            (proporção entre 0 e 1).

        """
        p = 0.0 if not self._f + self._m else self._m / (self._f + self._m)
        return {
            "absoluto": self._m,
            "percentual": p,
        }
