# SprintSync API 🐍
DRF-powered REST API for tasks and AI suggestions

# Overview 📗
This repository contains the backend for the SprintSync challenge. It’s a Django REST Framework API with JWT auth, `User` & `Task` models, clean CRUD endpoints, and an `/ai/suggest` stub. Local dev runs via Docker Compose with lightweight images.

# Data 🗂️
PostgreSQL is used locally via Docker. Configure DB settings through env vars:
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

# Product 📦
API endpoints (example):
- `POST /api/auth/login/` (JWT)
- `GET/POST /api/tasks/`
- `GET/PUT/PATCH/DELETE /api/tasks/{id}/`
- `POST /api/tasks/{id}/status/`
- `POST /api/ai/suggest/` (stub for now)

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