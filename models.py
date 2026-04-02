from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()  


class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)

    def __init__(self, titulo, autor):
        self.titulo =  titulo
        self.autor =  autor

    def to_dict(self):
        return {'id': self.id, 'titulo': self.titulo, 'autor': self.autor}
    

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __init__(self,user, senha):
        self.user = user
        self.senha = senha

    def to_dict(self):
        return {'id': self.id, 'user': self.user}
