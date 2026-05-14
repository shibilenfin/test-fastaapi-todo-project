import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models.todo import Base, Todo
from app.repositories.todo_repository import TodoRepository


@pytest.mark.asyncio
async def test_get_pending_filters_and_paginates():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        repository = TodoRepository(session)
        todo1 = await repository.create("pending1", "Desc1")
        todo2 = await repository.create("pending2", "Desc2")
        todo3 = await repository.create("pending3", "Desc3")
        todo4 = await repository.create("done", "Desc4")
        await repository.update(todo4.id, None, None, True)

        pending = await repository.get_pending()
        assert len(pending) == 3
        assert all(item.completed is False for item in pending)
        assert [item.title for item in pending] == ["pending1", "pending2", "pending3"]

        page1 = await repository.get_pending(limit=2)
        assert len(page1) == 2
        assert [item.title for item in page1] == ["pending1", "pending2"]

        page2 = await repository.get_pending(skip=1, limit=2)
        assert len(page2) == 2
        assert [item.title for item in page2] == ["pending2", "pending3"]
