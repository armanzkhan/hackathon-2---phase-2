"""
Integration tests for user isolation and security.

Tests that users can only access their own tasks and enforce 403 Forbidden on cross-user access.
"""

import pytest
from fastapi.testclient import TestClient


class TestUserIsolation:
    """Tests for user isolation enforcement."""

    def test_user_cannot_access_other_user_tasks(self, client: TestClient):
        """T053: User A creates task → User B tries GET /api/userA/tasks → 403 Forbidden."""
        # Create User A
        signup_a = client.post(
            "/api/auth/signup",
            json={"email": "usera@example.com", "password": "SecurePass123"},
        )
        user_a_id = signup_a.json()["user_id"]

        # Create User B
        signup_b = client.post(
            "/api/auth/signup",
            json={"email": "userb@example.com", "password": "SecurePass123"},
        )
        token_b = signup_b.json()["token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # User B tries to access User A's tasks (should be forbidden even if A has tasks)
        response = client.get(f"/api/{user_a_id}/tasks", headers=headers_b)

        assert response.status_code == 403
        assert "forbidden" in response.json()["detail"].lower() or "mismatch" in response.json()["detail"].lower()

    def test_jwt_user_id_must_match_url_user_id(self, client: TestClient):
        """T054: JWT has user_id 'A' → GET /api/userB/tasks → 403 Forbidden."""
        # Create User A
        signup_a = client.post(
            "/api/auth/signup",
            json={"email": "mismatchA@example.com", "password": "SecurePass123"},
        )
        user_a_id = signup_a.json()["user_id"]
        token_a = signup_a.json()["token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # Create User B
        signup_b = client.post(
            "/api/auth/signup",
            json={"email": "mismatchB@example.com", "password": "SecurePass123"},
        )
        user_b_id = signup_b.json()["user_id"]

        # User A (with their JWT) tries to access User B's tasks via URL
        response = client.get(f"/api/{user_b_id}/tasks", headers=headers_a)

        assert response.status_code == 403
        assert "forbidden" in response.json()["detail"].lower() or "mismatch" in response.json()["detail"].lower()

    def test_user_cannot_create_task_for_other_user(self, client: TestClient):
        """T069: JWT user_id 'A' → POST /api/userB/tasks → 403 Forbidden."""
        # Create User A
        signup_a = client.post(
            "/api/auth/signup",
            json={"email": "createA@example.com", "password": "SecurePass123"},
        )
        token_a = signup_a.json()["token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # Create User B
        signup_b = client.post(
            "/api/auth/signup",
            json={"email": "createB@example.com", "password": "SecurePass123"},
        )
        user_b_id = signup_b.json()["user_id"]

        # User A tries to create a task for User B
        response = client.post(
            f"/api/{user_b_id}/tasks",
            json={"title": "Malicious Task"},
            headers=headers_a,
        )

        assert response.status_code == 403
        assert "forbidden" in response.json()["detail"].lower() or "mismatch" in response.json()["detail"].lower()

    def test_user_cannot_update_other_user_task(self, client: TestClient):
        """T079: User A tries PUT /api/userB/tasks/{id} → 403 Forbidden."""
        from sqlmodel import Session
        from src.models import Task, User
        from src.database import engine
        import bcrypt

        # Create users and task directly in database
        with Session(engine) as session:
            # User A
            password_hash_a = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
            user_a = User(id="update-user-a", email="updatea@example.com", password_hash=password_hash_a)
            session.add(user_a)

            # User B
            password_hash_b = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
            user_b = User(id="update-user-b", email="updateb@example.com", password_hash=password_hash_b)
            session.add(user_b)
            session.commit()

            # Task owned by User B
            task_b = Task(user_id=user_b.id, title="User B's Task")
            session.add(task_b)
            session.commit()
            task_b_id = task_b.id

        # Login as User A
        login_a = client.post(
            "/api/auth/login",
            json={"email": "updatea@example.com", "password": "SecurePass123"},
        )
        token_a = login_a.json()["token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # User A tries to update User B's task
        response = client.put(
            f"/api/update-user-b/tasks/{task_b_id}",
            json={"title": "Malicious Update"},
            headers=headers_a,
        )

        assert response.status_code == 403
        assert "forbidden" in response.json()["detail"].lower() or "mismatch" in response.json()["detail"].lower()

    def test_user_cannot_delete_other_user_task(self, client: TestClient):
        """T090: User A tries DELETE /api/userB/tasks/{id} → 403 Forbidden."""
        from sqlmodel import Session
        from src.models import Task, User
        from src.database import engine
        import bcrypt

        # Create users and task directly in database
        with Session(engine) as session:
            # User A
            password_hash_a = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
            user_a = User(id="delete-user-a", email="deletea@example.com", password_hash=password_hash_a)
            session.add(user_a)

            # User B
            password_hash_b = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
            user_b = User(id="delete-user-b", email="deleteb@example.com", password_hash=password_hash_b)
            session.add(user_b)
            session.commit()

            # Task owned by User B
            task_b = Task(user_id=user_b.id, title="User B's Task to Delete")
            session.add(task_b)
            session.commit()
            task_b_id = task_b.id

        # Login as User A
        login_a = client.post(
            "/api/auth/login",
            json={"email": "deletea@example.com", "password": "SecurePass123"},
        )
        token_a = login_a.json()["token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # User A tries to delete User B's task
        response = client.delete(
            f"/api/delete-user-b/tasks/{task_b_id}",
            headers=headers_a,
        )

        assert response.status_code == 403
        assert "forbidden" in response.json()["detail"].lower() or "mismatch" in response.json()["detail"].lower()

    def test_filter_still_enforces_user_isolation(self, client: TestClient):
        """T098: GET /api/{user_id}/tasks?completed=false → still only returns user's tasks."""
        from sqlmodel import Session
        from src.models import Task, User
        from src.database import engine
        import bcrypt

        # Create two users with tasks
        with Session(engine) as session:
            # User A with incomplete task
            password_hash_a = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
            user_a = User(id="filter-iso-a", email="filterisoa@example.com", password_hash=password_hash_a)
            session.add(user_a)

            # User B with incomplete task
            password_hash_b = bcrypt.hashpw(b"SecurePass123", bcrypt.gensalt()).decode('utf-8')
            user_b = User(id="filter-iso-b", email="filterisob@example.com", password_hash=password_hash_b)
            session.add(user_b)
            session.commit()

            # Tasks for both users (both incomplete)
            task_a = Task(user_id=user_a.id, title="User A Incomplete Task", completed=False)
            task_b = Task(user_id=user_b.id, title="User B Incomplete Task", completed=False)
            session.add_all([task_a, task_b])
            session.commit()

        # Login as User A
        login_a = client.post(
            "/api/auth/login",
            json={"email": "filterisoa@example.com", "password": "SecurePass123"},
        )
        token_a = login_a.json()["token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # Get incomplete tasks for User A with filter
        response = client.get("api/filter-iso-a/tasks?completed=false", headers=headers_a)

        assert response.status_code == 200
        data = response.json()
        # Should only get User A's tasks, not User B's
        assert len(data) == 1
        assert data[0]["title"] == "User A Incomplete Task"
