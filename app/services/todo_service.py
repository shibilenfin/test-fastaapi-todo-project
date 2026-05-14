from typing import List
from ..constants import DEFAULT_PAGE_SKIP, DEFAULT_PAGE_LIMIT, PAGE_LIMIT_MAX
from ..repositories.todo_repository import TodoRepository
from ..schemas.todo import TodoCreate, TodoUpdate, TodoResponse, DbCheckResponse


class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def create(self, todo_data: TodoCreate) -> TodoResponse:
        if not todo_data.title.strip():
            raise ValueError("Title cannot be empty")
        todo = await self.repository.create(todo_data.title, todo_data.description)
        return TodoResponse.from_orm(todo)

    async def get_all(self, skip: int = DEFAULT_PAGE_SKIP, limit: int = DEFAULT_PAGE_LIMIT) -> List[TodoResponse]:
        todos = await self.repository.get_all(skip=skip, limit=limit)
        return [TodoResponse.from_orm(todo) for todo in todos]

    async def get_pending(self, skip: int = DEFAULT_PAGE_SKIP, limit: int = DEFAULT_PAGE_LIMIT) -> List[TodoResponse]:
        todos = await self.repository.get_pending(skip=skip, limit=limit)
        return [TodoResponse.from_orm(todo) for todo in todos]

    async def get_by_id(self, todo_id: int) -> TodoResponse | None:
        todo = await self.repository.get_by_id(todo_id)
        return TodoResponse.from_orm(todo) if todo else None

    async def update(self, todo_id: int, todo_data: TodoUpdate) -> TodoResponse | None:
        if todo_data.title is not None and not todo_data.title.strip():
            raise ValueError("Title cannot be empty")
        todo = await self.repository.update(todo_id, todo_data.title, todo_data.description, todo_data.completed)
        return TodoResponse.from_orm(todo) if todo else None

    async def delete(self, todo_id: int) -> bool:
        return await self.repository.delete(todo_id)

    async def db_check(self) -> DbCheckResponse:
        todo = await self.repository.create("bot-check", "PR reviewer bot DB endpoint")
        stored_todo = await self.repository.get_by_id(todo.id)
        if not stored_todo:
            raise ValueError("Failed to read created todo")

        updated_todo = await self.repository.update(stored_todo.id, "bot-check-updated", None, None)
        if not updated_todo:
            raise ValueError("Failed to update created todo")

        deleted = await self.repository.delete(updated_todo.id)
        if not deleted:
            raise ValueError("Failed to delete created todo")

        return DbCheckResponse(
            created_id=todo.id,
            title_after_update=updated_todo.title,
            deleted=deleted,
        )

    async def get_by_id(self, todo_id: int) -> TodoResponse | None:
        todo = await self.repository.get_by_id(todo_id)
        return TodoResponse.from_orm(todo) if todo else None

    async def update(self, todo_id: int, todo_data: TodoUpdate) -> TodoResponse | None:
        if todo_data.title is not None and not todo_data.title.strip():
            raise ValueError("Title cannot be empty")
        todo = await self.repository.update(todo_id, todo_data.title, todo_data.description, todo_data.completed)
        return TodoResponse.from_orm(todo) if todo else None

    async def delete(self, todo_id: int) -> bool:
        return await self.repository.delete(todo_id)