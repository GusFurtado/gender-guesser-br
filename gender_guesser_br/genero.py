from typing import Literal, Optional, Union
from DadosAbertosBrasil import ibge


class Genero:
    _UFS = {
        "RO": 11,
        "AC": 12,
        "AM": 13,
        "RR": 14,
        "PA": 15,
        "AP": 16,
        "TO": 17,
        "MA": 21,
        "PI": 22,
        "CE": 23,
        "RN": 24,
        "PB": 25,
        "PE": 26,
        "AL": 27,
        "SE": 28,
        "BA": 29,
        "MG": 31,
        "ES": 32,
        "RJ": 33,
        "SP": 35,
        "PR": 41,
        "SC": 42,
        "RS": 43,
        "MS": 50,
        "MT": 51,
        "GO": 52,
        "DF": 53,
    }

    def __init__(self, nome: str, uf: Optional[Union[int, str]] = None):
        # Converte a sigla da UF em código IBGE
        if isinstance(uf, str):
            uf = self._UFS[uf]

        self._f = self._gender_freq(nome, sexo="F", uf=uf)
        self._m = self._gender_freq(nome, sexo="M", uf=uf)

    def __call__(self, corte_ambos: float = 0.6, corte_maioria: float = 0.8) -> str:
        # Validar argumentos
        if corte_ambos < 0.5 or corte_ambos > 1:
            raise ValueError("Insira um valor entre 0.5 e 1.0 para `corte_ambos`.")
        if corte_maioria < 0.5 or corte_maioria > 1:
            raise ValueError("Insira um valor entre 0.5 e 1.0 para `corte_maioria`.")
        if corte_ambos > corte_maioria:
            raise ValueError(
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

    def _gender_freq(nome: str, sexo: Literal["f", "m"], uf: Optional[int] = None):
        try:
            freq = ibge.nomes(nome, sexo=sexo, localidade=uf)
            return freq.squeeze().sum()
        except ValueError:
            return 0

    @property
    def m(self):
        if not (self._f + self._m):
            p = 0
        else:
            p = self._m / (self._f + self._m)

        return {
            "absoluto": self._m,
            "percentual": p,
        }

    @property
    def f(self):
        if not (self._f + self._m):
            p = 0
        else:
            p = self._f / (self._f + self._m)

        return {
            "absoluto": self._f,
            "percentual": p,
        }
