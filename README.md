# Identity Service

API de autenticação, autorização e gerenciamento de identidade desenvolvida com **FastAPI**, **Tortoise ORM**, **PostgreSQL**, **Redis** e **Aerich**.

O serviço fornece recursos para:

* Cadastro de usuários
* Autenticação
* Emissão e renovação de tokens
* Logout e revogação de sessões
* Recuperação de senha
* Redefinição de senha
* Consulta de usuários
* Atualização de dados de usuários
* Alteração de senha
* Exclusão de usuários
* Estrutura de papéis (`roles`) e regras (`rules`)

---

## Stack

| Tecnologia    | Finalidade                                        |
| ------------- | ------------------------------------------------- |
| Python 3.14   | Linguagem                                         |
| FastAPI       | Framework da API                                  |
| Uvicorn       | Servidor ASGI                                     |
| Tortoise ORM  | ORM                                               |
| PostgreSQL 17 | Banco de dados                                    |
| Aerich        | Migrations                                        |
| Redis 7       | Cache e infraestrutura de dados                   |
| Mailpit       | SMTP e visualização de e-mails em desenvolvimento |
| Poetry        | Gerenciamento de dependências                     |
| Docker        | Containerização                                   |
| Pydantic      | Validação de dados                                |

---

## Arquitetura

O projeto segue uma separação entre **rotas**, **serviços**, **schemas**, **modelos** e **componentes de infraestrutura**.

```text
.
├── main.py
├── migrations/
├── src/
│   ├── core/
│   │   └── security.py
│   │
│   ├── database.py
│   │
│   ├── models/
│   │   ├── password_reset_token.py
│   │   ├── refresh_token.py
│   │   ├── role.py
│   │   ├── rule.py
│   │   └── user.py
│   │
│   ├── routers/
│   │   ├── auth_router.py
│   │   ├── private_router.py
│   │   └── public_router.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   └── user.py
│   │
│   └── services/
│       ├── auth_service.py
│       └── user_service.py
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
└── README.md
```

### Responsabilidades

#### `routers`

Define os endpoints HTTP da aplicação.

#### `services`

Contém a lógica de negócio da aplicação.

#### `schemas`

Define os modelos de entrada e saída utilizados pela API através do Pydantic.

#### `models`

Define as entidades persistidas no PostgreSQL utilizando Tortoise ORM.

#### `core`

Contém componentes centrais da aplicação, como autenticação e segurança.

#### `migrations`

Contém as migrations gerenciadas pelo Aerich.

---

# Executando o projeto

## Pré-requisitos

Para executar localmente, tenha instalado:

* Python 3.14+
* Poetry
* PostgreSQL
* Redis

Para executar utilizando Docker:

* Docker
* Docker Compose

---

## Variáveis de ambiente

O projeto utiliza um arquivo `.env`.

Um exemplo básico pode ser:

```env
DATABASE_URL=postgres://postgres:postgres@postgres:5432/identity_db

REDIS_URL=redis://redis:6379

SECRET_KEY=change-me
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

SMTP_HOST=mailpit
SMTP_PORT=1025
```

Os nomes e valores das variáveis devem corresponder às configurações utilizadas em:

* `src.database`
* `src.core`
* serviços da aplicação

> **Importante:** nunca versione credenciais reais no repositório.

Recomenda-se manter um arquivo:

```text
.env.example
```

contendo os nomes das variáveis necessárias e valores seguros para desenvolvimento.

---

# Executando com Docker

O projeto possui um `docker-compose.yml` que inicializa os seguintes serviços:

* `identity-api`
* `identity-postgres`
* `identity-redis`
* `identity-mailpit`

### Iniciar os serviços

```bash
docker compose up --build
```

### Executar em segundo plano

```bash
docker compose up --build -d
```

### Parar os containers

```bash
docker compose down
```

---

# API

A API ficará disponível em:

```text
http://localhost:8000
```

## Swagger UI

A documentação interativa do FastAPI pode ser acessada em:

```text
http://localhost:8000/docs
```

## ReDoc

A documentação alternativa pode ser acessada em:

```text
http://localhost:8000/redoc
```

## OpenAPI

O schema OpenAPI pode ser acessado em:

```text
http://localhost:8000/openapi.json
```

---

# Serviços auxiliares

## PostgreSQL

O PostgreSQL é utilizado como banco de dados principal.

### Configuração do Docker Compose

| Configuração | Valor         |
| ------------ | ------------- |
| Host         | `localhost`   |
| Porta        | `5432`        |
| Database     | `identity_db` |
| User         | `postgres`    |
| Password     | `postgres`    |

