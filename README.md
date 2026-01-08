# FastAPI Tutorial Project

This project is for learning about building backend system using FastAPI.

--- 

### [Setup Instructions](#setup)

---

## Features:

- ### Users
    - [x] Create a user
    - [x] Get a user by their `id`
    - [x] Get all users `limit=10` and `offset=0`
    - [x] Update user
    - [x] Delete a `user`, ***corresponding*** `tasks` will be *deleted*
- ### Tasks
    - [x] Create a task
    - [x] Get all tasks of an `user`
    - [x] Get task by its `id`
    - [x] Update a task by its `id`
    - [x] Delete a task by its `id`
    - [x] Delete all `tasks` of a user
    - [x] Get `tasks` by their status(completed or not)
- ### Testing
  - [x] Test coverage
  - [x] Integration testing
    - [x] Users
    - [x] Tasks
  - [x] Migrations using Alembic
---

## Todo:

- [ ] Handle wrong `request` like `422` etc
- [ ] When `user` or `task` is updated, check if anything is changed or only few `fields` is updated
- [ ] Unit testing
- [ ] E2E testing
- [ ] Pagination
- [ ] Logging
- [ ] Authentication and Authorization
- [ ] Email verification
- [ ] Password Reset
- [ ] Account Recovery
- [ ] Process `requests` using multi-threading/multiprocessing
- [ ] Caching using `Redis`
- [ ] Message Queue - `Kafka` or `RabbitMQ`
- [ ] Background jobs. Maybe `Celery`
- [ ] Scheduled Jobs

---

## Package Manager:

- uv
- To view dependency tree:

    ```
    uv tree
    ```

---

## API Endpoints:

### Users:

| Method | Endpoint                  | Description                   |
|--------|---------------------------|-------------------------------|
| GET    | `/api/v1/users`           | Get all users                 |
| GET    | `/api/v1/users/{user_id}` | Get user by ID                |
| POST   | `/api/v1/users`           | Create a new user             |
| PATCH  | `/api/v1/users/{user_id}` | Update user                   |
| DELETE | `/api/v1/users/{user_id}` | Delete user (and their tasks) |

### Tasks:

| Method | Endpoint                              | Description                             |
|--------|---------------------------------------|-----------------------------------------|
| GET    | `/api/v1/tasks/{user_id}`             | Get tasks of a user                     |
| GET    | `/api/v1/tasks/{user_id}/{task_id}`   | Get task by ID                          |
| POST   | `/api/v1/tasks`                       | Create new task                         |
| PATCH  | `/api/v1/tasks`                       | Update task                             |
| DELETE | `/api/v1/tasks/{user_id}/{task_id}`   | Delete task by ID                       |
| DELETE | `/api/v1/tasks/{user_id}`             | Delete all tasks of a user              |
| GET    | `api/v1/status/{user_id}/{completed}` | Get all thsks of a user by their status |

--- 

## <div id="setup">Setup Instructions:</div>

1. Fork the Repository
2. Clone the Repository
   ```
   git clone git@github.com:<github_username>/FastApi-Tutorial.git
   cd FastApi-Tutorial
   ```  

3. If `uv` is installed, if not <a href="https://docs.astral.sh/uv/getting-started/installation/" target="_blank" rel="noopener noreferrer">
   follow the instructions
   </a>:
   ```
   source .venv/bin/activate
   uv sync
    ```
4. Set up environment variables by copying the example configuration:
   ```
   cp .env.example .ev
   ```
5. For migrations:
   ```
   alembic init alembic && alembic revision --autogenerate
   alembic upgrade head 
   ```
6. Make scripts executable:
   ```
   chmod +x dev.sh
   chmod +x prod.sh
   chmod +x tests.sh
   ```
7. Run the **development** server:
   ```
   ./dev.sh
   ```
8. Development server runs at: http://127.0.0.1:8000
9. OpenAPI docs at: http://127.0.0.1:8000/docs
10. To run the **production** server:
   ```
   ./prod.sh
   ```
