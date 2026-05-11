from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_todo():
    response = client.post("/todos", json={"title": "Test Todo", "description": "Test Desc"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Desc"
    assert data["completed"] is False
    todo_id = data["id"]

    # Clean up
    client.delete(f"/todos/{todo_id}")

def test_create_todo_empty_title():
    response = client.post("/todos", json={"title": "", "description": "Test"})
    assert response.status_code == 400
    assert "Title cannot be empty" in response.json()["detail"]

def test_get_todos_empty():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_get_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert "Todo not found" in response.json()["detail"]

def test_update_todo():
    # Create first
    create_response = client.post("/todos", json={"title": "Test", "description": "Desc"})
    todo_id = create_response.json()["id"]

    update_response = client.put(f"/todos/{todo_id}", json={"title": "Updated", "completed": True})
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True

    # Clean up
    client.delete(f"/todos/{todo_id}")

def test_delete_todo():
    # Create first
    create_response = client.post("/todos", json={"title": "Test"})
    todo_id = create_response.json()["id"]

    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Todo deleted"}

    # Check not found
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404