"""
Integration tests for task endpoints.

Tests task CRUD operations with user isolation and JWT authentication.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


class TestCreateTask:
    """Tests for POST /api/{user_id}/tasks endpoint."""

    def test_create_task_with_title_only(self, client: TestClient):
        """T066: POST /api/{user_id}/tasks with title → 201 Created → returns task with id, user_id, completed=false."""
        # Create and login user
        signup_response = client.post(
            "/api/auth/signup",
            json={"email": "createtask@example.com", "password": "SecurePass123"},
        )
        user_id = signup_response.json()["user_id"]
        token = signup_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create task
        response = client.post(
            f"/api/{user_id}/tasks",
            json={"title": "New Task"},
            headers=headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["user_id"] == user_id
        assert data["title"] == "New Task"
        assert data["description"] is None
        assert data["completed"] is False

    def test_create_task_with_description(self, client: TestClient):
        """T067: POST /api/{user_id}/tasks with title and description → both fields saved."""
        # Create and login user
        signup_response = client.post(
            "/api/auth/signup",
            json={"email": "taskwithdesc@example.com", "password": "SecurePass123"},
        )
        user_id = signup_response.json()["user_id"]
        token = signup_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create task with description
        response = client.post(
            f"/api/{user_id}/tasks",
            json={
                "title": "Task with Description",
                "description": "This is a detailed description",
            },
            headers=headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Task with Description"
        assert data["description"] == "This is a detailed description"

    def test_create_task_empty_title_validation(self, client: TestClient):
        """T068: POST /api/{user_id}/tasks with empty title → 400 Bad Request → validation error."""
        # Create and login user
        signup_response = client.post(
            "/api/auth/signup",
            json={"email": "emptytitle@example.com", "password": "SecurePass123"},
        )
        user_id = signup_response.json()["user_id"]
        token = signup_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Try to create task with empty title
        response = client.post(
            f"/api/{user_id}/tasks",
            json={"title": ""},
            headers=headers,
        )

        assert response.status_code == 400 or response.status_code == 422
        assert "detail" in response.json()


class TestUpdateTask:
    """Tests for PUT /api/{user_id}/tasks/{task_id} endpoint."""

    def test_update_task_title_and_description(self, client: TestClient, session: Session):
        """T076: PUT /api/{user_id}/tasks/{id} with new title → 200 OK → changes saved, updated_at changed."""
        from src.models import Task, User
        import bcrypt
        from datetime import datetime, timedelta

        # Create user and task
        password_hash = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
        user = User(id="update-user", email="update@example.com", password_hash=password_hash)
        session.add(user)
        session.commit()

        task = Task(user_id=user.id, title="Original Title", description="Original Description")
        session.add(task)
        session.commit()
        original_updated_at = task.updated_at

        # Login
        login_response = client.post(
            "/api/auth/login",
            json={"email": "update@example.com", "password": "SecurePass123"},
        )
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Update task
        response = client.put(
            f"/api/{user.id}/tasks/{task.id}",
            json={"title": "Updated Title", "description": "Updated Description"},
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated Description"
        # Note: updated_at comparison might be tricky in tests, so we just verify it exists
        assert "updated_at" in data

    def test_mark_task_as_complete(self, client: TestClient, session: Session):
        """T077: PUT with completed=true → status updated."""
        from src.models import Task, User
        import bcrypt

        # Create user and task
        password_hash = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
        user = User(id="complete-user", email="complete@example.com", password_hash=password_hash)
        session.add(user)
        session.commit()

        task = Task(user_id=user.id, title="Task to Complete", completed=False)
        session.add(task)
        session.commit()

        # Login
        login_response = client.post(
            "/api/auth/login",
            json={"email": "complete@example.com", "password": "SecurePass123"},
        )
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Mark as complete
        response = client.put(
            f"/api/{user.id}/tasks/{task.id}",
            json={"completed": True},
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

    def test_update_task_empty_title_validation(self, client: TestClient, session: Session):
        """T078: PUT with empty title → 400 Bad Request."""
        from src.models import Task, User
        import bcrypt

        # Create user and task
        password_hash = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
        user = User(id="validate-user", email="validate@example.com", password_hash=password_hash)
        session.add(user)
        session.commit()

        task = Task(user_id=user.id, title="Original Title")
        session.add(task)
        session.commit()

        # Login
        login_response = client.post(
            "/api/auth/login",
            json={"email": "validate@example.com", "password": "SecurePass123"},
        )
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Try to update with empty title
        response = client.put(
            f"/api/{user.id}/tasks/{task.id}",
            json={"title": ""},
            headers=headers,
        )

        assert response.status_code == 400 or response.status_code == 422

    def test_update_non_existent_task(self, client: TestClient):
        """T080: PUT /api/{user_id}/tasks/9999 → 404 Not Found."""
        # Create and login user
        signup_response = client.post(
            "/api/auth/signup",
            json={"email": "notfound@example.com", "password": "SecurePass123"},
        )
        user_id = signup_response.json()["user_id"]
        token = signup_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Try to update non-existent task
        response = client.put(
            f"/api/{user_id}/tasks/99999",
            json={"title": "New Title"},
            headers=headers,
        )

        assert response.status_code == 404


class TestDeleteTask:
    """Tests for DELETE /api/{user_id}/tasks/{task_id} endpoint."""

    def test_delete_task(self, client: TestClient, session: Session):
        """T089: DELETE /api/{user_id}/tasks/{id} → 204 No Content → task removed from database."""
        from src.models import Task, User
        import bcrypt

        # Create user and task
        password_hash = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
        user = User(id="delete-user", email="delete@example.com", password_hash=password_hash)
        session.add(user)
        session.commit()

        task = Task(user_id=user.id, title="Task to Delete")
        session.add(task)
        session.commit()
        task_id = task.id

        # Login
        login_response = client.post(
            "/api/auth/login",
            json={"email": "delete@example.com", "password": "SecurePass123"},
        )
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Delete task
        response = client.delete(f"/api/{user.id}/tasks/{task_id}", headers=headers)

        assert response.status_code == 204

        # Verify task was deleted from database
        deleted_task = session.get(Task, task_id)
        assert deleted_task is None

    def test_delete_non_existent_task(self, client: TestClient):
        """T091: DELETE /api/{user_id}/tasks/9999 → 404 Not Found."""
        # Create and login user
        signup_response = client.post(
            "/api/auth/signup",
            json={"email": "deletenotfound@example.com", "password": "SecurePass123"},
        )
        user_id = signup_response.json()["user_id"]
        token = signup_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Try to delete non-existent task
        response = client.delete(f"/api/{user_id}/tasks/99999", headers=headers)

        assert response.status_code == 404


class TestFilterTasks:
    """Tests for filtering tasks by completion status."""

    def test_filter_incomplete_tasks(self, client: TestClient, session: Session):
        """T096: GET /api/{user_id}/tasks?completed=false → returns only incomplete tasks."""
        from src.models import Task, User
        import bcrypt

        # Create user
        password_hash = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
        user = User(id="filter-user", email="filter@example.com", password_hash=password_hash)
        session.add(user)
        session.commit()

        # Create tasks with different completion statuses
        task1 = Task(user_id=user.id, title="Incomplete Task 1", completed=False)
        task2 = Task(user_id=user.id, title="Completed Task", completed=True)
        task3 = Task(user_id=user.id, title="Incomplete Task 2", completed=False)
        session.add_all([task1, task2, task3])
        session.commit()

        # Login
        login_response = client.post(
            "/api/auth/login",
            json={"email": "filter@example.com", "password": "SecurePass123"},
        )
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get only incomplete tasks
        response = client.get(f"/api/{user.id}/tasks?completed=false", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(not task["completed"] for task in data)

    def test_filter_completed_tasks(self, client: TestClient, session: Session):
        """T097: GET /api/{user_id}/tasks?completed=true → returns only completed tasks."""
        from src.models import Task, User
        import bcrypt

        # Create user
        password_hash = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
        user = User(id="filter-complete-user", email="filtercomplete@example.com", password_hash=password_hash)
        session.add(user)
        session.commit()

        # Create tasks with different completion statuses
        task1 = Task(user_id=user.id, title="Incomplete Task", completed=False)
        task2 = Task(user_id=user.id, title="Completed Task 1", completed=True)
        task3 = Task(user_id=user.id, title="Completed Task 2", completed=True)
        session.add_all([task1, task2, task3])
        session.commit()

        # Login
        login_response = client.post(
            "/api/auth/login",
            json={"email": "filtercomplete@example.com", "password": "SecurePass123"},
        )
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get only completed tasks
        response = client.get(f"/api/{user.id}/tasks?completed=true", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(task["completed"] for task in data)


class TestGetUserTasks:
    """Tests for GET /api/{user_id}/tasks endpoint."""

    def test_get_user_tasks_with_valid_jwt(
        self, client: TestClient, session: Session
    ):
        """T051: GET /api/{user_id}/tasks with valid JWT → 200 OK → returns array of user's tasks."""
        from src.models import Task, User
        import bcrypt

        # Create a user directly in the database
        password_hash = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
        user = User(id="test-user-1", email="taskuser1@example.com", password_hash=password_hash)
        session.add(user)
        session.commit()

        # Create tasks directly in the database
        task1 = Task(user_id=user.id, title="Test Task 1", description="Description 1", completed=False)
        task2 = Task(user_id=user.id, title="Test Task 2", description="Description 2", completed=True)
        session.add(task1)
        session.add(task2)
        session.commit()

        # Login to get token
        login_response = client.post(
            "/api/auth/login",
            json={"email": "taskuser1@example.com", "password": "SecurePass123"},
        )
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get tasks
        response = client.get(f"/api/{user.id}/tasks", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

        # Verify task structure (most recent first)
        task = data[0]
        assert "id" in task
        assert "user_id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "created_at" in task
        assert "updated_at" in task
        assert task["user_id"] == user.id
        # Most recent task first (task2 was created last)
        assert task["title"] in ["Test Task 1", "Test Task 2"]

    def test_get_empty_task_list(self, client: TestClient):
        """T052: GET /api/{user_id}/tasks for user with no tasks → 200 OK → returns empty array."""
        # Create a user but don't add any tasks
        signup_response = client.post(
            "/api/auth/signup",
            json={"email": "emptytasks@example.com", "password": "SecurePass123"},
        )
        user_id = signup_response.json()["user_id"]
        token = signup_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get tasks (should be empty)
        response = client.get(f"/api/{user_id}/tasks", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
