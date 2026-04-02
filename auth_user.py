from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
<<<<<<< HEAD
=======
from models import db, Usuario, bcrypt
>>>>>>> dev
from models import Usuario, db

auth_pb = Blueprint('auth_user', __name__)

@auth_pb.post('/registro')
def registro():
<<<<<<< HEAD
    dados = request.get_json()
    novo_user = Usuario(user=dados['user'], senha=dados['senha'])
    db.session.add(novo_user)
    db.session.commit()
    return jsonify(novo_user.to_dict()), 201
=======
    try:
        dados = request.get_json()

        if not dados.get('user') or not dados.get('senha'):
            return jsonify({'Mensagem': 'Campo(s) estão vazios'}), 400
        
        if Usuario.query.filter_by(user=dados['user']).first():
            return jsonify({"Mensagem": 'Usuário já existe no sistema'}), 409
        
        senha_hash = bcrypt.generate_password_hash(dados['senha']).decode('utf-8')

        novo_user = Usuario(user=dados['user'], senha=senha_hash)
        db.session.add(novo_user)
        db.session.commit()
        return jsonify(novo_user.to_dict()), 201
    
    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({'Mensagem': 'Erro interno no servidor'}), 500
>>>>>>> dev


@auth_pb.post('/login')
def login():
<<<<<<< HEAD
    dados = request.get_json()
    usuario = Usuario.query.filter_by(user=dados['user']).first()

    if usuario is None or usuario.senha != dados['senha']:
        return jsonify({'Mensagem': 'Usuário ou senha estão incorretos'}), 404
    
    token = create_access_token(identity=str(usuario.id))
    return jsonify({'token': token})
=======
    try:
        dados = request.get_json()

        if not dados.get('user') or not dados.get('senha'):
            return jsonify({'Mensagem': 'Os campo(s) estão vazios'}), 400
        
        usuario = Usuario.query.filter_by(user=dados['user']).first()

        if usuario is None or not bcrypt.check_password_hash(usuario.senha, dados['senha']):
            return jsonify({'Mensagem': 'Usuário ou senha estão incorretos'}), 401
        
        token = create_access_token(identity=str(usuario.id))
        return jsonify({'token': token}), 200
    
    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({'Mensagem': 'Erro interno no servidor'}), 500


>>>>>>> dev
 