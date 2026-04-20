# API de Livros com Flask

API REST para gerenciamento de livros com autenticação JWT.

## Tecnologias
- Python + Flask
- SQLAlchemy (SQLite)
- JWT (autenticação)

## Como rodar# 📚 API de Gerenciamento de Livros com Autenticação JWT

API REST desenvolvida em **Python (Flask)** para gerenciamento de livros, com sistema completo de **registro, autenticação e autorização via JWT**, incluindo validações e testes automatizados.

---

## 🚀 Tecnologias utilizadas

* Python
* Flask
* Flask SQLAlchemy
* Flask JWT Extended
* Flask Bcrypt
* SQLite (ambiente de teste)
* Unittest

---

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Token)** para proteger rotas sensíveis.

Após o login, você receberá um token que deve ser enviado no header:

```
Authorization: Bearer SEU_TOKEN_AQUI
```

---

# 📌 ENDPOINTS

---

## 🧑‍💻 Registro de usuário

### `POST /registro`

Cria um novo usuário.

### 📥 Request

```json
{
  "email": "user@email.com",
  "senha": "Senha@123"
}
```

### 📤 Response (Sucesso - 201)

```json
{
  "id": 1,
  "email": "user@email.com"
}
```

### ❌ Possíveis erros

| Status | Motivo                     |
| ------ | -------------------------- |
| 400    | Campos vazios ou inválidos |
| 400    | Senha fraca                |
| 400    | Senha igual ao email       |
| 409    | Usuário já existe          |

---

## 🔑 Login

### `POST /login`

Autentica o usuário e retorna um token JWT.

### 📥 Request

```json
{
  "email": "user@email.com",
  "senha": "Senha@123"
}
```

### 📤 Response (Sucesso - 200)

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### ❌ Possíveis erros

| Status | Motivo                |
| ------ | --------------------- |
| 400    | Campos vazios         |
| 401    | Credenciais inválidas |

---

# 📚 LIVROS (CRUD)

---

## ➕ Criar livro

### `POST /add` 🔒

Requer autenticação.

### 📥 Request

```json
{
  "titulo": "Clean Code",
  "autor": "Robert C. Martin"
}
```

### 📤 Response (201)

```json
{
  "id": 1,
  "titulo": "Clean Code",
  "autor": "Robert C. Martin"
}
```

### ❌ Possíveis erros

| Status | Motivo              |
| ------ | ------------------- |
| 400    | Campos vazios       |
| 409    | Livro já cadastrado |
| 401    | Token inválido      |

---

## 📖 Listar livros

### `GET /list`

### 📤 Response (200)

```json
[
  {
    "id": 1,
    "titulo": "Clean Code",
    "autor": "Robert C. Martin"
  }
]
```

### ❌ Possíveis erros

| Status | Motivo                  |
| ------ | ----------------------- |
| 404    | Nenhum livro encontrado |

---

## 🔍 Buscar livro por ID

### `GET /buscar/<id>`

### 📤 Response (200)

```json
{
  "id": 1,
  "titulo": "Clean Code",
  "autor": "Robert C. Martin"
}
```

### ❌ Possíveis erros

| Status | Motivo               |
| ------ | -------------------- |
| 404    | Livro não encontrado |

---

## ✏️ Atualizar livro

### `PUT /atualizar/<id>` 🔒

### 📥 Request

```json
{
  "titulo": "Clean Code 2",
  "autor": "Robert Martin"
}
```

### 📤 Response (200)

```json
{
  "id": 1,
  "titulo": "Clean Code 2",
  "autor": "Robert Martin"
}
```

### ❌ Possíveis erros

| Status | Motivo               |
| ------ | -------------------- |
| 400    | Campos inválidos     |
| 404    | Livro não encontrado |
| 401    | Não autenticado      |

---

## ❌ Remover livro

### `DELETE /livros/<id>` 🔒

### 📤 Response (200)

```json
{
  "Mensagem": "Livro removido com sucesso!"
}
```

### ❌ Possíveis erros

| Status | Motivo               |
| ------ | -------------------- |
| 404    | Livro não encontrado |
| 401    | Não autenticado      |

---

# 🧪 Testes

O projeto possui cobertura de testes com `unittest`, incluindo:

* ✔ Validação de senha
* ✔ Validação de email
* ✔ Registro de usuário
* ✔ Login
* ✔ CRUD completo de livros
* ✔ Autenticação com JWT

Para rodar os testes:

```bash
python -m unittest discover
```

---

# 📌 Regras de validação

### Senha:

* Mínimo de 8 caracteres
* Letras maiúsculas e minúsculas
* Pelo menos 1 número
* Pelo menos 1 caractere especial
* Não pode conter sequências (123, abc, qwe)

### Email:

* Deve seguir formato válido (regex)

---

# 📦 Estrutura do Projeto

```
/app
/models
/routes
/tests
/validador
```

---

# 💡 Melhorias futuras

* Refresh Token
* Paginação de livros
* Filtro por autor/título
* Deploy (Render, Railway, etc.)
* Documentação com Swagger

---

# 👨‍💻 Autor

Projeto desenvolvido com foco em aprendizado de **backend**, incluindo boas práticas como:

* Separação de responsabilidades
* Validação de dados
* Testes automatizados
* Autenticação segura

---

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