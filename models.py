from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Instância do ORM para manipulação do banco de dados
db = SQLAlchemy()

# Instância para criptografia de senhas
bcrypt = Bcrypt()  


class Livro(db.Model):
    """
    Modelo que representa a entidade Livro no banco de dados.

    Atributos:
        id (int): Identificador único do livro (chave primária)
        titulo (str): Título do livro (obrigatório)
        autor (str): Nome do autor (obrigatório)
    """
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)

    def __init__(self, titulo, autor):
        """
        Inicializa um novo objeto Livro.

        Parâmetros:
            titulo (str): Título do livro
            autor (str): Nome do autor
        """
        self.titulo = titulo
        self.autor = autor

    def to_dict(self):
        """
        Converte o objeto Livro em um dicionário.

        Retorno:
            dict: Representação do livro em formato JSON
        """
        return {'id': self.id, 'titulo': self.titulo, 'autor': self.autor}
    

class Usuario(db.Model):
    """
    Modelo que representa a entidade Usuario no banco de dados.

    Atributos:
        id (int): Identificador único do usuário (chave primária)
        email (str): Email do usuário (obrigatório)
        senha (str): Senha criptografada do usuário (obrigatório)
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __init__(self, email, senha):
        """
        Inicializa um novo objeto Usuario.

        Parâmetros:
            email (str): Email do usuário
            senha (str): Senha do usuário (já deve estar criptografada)
        """
        self.email = email
        self.senha = senha

    def to_dict(self):
        """
        Converte o objeto Usuario em um dicionário.

        Observação:
            A senha não é retornada por questões de segurança.

        Retorno:
            dict: Representação do usuário em formato JSON
        """
        return {'id': self.id, 'email': self.email}