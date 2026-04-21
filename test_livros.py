import unittest
from app import create_app, db, Flask
from typing import Any
from flask.testing import FlaskClient
from flask.ctx import AppContext
from werkzeug.test import TestResponse


class TestLivros(unittest.TestCase):
    """
    Classe de testes de integração para o CRUD de livros.

    Testa todas as operações:
    - CREATE (criação de livros)
    - READ (listagem e busca)
    - UPDATE (atualização)
    - DELETE (remoção)

    Também valida autenticação via token JWT.
    """

    def setUp(self) -> None:
        """
        Configuração inicial antes de cada teste.

        - Cria a aplicação em modo de teste
        - Inicializa o cliente HTTP
        - Cria o contexto da aplicação
        - Cria as tabelas no banco de dados
        """

        self.app: Flask = create_app(test_config=True)
        self.client: FlaskClient = self.app.test_client()

        self.ctx: AppContext = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self) -> None:
        """
        Limpeza após cada teste.

        - Remove sessão do banco
        - Remove todas as tabelas
        - Finaliza o contexto da aplicação
        """
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def registrar(self) -> TestResponse:
        """
        Registra um usuário padrão para testes.

        Retorno:
            Response: resposta da requisição HTTP
        """
        return self.client.post('/registro', json={
            "email": "teste@email.com",
            "senha": "Teste@12"
        })

    def login(self) -> TestResponse:
        """
        Realiza login com o usuário padrão.

        Retorno:
            Response: resposta da requisição HTTP
        """
        return self.client.post('/login', json={
            "email": "teste@email.com",
            "senha": "Teste@12"
        })

    def autenticar(self) -> TestResponse:
        """
        Realiza o fluxo completo de autenticação.

        Fluxo:
        1. Registra o usuário
        2. Realiza login
        3. Obtém o token JWT

        Retorno:
            str: token de autenticação
        """

        self.registrar()
        response = self.login()
        return response.get_json().get("token")

    def headers(self, token: str) -> dict[str, str]:
        """
        Monta os headers de autenticação.

        Parâmetros:
            token (str): token JWT

        Retorno:
            dict: headers HTTP com Authorization
        """

        return {
            "Authorization": f"Bearer {token}"
        }

    def criar_livro(self, token: str, titulo: str= "Livro Teste", autor: str ="Autor Teste") -> TestResponse:
        """
        Cria um livro autenticado.

        Parâmetros:
            token (str): token JWT
            titulo (str): título do livro
            autor (str): autor do livro

        Retorno:
            Response: resposta da requisição HTTP
        """
        return self.client.post(
            '/add',
            json={"titulo": titulo, "autor": autor},
            headers=self.headers(token)
        )

    # =========================
    # CREATE
    # =========================

    def test_adicionando_livro_com_sucesso(self) -> None:
        """
        Testa criação de livro com dados válidos.

        Esperado:
        - Status code 201 (Created)
        """

        token: Any = self.autenticar()
        response: TestResponse = self.criar_livro(token)

        self.assertEqual(response.status_code, 201)

    def test_titulo_vazio(self) -> None:
        """
        Testa criação com título vazio.

        Esperado:
        - Status code 400 (Bad Request)
        """
        token: Any = self.autenticar()
        response: TestResponse = self.criar_livro(token, titulo="", autor="Autor Teste")

        self.assertEqual(response.status_code, 400)

    def test_autor_vazio(self) -> None:
        """
        Testa criação com autor vazio.

        Esperado:
        - Status code 400 (Bad Request)
        """
        token: Any = self.autenticar()
        response: TestResponse = self.criar_livro(token, titulo="Livro Teste", autor="")

        self.assertEqual(response.status_code, 400)

    def test_titulo_duplicados(self) -> None:
        """
        Testa criação de livros com título duplicado.

        Esperado:
        - Status code 409 (Conflict)
        """
        token: Any = self.autenticar()
        self.criar_livro(token)
        response: TestResponse = self.criar_livro(token)

        self.assertEqual(response.status_code, 409)

    # =========================
    # READ
    # =========================

    def test_sem_livros_para_exibir(self) -> None:
        """
        Testa listagem sem livros cadastrados.

        Esperado:
        - Status code 404 (Not Found)
        """
        response: TestResponse = self.client.get('/list')
        self.assertEqual(response.status_code, 404)

    def test_exibindo_livros_com_sucesso(self) -> None:
        """
        Testa listagem com livros cadastrados.

        Esperado:
        - Status code 200 (OK)
        """
        token: Any = self.autenticar()
        self.criar_livro(token)

        response: TestResponse = self.client.get('/list')
        self.assertEqual(response.status_code, 200)

    def test_buscar_id_com_sucesso(self) -> None:
        """
        Testa busca de livro por ID existente.

        Esperado:
        - Status code 200 (OK)
        """
        token: Any = self.autenticar()
        self.criar_livro(token)

        response: TestResponse = self.client.get('/buscar/1')
        self.assertEqual(response.status_code, 200)

    def test_buscando_id_nao_existe(self) -> None:
        """
        Testa busca por ID inexistente.

        Esperado:
        - Status code 404 (Not Found)
        """
        response: TestResponse = self.client.get('/buscar/10')
        self.assertEqual(response.status_code, 404)

    def test_buscando_id_com_sucesso(self) -> None:
        """
        Testa listagem geral após inserção de livro.

        Esperado:
        - Status code 200 (OK)
        """
        token: Any = self.autenticar()
        self.criar_livro(token)
        response: TestResponse = self.client.get('/list')
        
        self.assertEqual(response.status_code, 200)

    # =========================
    # UPDATE
    # =========================

    def test_atualizando_id_com_sucesso(self) -> None:
        """
        Testa atualização de livro com ID válido.

        Esperado:
        - Status code 200 (OK)
        """
        token: Any = self.autenticar()
        self.criar_livro(token)

        response: TestResponse = self.client.put(
            '/atualizar/1',
            json={"titulo": "Livro Novo", "autor": "Autor Novo"},
            headers=self.headers(token)
        )

        self.assertEqual(response.status_code, 200)

    def test_id_nao_encontrado_para_atualizacao(self) -> None:
        """
        Testa atualização de livro com ID inexistente.

        Esperado:
        - Status code 404 (Not Found)
        """
        token: Any = self.autenticar()
        self.criar_livro(token)

        response: TestResponse = self.client.put(
            '/atualizar/2',
            json={"titulo": "Livro Novo", "autor": "Autor Novo"},
            headers=self.headers(token)
        )

        self.assertEqual(response.status_code, 404)

    def test_titulo_vazio_para_atualizacao(self) -> None:
        """
        Testa atualização com título vazio.

        Esperado:
        - Status code 400 (Bad Request)
        """

        token: Any = self.autenticar()
        self.criar_livro(token)

        response: TestResponse = self.client.put(
            '/atualizar/1',
            json={"titulo": "", "autor": "Autor Novo"},
            headers=self.headers(token)
        )

        self.assertEqual(response.status_code, 400)

    def test_autor_vazio_para_atualizacao(self) -> None:
        """
        Testa atualização com autor vazio.

        Esperado:
        - Status code 400 (Bad Request)
        """
        token: Any = self.autenticar()
        self.criar_livro(token)

        response: TestResponse = self.client.put(
            '/atualizar/1',
            json={"titulo": "Titulo Novo", "autor": ""},
            headers=self.headers(token)
        )

        self.assertEqual(response.status_code, 400)

    # =========================
    # DELETE
    # =========================

    def test_id_nao_encontrado_para_remocao(self) -> None:
        """
        Testa remoção de livro com ID inexistente.

        Esperado:
        - Status code 404 (Not Found)
        """

        token: Any = self.autenticar()
        self.criar_livro(token)

        response: TestResponse = self.client.delete(
            '/livros/2',
            json={"titulo": "Titulo Novo", "autor": "Autor Novo"},
            headers=self.headers(token)
        )

        self.assertEqual(response.status_code, 404)

    def test_removendo_livro_com_sucesso(self) -> None:
        """
        Testa remoção de livro com ID válido.

        Esperado:
        - Status code 200 (OK)
        """
        
        token: Any = self.autenticar()
        self.criar_livro(token)

        response: TestResponse = self.client.delete(
            '/livros/1',
            json={"titulo": "Titulo Novo", "autor": "Autor Novo"},
            headers=self.headers(token)
        )

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    """
    Ponto de entrada para execução dos testes.
    """
    unittest.main()