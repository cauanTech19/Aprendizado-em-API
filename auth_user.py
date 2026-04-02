from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
from models import Usuario, db

auth_pb = Blueprint('auth_user', __name__)

@auth_pb.post('/registro')
def registro():
    dados = request.get_json()
    novo_user = Usuario(user=dados['user'], senha=dados['senha'])
    db.session.add(novo_user)
    db.session.commit()
    return jsonify(novo_user.to_dict()), 201


@auth_pb.post('/login')
def login():
    dados = request.get_json()
    usuario = Usuario.query.filter_by(user=dados['user']).first()

    if usuario is None or usuario.senha != dados['senha']:
        return jsonify({'Mensagem': 'Usuário ou senha estão incorretos'}), 404
    
    token = create_access_token(identity=str(usuario.id))
    return jsonify({'token': token})
 