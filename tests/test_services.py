import pytest
from unittest.mock import AsyncMock
from app.services.todo_service import TodoService
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.models.todo import Todo


@pytest.mark.asyncio
async def test_create_todo():
    mock_repo = AsyncMock()
    mock_repo.create.return_value = Todo(id=1, title="Test", description="Desc", completed=False)
    service = TodoService(mock_repo)
    todo_data = TodoCreate(title="Test", description="Desc")
    result = await service.create(todo_data)
    assert result.id == 1
    assert result.title == "Test"
    mock_repo.create.assert_called_once_with("Test", "Desc")


@pytest.mark.asyncio
async def test_create_todo_empty_title():
    mock_repo = AsyncMock()
    service = TodoService(mock_repo)
    todo_data = TodoCreate(title="", description="Desc")
    with pytest.raises(ValueError, match="Title cannot be empty"):
        await service.create(todo_data)


@pytest.mark.asyncio
async def test_get_all_todos():
    mock_repo = AsyncMock()
    mock_repo.get_all.return_value = [
        Todo(id=1, title="Test1", description=None, completed=False),
        Todo(id=2, title="Test2", description="Desc", completed=True)
    ]
    service = TodoService(mock_repo)
    result = await service.get_all()
    assert len(result) == 2
    assert result[0].title == "Test1"
    assert result[1].completed is True


@pytest.mark.asyncio
async def test_get_todo_by_id():
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = Todo(id=1, title="Test", description="Desc", completed=False)
    service = TodoService(mock_repo)
    result = await service.get_by_id(1)
    assert result.id == 1
    assert result.title == "Test"


@pytest.mark.asyncio
async def test_get_todo_by_id_not_found():
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None
    service = TodoService(mock_repo)
    result = await service.get_by_id(1)
    assert result is None


@pytest.mark.asyncio
async def test_update_todo():
    mock_repo = AsyncMock()
    mock_repo.update.return_value = Todo(id=1, title="Updated", description="Desc", completed=True)
    service = TodoService(mock_repo)
    todo_data = TodoUpdate(title="Updated", completed=True)
    result = await service.update(1, todo_data)
    assert result.title == "Updated"
    assert result.completed is True
    mock_repo.update.assert_called_once_with(1, "Updated", None, True)


@pytest.mark.asyncio
async def test_update_todo_empty_title():
    mock_repo = AsyncMock()
    service = TodoService(mock_repo)
    todo_data = TodoUpdate(title="")
    with pytest.raises(ValueError, match="Title cannot be empty"):
        await service.update(1, todo_data)


@pytest.mark.asyncio
async def test_delete_todo():
    mock_repo = AsyncMock()
    mock_repo.delete.return_value = True
    service = TodoService(mock_repo)
    result = await service.delete(1)
    assert result is True
    mock_repo.delete.assert_called_once_with(1)