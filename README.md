<h1 align="center">Task Manager API</h1>

## 📋 Descrição

A **Task Manager API** é uma aplicação construída com Flask para gerenciar tarefas e integrar eventos com o Google Calendar. A API permite criar, atualizar, listar e deletar tarefas, além de agendar eventos no Google Calendar automaticamente com base nas tarefas criadas.

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Marshmallow
- Flasgger (para documentação automática com Swagger)
- Google Calendar API

## 🛠️ Instalação e Configuração

### 1. Clone o repositório

### 2. Instale as dependências

pip install requirements.txt

### 3. Execute

python app.py

### 4. Autenticação
**Registrar um Usuário**

- **Método:** `POST`
- **URL:** `http://localhost:5000/register/`
- **Headers:**
  - `Content-Type: application/json`
- **Body (JSON):**
  ```json
  {
      "username": "testuser",
      "password": "testpassword"
  }
  ```
- **Descrição:** Isso cria um novo usuário no sistema.

**Fazer Login**

- **Método:** `POST`
- **URL:** `http://localhost:5000/login/`
- **Headers:**
  - `Content-Type: application/json`
- **Body (JSON):**

  ```json
  {
      "username": "testuser",
      "password": "testpassword"
  }
  ```

- **Descrição:** Isso retorna um token JWT que você usará para autenticar as próximas requisições.
- **Resposta esperada:**

  ```json
  {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
**Nota:** Copie o valor de `access_token`, pois você precisará dele para autenticação nas próximas requisições.

Ao criar uma nova tarefa ou acessar quaisquer outros endpoints da API, você terá que utilizar o Token gerado;
Authorization > Auth Type > Bearer Token > Token

## 📝 Endpoints da API

A documentação completa dos endpoints está disponível em `/apidocs`. Abaixo, uma breve descrição dos principais endpoints:

- **`POST /tarefas/`**: Cria uma nova tarefa e agenda um evento no Google Calendar.
- **`GET /tarefas/`**: Lista todas as tarefas.
- **`GET /tarefas/<int:tarefa_id>/`**: Obtém uma tarefa específica pelo ID.
- **`PUT /tarefas/<int:tarefa_id>/`**: Atualiza uma tarefa existente.
- **`DELETE /tarefas/<int:tarefa_id>/`**: Deleta uma tarefa existente.

### 4. Configuração do Google Calendar API

1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
2. Ative a Google Calendar API para o projeto.
3. Crie credenciais OAuth 2.0 e baixe o arquivo `credentials.json`.
4. Coloque o arquivo `credentials.json` no diretório raiz do projeto.
5. Crie um arquivo `.env` no diretório raiz do projeto e adicione suas credenciais:

```bash
GOOGLE_CLIENT_ID=<seu-client-id>
GOOGLE_CLIENT_SECRET=<seu-client-secret>
```

### 5. Inicie a aplicação

```bash
flask run
```

### 6. Autenticação Google OAuth 2.0

Na primeira execução, a aplicação abrirá uma janela do navegador para autenticação na Google Calendar API. Após autenticar, será gerado o arquivo `token.json` que será utilizado para futuras autenticações.

## 🔒 Segurança

A API usa JWT (JSON Web Token) para autenticação e autorização. Para acessar os endpoints protegidos, inclua o token JWT no cabeçalho da solicitação.

## 🛡️ Melhorando a Segurança

- **Nunca** compartilhe arquivos sensíveis como `credentials.json` ou `token.json`.
- Use variáveis de ambiente para gerenciar informações sensíveis.
- Configure seu `.gitignore` para ignorar arquivos que contêm informações sensíveis.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
