from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

from models import db, bcrypt
from auth_user import auth_pb
from livros import livros_pb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
bcrypt.init_app(app)
JWTManager(app)

app.register_blueprint(auth_pb)
app.register_blueprint(livros_pb)

@app.errorhandler(500)
def erro_interno(e):
    return jsonify({'Mensagem': 'Erro interno no servidor'}), 500

@app.errorhandler(404)
def rota_nao_encontrada(e):
    return jsonify({'Mensagem': 'Rota não encontrada'}), 404

@app.errorhandler(405)
def metodo_nao_permitido(e):
    return jsonify({'Mensagem': 'Método não permitido'}), 405

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False) 
