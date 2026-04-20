from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
from models import db, Usuario, bcrypt
from models import Usuario, db
from validador import ValidarUsuario

# Blueprint responsável pelas rotas de autenticação (registro e login)
auth_pb = Blueprint('auth_user', __name__)


@auth_pb.post('/registro')
def registro():
    """
    Realiza o registro de um novo usuário.

    Regras:
        - Email e senha não podem estar vazios
        - Senha não pode ser igual ao email
        - Email deve ser válido
        - Senha deve atender aos critérios de segurança
        - Email não pode já existir no sistema

    Fluxo:
        1. Recebe dados JSON (email, senha)
        2. Valida campos obrigatórios
        3. Valida regras de negócio (ValidarUsuario)
        4. Verifica duplicidade de email
        5. Criptografa a senha
        6. Salva no banco de dados

    Retorno:
        201: Usuário criado com sucesso
        400: Erro de validação
        409: Usuário já existente
        500: Erro interno no servidor
    """
    try:
        dados = request.get_json()
        email = dados.get('email', '').strip().lower()
        senha = dados.get('senha', '').strip()

        # Validação de campos vazios
        if not email or not senha:
            return jsonify({'Mensagem': 'Campo(s) estão vazios'}), 400

        # Regra de negócio: senha não pode ser igual ao email
        if email == senha.lower():
            return jsonify({"Mensagem": "A senha não pode ser igual ao usuário"}), 400

        # Validação completa (email + senha)
        erro = ValidarUsuario.validar_dados_usuarios(email, senha)
        if erro:
            return jsonify({'Mensagem': erro}), 400

        # Verifica se usuário já existe
        if Usuario.query.filter_by(email=email).first():
            return jsonify({"Mensagem": 'Usuário já existe no sistema'}), 409

        # Criptografia da senha
        senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')

        # Criação do usuário
        novo_user = Usuario(email=email, senha=senha_hash)
        db.session.add(novo_user)
        db.session.commit()

        return jsonify(novo_user.to_dict()), 201

    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({'Mensagem': 'Erro interno no servidor'}), 500


@auth_pb.post('/login')
def login():
    """
    Realiza autenticação do usuário e gera token JWT.

    Regras:
        - Email e senha não podem estar vazios
        - Usuário deve existir
        - Senha deve estar correta

    Fluxo:
        1. Recebe dados JSON (email, senha)
        2. Valida campos obrigatórios
        3. Busca usuário no banco
        4. Verifica senha com hash
        5. Gera token JWT

    Retorno:
        200: Login realizado com sucesso (retorna token)
        400: Campos inválidos
        401: Credenciais incorretas
        500: Erro interno no servidor
    """
    try:
        dados = request.get_json()

        # Validação de campos vazios
        if not dados.get('email') or not dados.get('senha'):
            return jsonify({'Mensagem': 'Os campo(s) estão vazios'}), 400

        # Busca usuário pelo email
        email = Usuario.query.filter_by(email=dados['email']).first()

        # Verifica se usuário existe e senha está correta
        if email is None or not bcrypt.check_password_hash(email.senha, dados['senha']):
            return jsonify({'Mensagem': 'Usuário ou senha estão incorretos'}), 401

        # Geração do token JWT
        token = create_access_token(identity=str(email.id))

        return jsonify({'token': token}), 200

    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({'Mensagem': 'Erro interno no servidor'}), 500