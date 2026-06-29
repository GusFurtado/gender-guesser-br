"""Exceções personalizadas do pacote gender-guesser-br."""


class GenderGuesserError(Exception):
    """
    Erro base do GenderGuesser.

    Representa qualquer erro relacionado ao uso incorreto
    ou inesperado do pacote gender-guesser-br.

    """

    MSG_NOME_DEVE_SER_STRING = "O parâmetro 'nome' deve ser uma string."
    MSG_NOME_VAZIO = "O parâmetro 'nome' não pode ser vazio."
    MSG_UF_INVALIDA = "UF inválida: '{}'. Use a sigla de duas letras ou o código IBGE da UF."
    MSG_CORTE_AMBOS_INVALIDO = "Insira um valor entre 0.5 e 1.0 para `corte_ambos`."
    MSG_CORTE_MAIORIA_INVALIDO = "Insira um valor entre 0.5 e 1.0 para `corte_maioria`."
    MSG_CORTE_MAIORIA_MENOR = (
        "O valor de `corte_maioria` deve ser maior que o valor de `corte_ambos`."
    )
