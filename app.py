import os
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from flask_cors import CORS
from models import db, bcrypt
from auth_user import auth_pb
from livros import livros_pb


load_dotenv()

def create_app(test_config=False):
    app = Flask(__name__)
    CORS(app)

    if test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        mysql_url = os.getenv('DATABASE_URL')
        if mysql_url:
            mysql_url = mysql_url.replace('mysql://', 'mysql+pymysql://')

        app.config['SQLALCHEMY_DATABASE_URI'] = mysql_url

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_pb)
    app.register_blueprint(livros_pb)
    return app


