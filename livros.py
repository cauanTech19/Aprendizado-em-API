from flask import jsonify, request, Blueprint, Response
from flask_jwt_extended import jwt_required
from models import Livro, db
from typing import Any

# Blueprint responsável pelas rotas de livros
livros_pb: Blueprint = Blueprint('livros', __name__)


@livros_pb.post('/add')
@jwt_required()
def criar_livro() -> tuple[Response, int]:
    """
    Cria um novo livro no sistema.

    Requisitos:
        - Usuário autenticado (JWT obrigatório)
        - Campos 'titulo' e 'autor' devem estar preenchidos
        - Título não pode estar duplicado

    Retorno:
        201: Livro criado com sucesso
        400: Campos vazios
        409: Livro já existente
        500: Erro interno no servidor
    """
    try:
        dados: dict[str, Any] = request.get_json()

        # Validação de campos obrigatórios
        if not dados.get('titulo') or not dados.get('autor'):
            return jsonify({'Mensagem': 'Campo(s) estão vazios'}), 400

        # Verifica duplicidade de título
        if Livro.query.filter_by(titulo=dados['titulo']).first():
            return jsonify({'Mensagem': 'Esse livro já foi cadastrado'}), 409

        # Criação do livro
        novo_livro: Livro = Livro(titulo=dados['titulo'], autor=dados['autor'])
        db.session.add(novo_livro)
        db.session.commit()

        return jsonify(novo_livro.to_dict()), 201

    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({'Mensagem': 'Erro interno no servidor'}), 500


@livros_pb.get('/list')
def listar_livros() -> tuple[Response, int]:
    """
    Lista todos os livros cadastrados.

    Retorno:
        200: Lista de livros
        404: Nenhum livro encontrado
    """
    livros: list[Livro] = Livro.query.all()

    if not livros:
        return jsonify({'Mensagem': 'Não há livros para exibir'}), 404

    return jsonify([l.to_dict() for l in livros]), 200


@livros_pb.get('/buscar/<int:id>')
def buscar_por_id(id: int) -> tuple[Response, int]:
    """
    Busca um livro pelo ID.

    Parâmetros:
        id (int): Identificador do livro

    Retorno:
        200: Livro encontrado
        404: Livro não encontrado
    """
    busca: Livro | None = Livro.query.get(id)

    if busca is None:
        return jsonify({"erro": 'id não encontrado'}), 404

    return jsonify(busca.to_dict()), 200


@livros_pb.put('/atualizar/<int:id>')
@jwt_required()
def atualizar_livro(id: int) -> tuple[Response, int]:
    """
    Atualiza os dados de um livro existente.

    Requisitos:
        - Usuário autenticado (JWT obrigatório)
        - Livro deve existir
        - Campos 'titulo' e 'autor' devem estar preenchidos

    Parâmetros:
        id (int): Identificador do livro

    Retorno:
        200: Livro atualizado com sucesso
        400: Campos inválidos
        404: Livro não encontrado
        500: Erro interno no servidor
    """
    try:
        atualizar: Livro | None = Livro.query.get(id)

        if atualizar is None:
            return jsonify({'Mensagem': 'id não encontrado'}), 404

        dados: dict[str, Any] = request.get_json()

        # Validação de campos obrigatórios
        if not dados.get('titulo') or not dados.get('autor'):
            return jsonify({'Mensagem': 'Campo(s) estão vazios'}), 400

        # Atualização dos dados
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
def remover_livro(id: int) -> tuple[Response, int]:
    """
    Remove um livro pelo ID.

    Requisitos:
        - Usuário autenticado (JWT obrigatório)
        - Livro deve existir

    Parâmetros:
        id (int): Identificador do livro

    Retorno:
        200: Livro removido com sucesso
        404: Livro não encontrado
        500: Erro interno no servidor
    """
    try:
        livros: Livro | None = Livro.query.get(id)

        if livros is None:
            return jsonify({"Erro": 'id não encontrado'}), 404

        # Remoção do livro
        db.session.delete(livros)
        db.session.commit()

        return jsonify({"Mensagem": 'Livro removido com sucesso!'}), 200

    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({'Mensagem': 'Erro interno no servidor'}), 500