Dentro da rede Docker, a aplicação deve utilizar:

```text
postgres:5432
```

como host do PostgreSQL.

---

## Redis

O Redis é executado na porta:

```text
6379
```

### Host local

```text
localhost:6379
```

### Dentro do Docker Compose

```text
redis:6379
```

---

## Mailpit

O Mailpit fornece um servidor SMTP para desenvolvimento e uma interface web para visualizar os e-mails enviados pela aplicação.

### SMTP

```text
localhost:1025
```

### Interface web

```text
http://localhost:8025
```

---

# Banco de dados

O projeto utiliza:

* **Tortoise ORM** para persistência
* **Aerich** para gerenciamento das migrations

A configuração do Tortoise está definida em:

```text
src.database.TORTOISE_ORM
```

e é referenciada no `main.py`.

O FastAPI registra o Tortoise através de:

```python
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)
```

O parâmetro:

```python
generate_schemas=False
```

indica que a estrutura do banco deve ser gerenciada através das migrations.

---

# Migrations com Aerich

## Criar uma migration

Depois de alterar os modelos:

```bash
aerich migrate
```

## Aplicar migrations

```bash
aerich upgrade
```

## Reverter a última migration

```bash
aerich downgrade
```

## Verificar o estado das migrations

```bash
aerich history
```

Dentro do container, pode ser necessário executar através do Poetry:

```bash
poetry run aerich upgrade
```

O Docker Compose executa automaticamente:

```bash
poetry run aerich upgrade
```

antes de iniciar o Uvicorn.

---

# API

A API está organizada em três grupos principais:

* Authentication
* Public
* Private

A autenticação dos endpoints protegidos é realizada através do mecanismo definido em:

```text
src.core.security.get_current_user
```

---

# Endpoint raiz

## `GET /`

Retorna uma mensagem indicando que o serviço está disponível.

### Resposta

```json
{
  "message": "Welcome to the Identity Service!"
}
```

---

# Authentication

**Prefixo:**

```text
/auth
```

Os endpoints dessa seção são responsáveis pela autenticação e gerenciamento de tokens.

---

## `POST /auth/login`

Autentica um usuário utilizando e-mail e senha.

### Request Body

```json
{
  "email": "usuario@example.com",
  "password": "senha123"
}
```

### Schema

```python
{
    "email": str,
    "password": str
}
```

### Exemplo

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "senha123"
  }'
```

### Resposta

A resposta é gerenciada por:

```text
AuthService.login()
```

O formato exato depende da implementação de:

```text
src.services.auth_service.AuthService.login
```

---

## `POST /auth/refresh`

Renova a autenticação utilizando um refresh token.

### Request Body

```json
{
  "refresh_token": "seu-refresh-token"
}
```

### Schema

```python
{
    "refresh_token": str
}
```

### Exemplo

```bash
curl -X POST "http://localhost:8000/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "seu-refresh-token"
  }'
```

A lógica de renovação é implementada por:

```text
AuthService.refresh_token()
```

---

## `POST /auth/logout`

Encerra a sessão do usuário autenticado.

### Autenticação

Obrigatória.

O endpoint utiliza:

```python
Depends(get_current_user)
```

### Exemplo

```bash
curl -X POST "http://localhost:8000/auth/logout" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

A operação é realizada por:

```text
AuthService.logout()
```

---

# Public

**Prefixo:**

```text
/created
```

Apesar do nome do router ser `public_router`, os endpoints atualmente registrados utilizam o prefixo `/created`.

---

## `POST /created/`

Cria um novo usuário.

### Autenticação

Não requerida.

### Request Body

```json
{
  "nome": "Lucas Oliveira",
  "email": "lucas@example.com",
  "password": "senha123"
}
```

### Regras de validação

| Campo      | Tipo   | Obrigatório | Regras             |
| ---------- | ------ | ----------- | ------------------ |
| `nome`     | string | Sim         | 2 a 100 caracteres |
| `email`    | email  | Sim         | 8 a 255 caracteres |
| `password` | string | Sim         | 6 a 255 caracteres |

### Status

```text
201 Created
```

### Exemplo

```bash
curl -X POST "http://localhost:8000/created/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Lucas Oliveira",
    "email": "lucas@example.com",
    "password": "senha123"
  }'
```

A lógica de criação está em:

```text
UserService.create_user()
```

---

## `POST /created/forgot-password`

Solicita recuperação de senha.

### Autenticação

Não requerida.

### Request Body

```json
{
  "email": "lucas@example.com"
}
```

### Status

```text
202 Accepted
```

### Exemplo

