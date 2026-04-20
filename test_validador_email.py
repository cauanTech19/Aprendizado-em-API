import unittest
from validador import ValidarEmail


class TestValidadorEmail(unittest.TestCase):
    """
    Classe de testes unitários para validação de e-mails.

    Garante que a função validar_email da classe ValidarEmail
    esteja funcionando corretamente para diferentes cenários.
    """

    def test_casos_emails_invalidos(self):
        """
        Testa diferentes formatos de e-mails inválidos.

        Casos testados:
        - Ausência de usuário antes do @
        - Domínio mal formatado
        - TLD (extensão) com tamanho inválido
        """
        msg = 'Email inválido'

        valores_invalidos = [
           ('@email.com', msg),
           ('user@.com', msg),
           ('user@email.c', msg),
        ]

        for email, esperado in valores_invalidos:
            self.assertEqual(ValidarEmail.validar_email(email), esperado)

    def test_casos_emails_validos(self):
        """
        Testa e-mails válidos com diferentes variações.

        Casos testados:
        - E-mail simples
        - E-mail com subdomínio
        - E-mail com caractere especial (+)
        """
        valores_validos = [
            'user@gmail.com',
            'teste.email@empresa.com.br',
            'user+1@email.com'        
        ]

        for email in valores_validos:
            self.assertIsNone(ValidarEmail.validar_email(email))


if __name__ == '__main__':
    """
    Ponto de entrada para execução dos testes unitários.
    """
    unittest.main()