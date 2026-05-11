# FastAPI Todo Application

A simple CRUD todo application built with FastAPI, following strict architectural rules.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `uvicorn app.main:app --reload`
3. Access API docs at http://localhost:8000/docs

## Architecture

- Models: ORM entities
- Repositories: DB access
- Services: Business logic
- API/Routes: HTTP layer
- Schemas: Pydantic DTOs
- Utils: Helpers