```bash
curl -X POST "http://localhost:8000/created/forgot-password" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "lucas@example.com"
  }'
```

A operação é realizada por:

```text
AuthService.forgot_password()
```

---

## `POST /created/reset-password`

Redefine a senha utilizando um token de recuperação.

### Autenticação

Não requerida.

### Request Body

```json
{
  "token": "token-de-recuperacao",
  "new_password": "nova-senha-segura"
}
```

### Regras

`new_password` deve possuir:

* mínimo de 8 caracteres
* máximo de 128 caracteres

### Status

```text
200 OK
```

### Exemplo

```bash
curl -X POST "http://localhost:8000/created/reset-password" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "token-de-recuperacao",
    "new_password": "nova-senha-segura"
  }'
```

A operação é realizada por:

```text
AuthService.reset_password()
```

---

# Private

**Prefixo:**

```text
/users
```

Todos os endpoints desse router possuem:

```python
dependencies=[Depends(get_current_user)]
```

Portanto, exigem autenticação.

O header esperado é:

```http
Authorization: Bearer SEU_ACCESS_TOKEN
```

---

## `GET /users/`

Retorna a lista de usuários.

### Autenticação

Obrigatória.

### Resposta

Lista de objetos `UserGet`.

```json
[
  {
    "id": 1,
    "nome": "Lucas Oliveira",
    "email": "lucas@example.com"
  }
]
```

### Exemplo

```bash
curl -X GET "http://localhost:8000/users/" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

### Status

```text
200 OK
```

---

## `GET /users/me`

Retorna os dados do usuário autenticado.

### Autenticação

Obrigatória.

### Resposta

```json
{
  "id": 1,
  "nome": "Lucas Oliveira",
  "email": "lucas@example.com"
}
```

### Exemplo

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

### Status

```text
200 OK
```

---

## `GET /users/{user_id}`

Busca um usuário pelo ID.

### Path Parameter

| Parâmetro | Tipo    | Descrição     |
| --------- | ------- | ------------- |
| `user_id` | integer | ID do usuário |

### Exemplo

```bash
curl -X GET "http://localhost:8000/users/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

### Status esperado

```text
200 OK
```

Caso o usuário não seja encontrado, a intenção da implementação é retornar:

```text
404 Not Found
```

> **Observação:** a implementação atual retorna `{404: "User not found"}` diretamente quando o usuário não existe, em vez de lançar `HTTPException(status_code=404, ...)`.
>
> Isso significa que o comportamento HTTP real pode não corresponder ao `404` pretendido. Recomenda-se corrigir esse ponto no serviço/router.

---

## `PUT /users/me`

Atualiza os dados do usuário autenticado.

### Autenticação

Obrigatória.

### Request Body

Todos os campos são opcionais.

```json
{
  "nome": "Novo Nome",
  "email": "novo@example.com",
  "password": "nova-senha"
}
```

### Schema

```python
{
    "nome": "string | null",
    "email": "string | null",
    "password": "string | null"
}
```

### Regras

| Campo      | Regras             |
| ---------- | ------------------ |
| `nome`     | 2 a 100 caracteres |
| `email`    | 8 a 255 caracteres |
| `password` | 6 a 255 caracteres |

### Exemplo

```bash
curl -X PUT "http://localhost:8000/users/me" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Novo Nome",
    "email": "novo@example.com"
  }'
```

### Status

```text
200 OK
```

---

## `PUT /users/{user_id}`

Atualiza um usuário através do ID.

### Autenticação

Obrigatória.

### Path Parameter

```text
user_id: integer
```

### Request Body

```json
{
  "nome": "Novo Nome",
  "email": "novo@example.com",
  "password": "nova-senha"
}
```

Todos os campos são opcionais.

### Exemplo

```bash
curl -X PUT "http://localhost:8000/users/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Novo Nome"
  }'
```

### Status

```text
200 OK
```

---

## `PATCH /users/me/password`

Altera a senha do usuário autenticado.

### Autenticação

Obrigatória.

### Request Body

```json
{
  "senha_atual": "senha-atual",
  "nova_senha": "nova-senha"
}
```

### Regras

| Campo         | Tipo   | Regras             |
| ------------- | ------ | ------------------ |
| `senha_atual` | string | 4 a 100 caracteres |
| `nova_senha`  | string | 6 a 255 caracteres |

### Exemplo

```bash
curl -X PATCH "http://localhost:8000/users/me/password" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "senha_atual": "senha-atual",
    "nova_senha": "nova-senha"
  }'
```

### Status

```text
204 No Content
```

---

## `DELETE /users/{user_id}`

Remove um usuário pelo ID.

### Autenticação

