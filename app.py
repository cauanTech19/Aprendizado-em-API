import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, bcrypt
from auth_user import auth_pb
from livros import livros_pb

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env para o sistema
# Deve ser chamado antes de qualquer os.getenv()
load_dotenv()


def create_app(test_config: bool = False) -> Flask:
    """
    Cria e configura a instância da aplicação Flask (Application Factory Pattern).

    Este padrão permite criar múltiplas instâncias da aplicação com configurações
    diferentes, o que é especialmente útil para separar ambientes de teste e produção
    sem alterar o código principal.

    Args:
        test_config (bool): 
            - False (padrão): usa o banco de dados MySQL definido em DATABASE_URL.
            - True: usa SQLite em memória, ideal para testes automatizados,
              pois não persiste dados e não afeta o banco de produção.

    Returns:
        Flask: instância da aplicação completamente configurada e pronta para uso.

    Variáveis de ambiente necessárias (.env):
        DATABASE_URL  : URL de conexão com o MySQL. Ex: mysql://user:pass@host/db
        JWT_SECRET_KEY: Chave secreta para assinar e validar os tokens JWT.

    Exemplo de uso:
        # Produção
        app = create_app()

        # Testes
        app = create_app(test_config=True)
    """

    # -------------------------------------------------------------------------
    # Passo 1: Criar a instância base do Flask
    # __name__ indica o pacote/módulo atual, usado pelo Flask para localizar
    # arquivos estáticos e templates corretamente.
    # -------------------------------------------------------------------------
    app: Flask = Flask(__name__)

    # -------------------------------------------------------------------------
    # Passo 2: Habilitar CORS (Cross-Origin Resource Sharing)
    # Permite que o frontend (em outro domínio/porta) faça requisições à API.
    # Sem isso, o navegador bloquearia as chamadas por política de segurança.
    # -------------------------------------------------------------------------
    CORS(app)

    # -------------------------------------------------------------------------
    # Passo 3: Configurar o banco de dados
    # Decide qual banco usar com base no parâmetro test_config.
    # -------------------------------------------------------------------------
    if test_config:
        # Modo de teste: banco SQLite em memória.
        # Vantagens: rápido, isolado, destruído ao encerrar a aplicação.
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        # Modo de produção: banco MySQL via variável de ambiente.
        mysql_url: str | None = os.getenv('DATABASE_URL')

        if mysql_url:
            # O SQLAlchemy exige o driver PyMySQL explicitamente.
            # Por isso, substituímos o prefixo 'mysql://' por 'mysql+pymysql://'.
            # Ex: mysql://user:pass@host/db → mysql+pymysql://user:pass@host/db
            mysql_url = mysql_url.replace('mysql://', 'mysql+pymysql://')

        app.config['SQLALCHEMY_DATABASE_URI'] = mysql_url

    # -------------------------------------------------------------------------
    # Passo 4: Configurar a chave secreta do JWT
    # Usada para assinar os tokens de autenticação.
    # IMPORTANTE: deve ser uma string longa, aleatória e mantida em segredo.
    # -------------------------------------------------------------------------
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # -------------------------------------------------------------------------
    # Passo 5: Inicializar as extensões com a instância do app
    # As extensões precisam do app para se registrar e acessar suas configs.
    # -------------------------------------------------------------------------
    db.init_app(app)       # Conecta o SQLAlchemy ao app (ORM do banco de dados)
    bcrypt.init_app(app)   # Conecta o Bcrypt ao app (hashing seguro de senhas)
    JWTManager(app)        # Inicializa o gerenciador de tokens JWT

    # -------------------------------------------------------------------------
    # Passo 6: Registrar os Blueprints (módulos de rotas)
    # Blueprints organizam as rotas em grupos lógicos e separados.
    # -------------------------------------------------------------------------
    app.register_blueprint(auth_pb)    # Rotas de autenticação: /login, /register, etc.
    app.register_blueprint(livros_pb)  # Rotas de livros: /livros, /livros/<id>, etc.

    # -------------------------------------------------------------------------
    # Passo 7: Retornar a aplicação configurada
    # -------------------------------------------------------------------------
    return app


app = create_app()
