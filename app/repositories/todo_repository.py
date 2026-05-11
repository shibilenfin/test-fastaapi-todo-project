from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..constants import DEFAULT_PAGE_SKIP, DEFAULT_PAGE_LIMIT
from ..models import Todo


class TodoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, title: str, description: str | None) -> Todo:
        todo = Todo(title=title, description=description)
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        return todo

    async def get_all(self) -> List[Todo]:
        result = await self.session.execute(select(Todo))
        return result.scalars().all()

    async def get_by_id(self, todo_id: int) -> Todo | None:
        result = await self.session.execute(select(Todo).where(Todo.id == todo_id))
        return result.scalar_one_or_none()

    async def get_pending(self, skip: int = DEFAULT_PAGE_SKIP, limit: int = DEFAULT_PAGE_LIMIT) -> List[Todo]:
        result = await self.session.execute(
            select(Todo)
            .where(Todo.completed.is_(False))
            .order_by(Todo.id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def update(self, todo_id: int, title: str | None, description: str | None, completed: bool | None) -> Todo | None:
        todo = await self.get_by_id(todo_id)
        if not todo:
            return None
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if completed is not None:
            todo.completed = completed
        await self.session.commit()
        return todo

    async def delete(self, todo_id: int) -> bool:
        result = await self.session.execute(delete(Todo).where(Todo.id == todo_id))
        await self.session.commit()
        return result.rowcount > 0