Obrigatória.

### Path Parameter

```text
user_id: integer
```

### Exemplo

```bash
curl -X DELETE "http://localhost:8000/users/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

### Resposta

```json
{
  "message": "Usuario deletado com sucesso"
}
```

### Status

```text
200 OK
```

---

# Schemas

## `UserCreate`

Utilizado no cadastro.

```json
{
  "nome": "Lucas Oliveira",
  "email": "lucas@example.com",
  "password": "senha123"
}
```

---

## `UserGet`

Representação pública básica de um usuário.

```json
{
  "id": 1,
  "nome": "Lucas Oliveira",
  "email": "lucas@example.com"
}
```

O campo `password_hash` não é exposto pelo schema.

---

## `UserUpdate`

Utilizado para atualização de dados.

```json
{
  "nome": "Novo Nome",
  "email": "novo@example.com",
  "password": "nova-senha"
}
```

Todos os campos são opcionais.

---

## `UserPasswordUpdate`

Utilizado especificamente para alteração de senha.

```json
{
  "senha_atual": "senha-atual",
  "nova_senha": "nova-senha"
}
```

---

## `Login`

```json
{
  "email": "lucas@example.com",
  "password": "senha123"
}
```

---

## `RefreshToken`

```json
{
  "refresh_token": "refresh-token"
}
```

---

## `ForgotPassword`

```json
{
  "email": "lucas@example.com"
}
```

---

## `ResetPassword`

```json
{
  "token": "token-de-recuperacao",
  "new_password": "nova-senha"
}
```

---

# Modelos do banco

## User

Representa um usuário da aplicação.

### Campos principais

| Campo           | Tipo     | Observação         |
| --------------- | -------- | ------------------ |
| `id`            | integer  | Primary key        |
| `nome`          | string   | Nome do usuário    |
| `email`         | string   | Único              |
| `password_hash` | string   | Hash da senha      |
| `criado_em`     | datetime | Data de criação    |
| `atualizado_em` | datetime | Última atualização |

### Tabela

```text
users
```

---

## RefreshToken

Armazena refresh tokens associados aos usuários.

### Campos

| Campo        | Tipo      |
| ------------ | --------- |
| `id`         | integer   |
| `token`      | string    |
| `user`       | FK → User |
| `expires_at` | datetime  |
| `created_at` | datetime  |
| `revoked`    | boolean   |

### Tabela

```text
refresh_tokens
```

O campo `revoked` indica se o token foi revogado.

---

## PasswordResetToken

Armazena tokens utilizados no fluxo de recuperação de senha.

### Campos

| Campo        | Tipo      |
| ------------ | --------- |
| `id`         | integer   |
| `user`       | FK → User |
| `token_hash` | string    |
| `expires_at` | datetime  |
| `used_at`    | datetime  |
| `created_at` | datetime  |

O token possui controle de:

* expiração
* utilização
* usuário associado
* hash do token
* data de criação

---

## Role

Representa um papel de autorização.

### Campos

| Campo           | Tipo     |
| --------------- | -------- |
| `id`            | integer  |
| `name`          | string   |
| `description`   | string   |
| `criado_em`     | datetime |
| `atualizado_em` | datetime |

### Tabela

```text
roles
```

Um `Role` possui relacionamento muitos-para-muitos com `Rule`.

---

## Rule

Representa uma regra de autorização.

### Campos

| Campo           | Tipo     |
| --------------- | -------- |
| `id`            | integer  |
| `name`          | string   |
| `description`   | string   |
| `resource`      | string   |
| `action`        | string   |
| `criado_em`     | datetime |
| `atualizado_em` | datetime |

### Tabela

```text
rules
```

Existe uma restrição de unicidade para:

```text
resource + action
```

---

# Fluxo de autenticação

O fluxo básico esperado é:

```text
                    ┌─────────────────┐
                    │  Criar usuário  │
                    │ POST /created/  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      Login      │
                    │ POST /auth/login│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Access Token +  │
                    │ Refresh Token   │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
       ┌─────────────────┐       ┌─────────────────┐
       │ Recursos        │       │ Access Token    │
       │ protegidos      │       │ expirado        │
       │ /users/...      │       │                 │
       └─────────────────┘       └────────┬────────┘
                                          │
                                          ▼
                                ┌─────────────────┐
                                │ POST /auth/     │
                                │ refresh         │
                                └─────────────────┘
```

Para recursos protegidos, o token deve ser enviado através do header:

```http
Authorization: Bearer SEU_ACCESS_TOKEN
```

---

# Recuperação de senha

O fluxo de recuperação utiliza dois endpoints públicos:

```text
POST /created/forgot-password
POST /created/reset-password
```

### Fluxo

```text
Usuário
   │
   │ POST /created/forgot-password
   │ email
   ▼
