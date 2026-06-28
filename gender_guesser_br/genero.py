from functools import lru_cache
from typing import Dict, Literal, Optional, Union

from DadosAbertosBrasil import ibge

from ._ufs import UFS
from .errors import GenderGuesserError

# Valores padrões de threshold
DEFAULT_CORTE_AMBOS: float = 0.6
DEFAULT_CORTE_MAIORIA: float = 0.8


class Genero:
    """Identificador de Gênero baseado em dados do IBGE.

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

    def __init__(self, nome: str, uf: Optional[Union[int, str]] = None):
        """Inicializa o identificador de gênero.

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
        # Validate nome
        if not isinstance(nome, str):
            raise GenderGuesserError("O parâmetro 'nome' deve ser uma string.")
        if not nome.strip():
            raise GenderGuesserError("O parâmetro 'nome' não pode ser vazio.")

        # Converte a sigla da UF em código IBGE
        if isinstance(uf, str):
            uf_upper = uf.upper().strip()
            if uf_upper not in UFS:
                raise GenderGuesserError(
                    f"UF inválida: '{uf}'. Use a sigla de duas letras ou o código IBGE da UF."
                )
            uf = UFS[uf_upper]

        self._nome = nome.strip()
        self._uf = uf
        self._f = self._gender_freq(nome, sexo="f", uf=uf)
        self._m = self._gender_freq(nome, sexo="m", uf=uf)

    def __call__(
        self,
        corte_ambos: float = DEFAULT_CORTE_AMBOS,
        corte_maioria: float = DEFAULT_CORTE_MAIORIA,
    ) -> str:
        """Retorna um texto com a previsão de gênero.

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
        # Validar argumentos
        if not 0.5 <= corte_ambos <= 1.0:
            raise GenderGuesserError("Insira um valor entre 0.5 e 1.0 para `corte_ambos`.")
        if not 0.5 <= corte_maioria <= 1.0:
            raise GenderGuesserError("Insira um valor entre 0.5 e 1.0 para `corte_maioria`.")
        if corte_ambos >= corte_maioria:
            raise GenderGuesserError(
                "O valor de `corte_maioria` deve ser maior que o valor de `corte_ambos`."
            )

        # Possíveis resultados
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
    def f(self) -> Dict[str, float]:
        """Proporções do gênero feminino.

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
    def m(self) -> Dict[str, float]:
        """Proporções do gênero masculino.

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

    @lru_cache(maxsize=128)
    def _gender_freq(
        self,
        nome: str,
        sexo: Literal["f", "m"],
        uf: Optional[int] = None,
    ) -> float:
        """Obtém a frequência de um nome por gênero na API do IBGE.

        Parameters
        ----------
        nome : str
            Nome próprio a ser consultado.
        sexo : Literal["f", "m"]
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

        # Caso não encontre valores para o nome procurado
        except Exception:
            return 0.0
