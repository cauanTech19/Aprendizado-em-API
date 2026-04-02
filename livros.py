from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from models import Livro, db

livros_pb = Blueprint('livros', __name__)

@livros_pb.post('/add')
@jwt_required()
def criar_livro():
    try:
        dados = request.get_json()
        if not dados.get('titulo') or not dados.get('autor'):
            return jsonify({'Mensagem': 'Campo(s) estão vazios'}), 400
        
        if not isinstance(dados.get('titulo'), str) or not isinstance(dados.get('autor'), str):
            return jsonify({'Mensagem': 'Título e Autor são caracteres'}), 400
        
        if Livro.query.filter_by(titulo=dados['titulo']).first():
            return jsonify({'Mensagem': 'Esse livro já foi cadastrado' }), 409

        novo_livro = Livro(titulo=dados['titulo'], autor=dados['autor'])
        db.session.add(novo_livro)
        db.session.commit()
        return jsonify(novo_livro.to_dict()), 201
    
    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({'Mensagem': 'Erro interno no servidor'}), 500

@livros_pb.get('/list')
def listar_livros():
    livros = Livro.query.all()
    if not livros:
        return jsonify({'Mensagem': 'Não há livros para exibir'}), 404
    return jsonify([l.to_dict() for l in livros]), 200


@livros_pb.get('/buscar/<int:id>')
def buscar_por_id(id):
    busca = Livro.query.get(id)

    if busca is None:
        return jsonify({"erro": 'id não encontrado'}), 404
    
    return jsonify(busca.to_dict()), 200

@livros_pb.put('/atualizar/<int:id>')
@jwt_required()
def atualizar_livro(id):
    try:
        atualizar = Livro.query.get(id)

        if atualizar is None:
            return jsonify({'Mensagem': 'id não encontrado'}), 404
    
        dados = request.get_json()

        if not dados.get('titulo') or not dados.get('autor'):
            return jsonify({'Mensagem': 'Campo(s) estão vazios'}), 400

        atualizar.titulo = dados['titulo']
        atualizar.autor = dados['autor']
        db.session.commit()
        return jsonify(atualizar.to_dict()), 200
    
    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({'Mensagem': 'Erro interno no servidor'}), 500


@livros_pb.delete('/livros/<int:id>')
@jwt_required()
def remover_livro(id):
    try:
        livros = Livro.query.get(id)

        if livros is None:
            return jsonify({"Erro": 'id não encontrado'}), 404
        
        db.session.delete(livros)
        db.session.commit()
        return jsonify({"Mensagem": 'Livro removido com sucesso!'}), 200
    
    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({'Mensagem': 'Erro interno no servidor'}), 500
