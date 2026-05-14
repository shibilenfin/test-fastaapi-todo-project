import os

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ...constants import DEFAULT_PAGE_SKIP, DEFAULT_PAGE_LIMIT, PAGE_LIMIT_MAX
from ...database import get_db
from ...repositories.todo_repository import TodoRepository
from ...services.todo_service import TodoService
from ...schemas.todo import TodoCreate, TodoUpdate, TodoResponse, DbCheckResponse

router = APIRouter()

def get_todo_service(session: AsyncSession = Depends(get_db)) -> TodoService:
    repository = TodoRepository(session)
    return TodoService(repository)

@router.post("/todos", response_model=TodoResponse)
async def create_todo(todo_data: TodoCreate, service: TodoService = Depends(get_todo_service)):
    try:
        return await service.create(todo_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/todos/db-check", response_model=DbCheckResponse)
async def db_check(service: TodoService = Depends(get_todo_service)):
    if os.getenv("ENABLE_DB_CHECK_ENDPOINT", "false").lower() not in ("1", "true", "yes"):
        raise HTTPException(status_code=404, detail="Not found")
    try:
        return await service.db_check()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/todos/pending", response_model=List[TodoResponse])
async def get_pending_todos(
    skip: int = Query(default=DEFAULT_PAGE_SKIP, ge=0),
    limit: int = Query(default=DEFAULT_PAGE_LIMIT, ge=1, le=PAGE_LIMIT_MAX),
    service: TodoService = Depends(get_todo_service),
):
    try:
        return await service.get_pending(skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/todos", response_model=List[TodoResponse])
async def get_todos(
    skip: int = Query(default=DEFAULT_PAGE_SKIP, ge=0),
    limit: int = Query(default=DEFAULT_PAGE_LIMIT, ge=1, le=PAGE_LIMIT_MAX),
    service: TodoService = Depends(get_todo_service),
):
    return await service.get_all(skip=skip, limit=limit)

@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    todo = await service.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo_data: TodoUpdate, service: TodoService = Depends(get_todo_service)):
    try:
        todo = await service.update(todo_id, todo_data)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    deleted = await service.delete(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}