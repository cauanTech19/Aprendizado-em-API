from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

from models import db
from auth import auth_pb
from livros import livros_pb



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')


db.init_app(app)
JWTManager(app)

app.register_blueprint(auth_pb)
app.register_blueprint(livros_pb)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
