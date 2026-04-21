from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Instância do ORM para manipulação do banco de dados
db: SQLAlchemy = SQLAlchemy()

# Instância para criptografia de senhas
bcrypt: Bcrypt = Bcrypt()  


class Livro(db.Model):
    """
    Modelo que representa a entidade Livro no banco de dados.

    Atributos:
        id (int): Identificador único do livro (chave primária)
        titulo (str): Título do livro (obrigatório)
        autor (str): Nome do autor (obrigatório)
    """
    id: int = db.Column(db.Integer, primary_key=True)
    titulo: str = db.Column(db.String(100), nullable=False)
    autor: str = db.Column(db.String(100), nullable=False)

    def __init__(self, titulo: str, autor: str) -> None:
        """
        Inicializa um novo objeto Livro.

        Parâmetros:
            titulo (str): Título do livro
            autor (str): Nome do autor
        """
        self.titulo: str = titulo
        self.autor: str = autor

    def to_dict(self) -> dict[str, int | str]:
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
    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(100), nullable=False)
    senha: str = db.Column(db.String(100), nullable=False)

    def __init__(self, email: str, senha: str) -> None:
        """
        Inicializa um novo objeto Usuario.

        Parâmetros:
            email (str): Email do usuário
            senha (str): Senha do usuário (já deve estar criptografada)
        """
        self.email: str = email
        self.senha: str = senha

    def to_dict(self) -> dict[str, int | str]:
        """
        Converte o objeto Usuario em um dicionário.

        Observação:
            A senha não é retornada por questões de segurança.

        Retorno:
            dict: Representação do usuário em formato JSON
        """
        return {'id': self.id, 'email': self.email}