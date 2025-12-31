# FastAPI Tutorial Project

This project is for learning about building backend system using FastAPI.

--- 

### [Setup Instructions](#setup)

---

## Models:

- ### Users
    - [x] Create a user
    - [x] Get a user by their `id`
    - [x] Get all users `limit=10` and `offset=0`
    - [x] Update user
    - [x] Delete a `user`, ***corresponding*** `tasks` shall be *deleted* too
- ### Tasks
    - [x] Create a task
    - [x] Get all tasks of an `user`
    - [x] Get task by its `id`
    - [x] Update a task by its `id`
    - [x] Delete a task by its `id`
    - [x] Delete all `tasks` of a user

---

## Features:

- [ ] Pagination
- [ ] Unit testing - Pytest
- [ ] Authentication and Authorization
- [ ] Password Reset
- [ ] Account Recovery(?)
- [ ] E2E testing
- [ ] Process `requests` using multi-threading/multiprocessing
- [ ] Caching using `Redis`
- [ ] Message Queue - `Kafka` or `RabbitMQ`
- [ ] Background jobs. Maybe `Celery`
- [ ] Scheduled Jobs
- [ ] Email verification

---

## Package Manager:

- uv

---

## API Endpoints:

### Users:

| Method | Endpoint                  | Description                   |
|--------|---------------------------|-------------------------------|
| GET    | `/api/v1/users`           | Get all users                 |
| GET    | `/api/v1/users/{user_id}` | Get user by ID                |
| POST   | `/api/v1/users`           | Create a new user             |
| PATCH  | `/api/v1/users/{user_id}` | Update a user                 |
| DELETE | `/api/v1/users/{user_id}` | Delete user (and their tasks) |

### Tasks:

| Method | Endpoint                            | Description                 |
|--------|-------------------------------------|-----------------------------|
| GET    | `/api/v1/tasks/{user_id}`           | Get tasks for a user        |
| GET    | `/api/v1/tasks/{user_id}/{task_id}` | Get task by ID              |
| POST   | `/api/v1/tasks`                     | Create new task             |
| PATCH  | `/api/v1/tasks`                     | Update task                 |
| DELETE | `/api/v1/tasks/{user_id}/{task_id}` | Delete task by ID           |
| DELETE | `/api/v1/tasks/{user_id}`           | Delete all tasks for a user |

--- 

## <div id="setup">Setup Instructions:</div>

1. Fork the Repository
2. Clone the Repository
   ```
   git clone git@github.com:<github_username>/FastApi-Tutorial.git
   cd FastApi-Tutorial
   ```  

3. If `uv` package manager is not
   installed, [follow the instructions](https://docs.astral.sh/uv/getting-started/installation/)
4. If `uv` is already installed:
   ```
   source .venv/bin/activate
   uv sync
    ```
5. Make scripts executable:
   ```
   chmod +x dev.sh
   chmod +x prod.sh
   chmod +x tests.sh
   ```
6. Run the development server:
   ```
   ./dev.sh
   ```
7. Development server runs at: http://127.0.0.1:8000
8. OpenAPI docs at: http://127.0.0.1:8000/docs
9. To run the **production** server:
   ```
   ./prod.sh
   ```
