# API de Livros com Flask

API REST para gerenciamento de livros com autenticação JWT.

## Tecnologias
- Python + Flask
- SQLAlchemy (SQLite)
- JWT (autenticação)

## Como rodar
1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Crie um arquivo `.env` com: `JWT_SECRET_KEY=sua_chave`
4. Rode: `python app.py`

## Rotas
| Método | Rota | Protegida |
|--------|------|-----------|
| GET | /list | ❌ |
| GET | /buscar/<id> | ❌ |
| POST | /add | ✅ |
| PUT | /atualizar/<id> | ✅ |
| DELETE | /livros/<id> | ✅ |
| POST | /registro | ❌ |
| POST | /login | ❌ |