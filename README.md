# FastAPI Tutorial Project

This project is for learning about building backend system using FastAPI.

--- 

## Features:

- ### Users
  - [x] Create a user
  - [x] Get a user by their `id`
  - [x] Get all users `limit=10` and `offset=0`
  - [x] Update user
  - [ ] Delete a user
- ### Tasks
  - [x] Create a task
  - [x] Get all tasks of an `user`
  - [x] Get task by its `id`
  - [x] Update a task by its `id`
  - [x] Delete a task by its `id`
  - [x] Delete all `tasks` of a user

---

## Todos:

- [ ] When a `user` is deleted, ***corresponding*** `tasks` shall be *deleted* too
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

## API Endpoints

### Users:

- `GET` `/api/v1/users` - Get all `user` details
- `GET` `/api/v1/users/{user_id}` - A user by their `id`
- `POST` `/api/v1/users` - Create a new user
- `PATCH` `/api/v1/users/{user_id}` - Update `user` details
- `DELETE` `/api/v1/users/{user_id}` - Delete `user` by their `id` and their corresponding `tasks`

### Tasks:

- `GET` `/api/v1/tasks/{user_id}` - Get all tasks of a `user`
- `GET` `/api/v1/tasks/{user_id}/{task_id}` - Get `Task` details by its `id`
- `POST` `/api/v1/tasks` - Create a new task for a `user`
- `PATCH` `/api/v1/tasks` - Update `task` details
- `DELETE` `/api/v1/tasks/{user_id}/{task_id}` - Delete a `task` by its `id`
- `DELETE` `/api/v1/tasks/{user_id}` - Deletes all the `tasks` of a `user`
