import unittest
from app import create_app, db


class TestLogin(unittest.TestCase):
    """
    Classe de testes de integração para o endpoint de login.

    Verifica diferentes cenários de autenticação,
    incluindo sucesso e falhas comuns.
    """

    def setUp(self) -> None:
        """
        Configuração inicial antes de cada teste.

        - Cria a aplicação em modo de teste
        - Inicializa o cliente HTTP
        - Cria o contexto da aplicação
        - Cria as tabelas no banco de dados
        """
        self.app = create_app(test_config=True)
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
    
    def tearDown(self) -> None:
        """
        Limpeza após cada teste.

        - Remove a sessão do banco
        - Apaga todas as tabelas
        - Finaliza o contexto da aplicação
        """
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
    
    def test_login_sucess(self):
        """
        Testa login com credenciais válidas.

        Fluxo:
        1. Registra um usuário
        2. Realiza login com os mesmos dados

        Esperado:
        - Status code 200 (OK)
        """
        self.client.post('/registro', json={
            "email": "teste@email.com",
            "senha": "Teste@12"
        })

        response = self.client.post('/login', json={
            "email": "teste@email.com",
            "senha": "Teste@12"
        })

        self.assertEqual(response.status_code, 200)

    def test_login_email_vazio(self):
        """
        Testa login com email vazio.

        Esperado:
        - Status code 400 (Bad Request)
        """
        response = self.client.post('/login', json={
            "email": "",
            "senha": "Teste@12"
        })

        self.assertEqual(response.status_code, 400)

    def test_login_email_incorreto(self):
        """
        Testa login com email não cadastrado.

        Esperado:
        - Status code 401 (Unauthorized)
        """
        response = self.client.post('/login', json={
            "email": "teste@email.com",
            "senha": "Teste@12"
        })

        self.assertEqual(response.status_code, 401)

    def test_login_senha_vazia(self):
        """
        Testa login com senha vazia.

        Esperado:
        - Status code 400 (Bad Request)
        """
        response = self.client.post('/login', json={
            "email": "teste@email.com",
            "senha": ""
        })

        self.assertEqual(response.status_code, 400)

    def test_login_senha_incorreta(self):
        """
        Testa login com senha incorreta.

        Fluxo:
        1. Registra um usuário válido
        2. Tenta login com senha errada

        Esperado:
        - Status code 401 (Unauthorized)
        """
        self.client.post('/registro', json={
            "email": "teste@email.com",
            "senha": "Teste@12"
        })

        response = self.client.post('/login', json={
            "email": "teste@email.com",
            "senha": "Senha1!247|"
        })

        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    """
    Ponto de entrada para execução dos testes.
    """
    unittest.main()