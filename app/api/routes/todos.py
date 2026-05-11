from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ...database import get_db
from ...models.todo import Todo
from ...repositories.todo_repository import TodoRepository
from ...services.todo_service import TodoService
from ...schemas.todo import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter()

async def query_pending_todos(session: AsyncSession) -> List[Todo]:
    result = await session.execute(select(Todo).where(Todo.completed == False))
    return result.scalars().all()

@router.get("/todos/pending", response_model=List[TodoResponse])
async def get_pending_todos_direct(session: AsyncSession = Depends(get_db)):
    todos = await query_pending_todos(session)
    if not todos:
        raise HTTPException(status_code=404, detail="No pending todos found")
    return todos



def get_todo_service(session: AsyncSession = Depends(get_db)) -> TodoService:
    repository = TodoRepository(session)
    return TodoService(repository)

@router.post("/todos", response_model=TodoResponse)
async def create_todo(todo_data: TodoCreate, service: TodoService = Depends(get_todo_service)):
    try:
        return await service.create(todo_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/todos", response_model=List[TodoResponse])
async def get_todos(service: TodoService = Depends(get_todo_service)):
    return await service.get_all()

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