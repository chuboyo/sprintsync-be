# SprintSync API 🐍
DRF-powered REST API for tasks and AI suggestions

# Overview 📗
This repository contains the backend for the SprintSync challenge. It’s a Django REST Framework API with JWT auth, `User` & `Task` models, clean CRUD endpoints, and OpenAI integration for task description generation. Local dev runs via Docker Compose with lightweight images.

# Data 🗂️
PostgreSQL is used locally via Docker. Configure DB settings through env vars:
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

# Product 📦
API endpoints (example):
- `GET/POST /api/v1/users/`
- `GET/PUT/PATCH/DELETE /api/v1/users/{id}/`
- `POST /api/v1/users/login/` (JWT)
- `GET/POST /api/v1/tasks/`
- `GET/PUT/PATCH/DELETE /api/v1/tasks/{id}/`
- `POST /api/v1/tasks/draft_description/` 
- `POST /api/v1/tasks/daily_summary/` 

# Implementation ⚙️
Tech:
- Django + DRF
- SimpleJWT
- PostgreSQL
- Docker & Docker Compose (lightweight images)

## Project Setup 
```bash
docker compose up --build
```