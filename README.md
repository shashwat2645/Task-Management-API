# Task Management API

A FastAPI backend for managing **users** and **tasks**, with **JWT authentication** and **PostgreSQL** persistence (SQLAlchemy).

---

## Features
- User registration and login
- JWT-protected task APIs
- CRUD-style operations for tasks

---

## Tech stack
- **FastAPI** (API framework)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (database)
- **Pydantic** / **pydantic-settings** (schemas & configuration)
- **JWT** (authentication)
- **pwdlib** (password hashing)

---

## Project structure (high level)
- `main.py`: FastAPI app + router inclusion
- `src/user/*`: user models, routes, and controller (register/login)
- `src/tasks/*`: task routes, DTOs, controller (task CRUD)
- `src/utils/*`:
  - `db.py`: SQLAlchemy engine + session dependency
  - `settings.py`: environment configuration
  - `helpers.py`: JWT auth dependency

---

## Environment variables
The app reads these variables from `.env` (via `pydantic-settings`):

- `DB_CONNECTION` (string)
  - SQLAlchemy DB URL, e.g. `postgresql+psycopg2://user:password@localhost:5432/task_management`
- `SECRET_KEY` (string)
  - JWT signing key
- `ALGORITHM` (string)
  - JWT algorithm (e.g. `HS256`)
- `EXP_TIME` (int)
  - JWT expiry time in **minutes**

> Example `.env`
```bash
DB_CONNECTION=postgresql+psycopg2://postgres:postgres@localhost:5432/task_management
SECRET_KEY=your-secret-key
ALGORITHM=HS256
EXP_TIME=60
```

---

## Database tables
Based on SQLAlchemy models:

### `users`
- `id` (int, primary key)
- `name` (string)
- `username` (string, unique)
- `email` (string, unique)
- `password_hash` (string)

### `tasks`
- `id` (int, primary key)
- `title` (string)
- `description` (string)
- `is_completed` (boolean, default `false`)

---

## Authentication (JWT)
1. `POST /user/register` to create an account
2. `POST /user/login` to get a JWT token
3. Call task endpoints by sending:
   - `Authorization: Bearer <token>`

The auth dependency validates the token and loads the user.

---

## API reference
### Users (`/user`)

#### 1) Register
- **POST** `/user/register`
- Body: `UserSchema`
  - `name`: string
  - `username`: string
  - `email`: string
  - `password`: string
- Response: created user (as returned by controller)

```bash
curl -X POST http://localhost:8000/user/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","username":"alice","email":"alice@example.com","password":"password123"}'
```

#### 2) Login
- **POST** `/user/login`
- Body: `LoginSchema`
  - `username`: string
  - `password`: string
- Response:
  - `{ "token": "<jwt>" }`

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}' | jq -r .token)

echo $TOKEN
```

#### 3) Check auth
- **GET** `/user/is_auth`
- Note: in this project it accepts `db` and `request`.
- Uses JWT from `Authorization` header.

```bash
curl -X GET http://localhost:8000/user/is_auth \
  -H "Authorization: Bearer $TOKEN"
```

---

### Tasks (`/tasks`) — protected endpoints
All `/tasks` endpoints require authentication.

#### 1) Create task
- **POST** `/tasks/create`
- Body: `TaskSchema`
  - `title`: string
  - `description`: string
  - `is_completed`: boolean (optional, default `false`)

```bash
curl -X POST http://localhost:8000/tasks/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","description":"2 liters","is_completed":false}'
```

#### 2) Get all tasks
- **GET** `/tasks/get_tasks`

```bash
curl -X GET http://localhost:8000/tasks/get_tasks \
  -H "Authorization: Bearer $TOKEN"
```

#### 3) Get one task
- **GET** `/tasks/get_task/{task_id}`

```bash
curl -X GET http://localhost:8000/tasks/get_task/1 \
  -H "Authorization: Bearer $TOKEN"
```

#### 4) Update task
- **PUT** `/tasks/update_task/{task_id}`
- Body: `TaskSchema`

```bash
curl -X PUT http://localhost:8000/tasks/update_task/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","description":"2 liters + bread","is_completed":true}'
```

#### 5) Delete task
- **DELETE** `/tasks/delete_task/{task_id}`

```bash
curl -X DELETE http://localhost:8000/tasks/delete_task/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Running the app
1. Create a virtual environment (recommended)
2. Install dependencies (managed by `pyproject.toml`)
3. Provide a `.env` file
4. Start FastAPI

Typical run command (depends on your setup):
```bash
uvicorn main:app --reload --port 8000
```

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Notes / current behavior
- Task DTO/response schema currently omits `description` and `is_completed` fields from `TaskResponseSchema` (it returns at least `id` and `title`).
- For task operations, the controller uses primary key lookup via SQLAlchemy ORM `.get()`.

---

## License
(Add your license information here.)