API
   │
   │ gera token
   ▼
E-mail
   │
   │ token de recuperação
   ▼
Usuário
   │
   │ POST /created/reset-password
   │ token + nova senha
   ▼
API
   │
   ▼
Senha atualizada
```

O projeto possui um modelo específico para armazenar os tokens:

```text
PasswordResetToken
```

com controle de:

* hash do token
* expiração
* utilização
* usuário associado
* data de criação

---

# Segurança

O projeto utiliza uma camada de segurança centralizada em:

```text
src/core/security.py
```

Os endpoints privados utilizam:

```python
Depends(get_current_user)
```

Isso permite centralizar a validação do usuário autenticado.

As senhas não devem ser armazenadas em texto puro.

O modelo `User` armazena:

```text
password_hash
```

em vez da senha original.

---

# Documentação automática

Como o projeto utiliza FastAPI, a especificação OpenAPI é gerada automaticamente.

## Swagger UI

```text
http://localhost:8000/docs
```

A interface permite:

* visualizar endpoints
* consultar schemas
* enviar requisições
* testar autenticação
* visualizar códigos HTTP
* consultar parâmetros
* consultar request bodies

## ReDoc

```text
http://localhost:8000/redoc
```

---

# Lista de endpoints

| Método   | Endpoint                   | Autenticação | Descrição                    |
| -------- | -------------------------- | ------------ | ---------------------------- |
| `GET`    | `/`                        | Não          | Health/welcome endpoint      |
| `POST`   | `/auth/login`              | Não          | Autenticação                 |
| `POST`   | `/auth/refresh`            | Não          | Renovação do token           |
| `POST`   | `/auth/logout`             | Sim          | Logout                       |
| `POST`   | `/created/`                | Não          | Cadastro de usuário          |
| `POST`   | `/created/forgot-password` | Não          | Solicitação de recuperação   |
| `POST`   | `/created/reset-password`  | Não          | Redefinição de senha         |
| `GET`    | `/users/`                  | Sim          | Lista usuários               |
| `GET`    | `/users/me`                | Sim          | Usuário autenticado          |
| `GET`    | `/users/{user_id}`         | Sim          | Busca usuário por ID         |
| `PUT`    | `/users/me`                | Sim          | Atualiza usuário autenticado |
| `PUT`    | `/users/{user_id}`         | Sim          | Atualiza usuário por ID      |
| `PATCH`  | `/users/me/password`       | Sim          | Altera senha                 |
| `DELETE` | `/users/{user_id}`         | Sim          | Remove usuário               |

---

# Desenvolvimento

## Instalar as dependências

```bash
poetry install
```

## Entrar no ambiente virtual

```bash
poetry shell
```

## Executar a aplicação

```bash
poetry run uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://localhost:8000
```

---

# Testes

## Executar os testes

```bash
poetry run pytest
```

## Executar com cobertura

```bash
poetry run pytest --cov
```

---

# Lint

O projeto utiliza **Ruff**.

## Verificar problemas

```bash
poetry run ruff check .
```

## Corrigir automaticamente quando possível

```bash
poetry run ruff check . --fix
```

---

# Pre-commit

Caso os hooks estejam configurados:

## Instalar os hooks

```bash
poetry run pre-commit install
```

## Executar manualmente

```bash
poetry run pre-commit run --all-files
```

---

# Docker em desenvolvimento

O serviço da API utiliza volumes para permitir hot reload:

```yaml
volumes:
  - .:/app
  - /app/.venv
```

O segundo volume é necessário para preservar o ambiente virtual criado dentro da imagem Docker, evitando que o bind mount:

```text
.:/app
```

esconda o `.venv`.

A API inicia executando:

```bash
poetry run aerich upgrade
```

e depois:

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

# Resumo

O **Identity Service** fornece uma base completa para gerenciamento de identidade, incluindo:

* autenticação com access token e refresh token
* gerenciamento de sessões
* cadastro e gerenciamento de usuários
* alteração e recuperação de senha
* autorização baseada em roles e rules
* persistência com PostgreSQL
* cache e infraestrutura com Redis
* envio de e-mails em desenvolvimento através do Mailpit
* migrations com Aerich
* documentação automática através do OpenAPI
* execução local ou containerizada com Docker

## Principais tecnologias

```text
FastAPI
Python 3.14
Tortoise ORM
PostgreSQL 17
Redis 7
Aerich
Mailpit
Poetry
Docker
Pydantic
```
