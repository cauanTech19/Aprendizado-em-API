import unittest
from app import create_app, Flask
from models import db
from flask.testing import FlaskClient
from flask.ctx import AppContext
from werkzeug.test import TestResponse


class TestRegistro(unittest.TestCase):
    """
    Classe de testes de integração para o endpoint de registro de usuários.

    Esses testes validam o comportamento da rota /registro,
    incluindo cenários de sucesso e diferentes tipos de erro.
    """

    def setUp(self) -> None:
        """
        Configuração inicial antes de cada teste.

        - Cria uma instância da aplicação em modo de teste
        - Inicializa o cliente de requisição
        - Cria o contexto da aplicação
        - Cria todas as tabelas no banco de dados
        """
        self.app: Flask = create_app(test_config=True)
        self.client: FlaskClient = self.app.test_client()

        self.ctx: AppContext = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self) -> None:
        """
        Limpeza após cada teste.

        - Remove a sessão do banco de dados
        - Remove todas as tabelas criadas
        - Finaliza o contexto da aplicação
        """
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
    
    def test_registro_sucesso(self) -> None:
        """
        Testa o registro de um usuário válido.

        Esperado:
        - Status code 201 (Created)
        """
        response: TestResponse = self.client.post('/registro', json={
            "email": "teste@email.com",
            "senha": "Teste@12"
        })
        self.assertEqual(response.status_code, 201)

    def test_registro_email_vazio(self) -> None:
        """
        Testa o registro com email vazio.

        Esperado:
        - Status code 400 (Bad Request)
        """
        response: TestResponse = self.client.post('/registro', json={
            "email": "",
            "senha": "Teste@12"
        })
        self.assertEqual(response.status_code, 400)

    def test_registro_email_incorreto(self) -> None:
        """
        Testa o registro com email em formato inválido.

        Esperado:
        - Status code 400 (Bad Request)
        """
        response: TestResponse  = self.client.post('/registro', json={
            "email": "@gmail.com",
            "senha": "16495User!@"
        })
        self.assertEqual(response.status_code, 400)

    def test_registro_conta_existente(self) -> None:
        """
        Testa tentativa de registro com email já cadastrado.

        Fluxo:
        1. Cria um usuário
        2. Tenta criar novamente com o mesmo email

        Esperado:
        - Status code 409 (Conflict)
        """
        self.client.post('/registro', json={
            "email": "teste@email.com",
            "senha": "Teste@12"
        })
        
        cadastro: TestResponse = self.client.post('/registro', json={
            "email": "teste@email.com",
            "senha": "Teste@12"
        })        
        self.assertEqual(cadastro.status_code, 409)
    
    def test_registro_senha_incorreta(self) -> None:
        """
        Testa registro com senha inválida (não atende aos critérios).

        Esperado:
        - Status code 400 (Bad Request)
        """
        response: TestResponse  = self.client.post('/registro', json={
            "email": "user@gmail.com",
            "senha": "123"
        })
        self.assertEqual(response.status_code, 400)

    def test_registro_senha_vazia(self) -> None:
        """
        Testa registro com senha vazia.

        Esperado:
        - Status code 400 (Bad Request)
        """
        response: TestResponse  = self.client.post('/registro', json={
            "email": "user@gmail.com",
            "senha": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_registro_senha_e_email_identico(self) -> None:
        """
        Testa registro onde senha e email são iguais.

        Esperado:
        - Status code 400 (Bad Request)
        """
        response: TestResponse = self.client.post('/registro', json={
            "email": "user@gmail.com",
            "senha": "user@gmail.com"
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    """
    Ponto de entrada para execução dos testes.
    """
    unittest.main()