import unittest
from validador import ValidarSenha, senha_sequencial


class TestValidadorSenha(unittest.TestCase):
    """
    Classe de testes unitários para validação de senhas.

    Testa regras de segurança implementadas na classe ValidarSenha
    e na função senha_sequencial.
    """

    def test_senha_menor_que_8_caracteres(self):
        """
        Testa se a validação retorna erro quando a senha possui
        menos de 8 caracteres.
        """
        self.assertEqual(
            ValidarSenha.validar_senha('zeca12'),
            'Senha fraca: mínimo 8 caracteres.'
        )

    def test_senha_sem_letras_minusculas_maiusculas_numeros(self):
        """
        Testa senhas que não atendem ao requisito de conter:
        - letras minúsculas
        - letras maiúsculas
        - números
        """
        msg = 'Senha fraca: deve conter letras minúsculas, maiúsculas e números.'

        senhas_invalidads = [
           ('ASDQWEDFEF1235@', msg),   # sem minúsculas
           ('adfdfrergefveht1235', msg),  # sem maiúsculas
           ('aASDqwegtrwf!@', msg),   # sem números
        ]

        for senha, esperado in senhas_invalidads:
            self.assertEqual(ValidarSenha.validar_senha(senha), esperado)

    def test_senha_sem_caracteres(self):
        """
        Testa senhas que não possuem caracteres especiais.
        """
        msg = 'Senha fraca: inclua pelo menos um caractere especial.'
        senhas_nao_sequencias = [
            ('CauanPass1691', msg),
            ('EduCosta2591', msg),
            ('LeoSoares451', msg)
        ]

        for senha, esperado in senhas_nao_sequencias:
            self.assertEqual(ValidarSenha.validar_senha(senha), esperado)

    def test_senha_sequencial(self):
        """
        Testa se a função senha_sequencial identifica corretamente
        sequências simples dentro da senha.
        """
        senhas_sequencias = [
           '123456789',
           'abcdefghi',
           'rootqwe123!@',
           'ABCDEFGH123!@'
        ]

        for senha in senhas_sequencias:
            self.assertTrue(senha_sequencial(senha))

    def test_senha_nao_sequencial(self):
        """
        Testa senhas que NÃO possuem sequências simples,
        garantindo que a função retorne False.
        """
        senhas_nao_sequencias = [
           'CauanPass1691!@',
           'EduCosta$$2591',
           'LeoSoares451!'
        ]

        for senha in senhas_nao_sequencias:
            self.assertFalse(senha_sequencial(senha))

    def test_sequencia_case_insensitive(self):
        """
        Testa se a verificação de sequência é case insensitive,
        ou seja, não diferencia maiúsculas de minúsculas.
        """
        self.assertTrue(senha_sequencial('ABC'))

    def test_senha_valida(self):
        """
        Testa uma senha completamente válida que atende
        a todos os critérios de segurança.
        """
        self.assertIsNone(ValidarSenha.validar_senha('DEVs&&1995'))


if __name__ == '__main__':
    """
    Ponto de entrada para execução dos testes unitários.
    """
    unittest.main()