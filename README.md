# Atlas

Atlas is a universal tracking platform for building broad software engineering skills across multiple languages and frameworks.
This Phase 1 implementation is a Python backend built with FastAPI, PostgreSQL, Alembic, and Pytest.

## Features
- JWT authentication
- CRUD for items
- Categories and tags
- Search and filtering 
- Pagination
- Input validation and error handling

## Tech Stack
- Python 3.13
- FastAPI
- PostgreSQL 
- SQLAlchemy + Alembic
- Pytest
- Docker + Docker Compose

## How to Run (Docker)
Prereqs: Docker Desktop installed and running.

1) Created a '.env' file in the repo root:
    - DATABASE_URL=your_database_url
    - SECRET_KEY=your_secret_key
2) Build and start containers:
   - docker compose up --build
3) Run migrations:
   - docker compose exec web alembic upgrade head
4) Open the app:
   - Health check: "http://127.0.0.1:8000/health'
   - API docs: 'http://127.0.0.1:8000/docs'

## How to Run (Local)
Prereqs: Python 3.13, Postgres running locally

1) Create and activate a virtual environment:
    - python -m venv .venv
    - .venv/Scripts/Activate.ps1
2) Install dependencies:
   - pip install -r requirements.txt
3) Set '.env' for local DB:
    - DATABASE_URL=your_database_url
    - SECRET_KEY=your_secret_key
4) Run migrations:
   - alembic upgrade head
5) Start the server:
   - uvicorn app.main:app --reload

## Running Tests
Set 'TEST_DATABASE_URL' in your environment (or '.env') and run:
 - pytest

## Notes
- Docker uses service name 'db' as the Postgres host.
   - ex. DATABASE_URL=postgresql+psycopg://{username}:{password}@**db**:{port_number}/{db_name} -> Docker
- Local runs use 'localhost' instead.
  - ex. DATABASE_URL=postgresql+psycopg://{username}:{password}@**localhost**:{port_number}/{db_name} -> Local