import re
import string
from typing import Union

def senha_sequencial(senha:str) -> bool:
    """
    Verifica se a senha contém sequências simples de caracteres.

    Exemplos de sequências detectadas:
    - Numéricas: 123, 456, 789
    - Alfabéticas: abc, def
    - Teclado: qwe, wer

    Parâmetros:
        senha (str): Senha a ser analisada.

    Retorno:
        bool: True se houver sequência simples, False caso contrário.
    """
    valores_sequenciais: list[str] = [
        "1234567890",
        "abcdefghijklmnopqrstuvwxyz",
        "qwertyuiop"
    ]

    senhas: str = senha.lower()

    for valor in valores_sequenciais:
        for i in range(len(senhas) - 2):
            parte: str = senhas[i:i+3]

            if parte in valor:
                return True
    return False


class ValidarSenha:
    """
    Classe responsável por validar regras de segurança de senha.
    """

    @staticmethod
    def validar_senha(senha:str) -> Union[str, None]:
        """
        Valida a senha com base em critérios de segurança.

        Regras:
        - Mínimo de 8 caracteres
        - Deve conter letras minúsculas
        - Deve conter letras maiúsculas
        - Deve conter números
        - Deve conter pelo menos um caractere especial
        - Não pode conter sequências simples (ex: 123, abc, qwe)

        Parâmetros:
            senha (str): Senha a ser validada.

        Retorno:
            str | None:
                - Retorna mensagem de erro se inválida
                - Retorna None se válida
        """
        minusculo: bool = any(i.islower() for i in senha)
        maiusculo: bool = any(i.isupper() for i in senha)
        numero: bool = any(i.isdigit() for i in senha)
        caracteres_especiais: bool = any(c in string.punctuation for c in senha)

        if len(senha) < 8:
            return 'Senha fraca: mínimo 8 caracteres.'

        if not all([maiusculo, minusculo, numero]):
            return 'Senha fraca: deve conter letras minúsculas, maiúsculas e números.'

        if not caracteres_especiais:
            return 'Senha fraca: inclua pelo menos um caractere especial.'

        if senha_sequencial(senha):
            return 'Senha não pode conter sequências simples.'

        return None


class ValidarEmail:
    """
    Classe responsável por validar formato de e-mail.
    """

    @staticmethod
    def validar_email(email:str) -> Union[str, None]:
        """
        Valida se o e-mail está em um formato válido usando regex.

        Parâmetros:
            email (str): E-mail a ser validado.

        Retorno:
            str | None:
                - Retorna mensagem de erro se inválido
                - Retorna None se válido
        """
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(padrao, email):
            return 'Email inválido'
        return None


class ValidarUsuario:
    """
    Classe responsável por validar dados completos de um usuário.
    """

    @staticmethod
    def validar_dados_usuarios(email: str, senha: str) -> Union[str, None]:
        """
        Valida email e senha de um usuário.

        Fluxo:
        1. Valida o email
        2. Se válido, valida a senha

        Parâmetros:
            email (str): Email do usuário
            senha (str): Senha do usuário

        Retorno:
            str | None:
                - Retorna erro encontrado (email ou senha)
                - Retorna None se tudo estiver válido
        """
        erro_email: Union[str, None] = ValidarEmail.validar_email(email)
        if erro_email:
            return erro_email

        erro_senha: Union[str, None] = ValidarSenha.validar_senha(senha)
        if erro_senha:
            return erro_senha

        return None