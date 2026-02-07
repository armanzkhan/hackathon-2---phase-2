"""
Unit tests for TodoRepository.

Tests CRUD operations, ID generation, and repository behavior.
"""

import unittest
from src.repository.todo_repository import TodoRepository
from src.models.todo import Todo


class TestTodoRepository(unittest.TestCase):
    """Test suite for TodoRepository."""

    def setUp(self):
        """Create a fresh repository for each test."""
        self.repo = TodoRepository()

    def test_create_todo(self):
        """T015 [US1]: Repository create() should add todo and return it."""
        todo = self.repo.create("Buy groceries", "Milk, eggs")

        self.assertEqual(todo.id, 1)
        self.assertEqual(todo.title, "Buy groceries")
        self.assertEqual(todo.description, "Milk, eggs")
        self.assertFalse(todo.completed)

    def test_get_all_with_empty_storage(self):
        """T016 [US1]: get_all() on empty repository should return empty list."""
        todos = self.repo.get_all()
        self.assertEqual(todos, [])
        self.assertIsInstance(todos, list)

    def test_get_all_with_multiple_todos(self):
        """T017 [US1]: get_all() should return all todos sorted by ID."""
        todo1 = self.repo.create("Task 1")
        todo2 = self.repo.create("Task 2")
        todo3 = self.repo.create("Task 3")

        todos = self.repo.get_all()

        self.assertEqual(len(todos), 3)
        self.assertEqual(todos[0].id, 1)
        self.assertEqual(todos[1].id, 2)
        self.assertEqual(todos[2].id, 3)
        self.assertEqual([t.title for t in todos], ["Task 1", "Task 2", "Task 3"])

    def test_id_auto_increment(self):
        """T018 [US1]: IDs should auto-increment (1, 2, 3...)."""
        todo1 = self.repo.create("Task 1")
        todo2 = self.repo.create("Task 2")
        todo3 = self.repo.create("Task 3")

        self.assertEqual(todo1.id, 1)
        self.assertEqual(todo2.id, 2)
        self.assertEqual(todo3.id, 3)

    def test_get_by_id_existing(self):
        """Additional test: get_by_id() should return todo if exists."""
        created = self.repo.create("Test Task")
        found = self.repo.get_by_id(1)

        self.assertIsNotNone(found)
        self.assertEqual(found.id, created.id)
        self.assertEqual(found.title, created.title)

    def test_get_by_id_non_existent(self):
        """Additional test: get_by_id() should return None if not found."""
        found = self.repo.get_by_id(999)
        self.assertIsNone(found)

    def test_create_with_empty_title_should_fail(self):
        """Additional test: create() with empty title should raise ValueError."""
        with self.assertRaises(ValueError):
            self.repo.create("")

    def test_update_title(self):
        """Additional test: update() should modify title."""
        todo = self.repo.create("Old Title")
        updated = self.repo.update(1, title="New Title")

        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.id, 1)

        # Verify in storage
        stored = self.repo.get_by_id(1)
        self.assertEqual(stored.title, "New Title")

    def test_update_description(self):
        """Additional test: update() should modify description."""
        todo = self.repo.create("Title", "Old Desc")
        updated = self.repo.update(1, description="New Desc")

        self.assertEqual(updated.description, "New Desc")

    def test_update_both_fields(self):
        """Additional test: update() should modify both title and description."""
        todo = self.repo.create("Old Title", "Old Desc")
        updated = self.repo.update(1, title="New Title", description="New Desc")

        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.description, "New Desc")

    def test_update_non_existent_should_fail(self):
        """Additional test: update() with invalid ID should raise KeyError."""
        with self.assertRaises(KeyError):
            self.repo.update(999, title="New Title")

    def test_update_preserves_completion_status(self):
        """Additional test: update() should preserve completion status."""
        todo = self.repo.create("Title")
        self.repo.mark_complete(1)

        updated = self.repo.update(1, title="New Title")
        self.assertTrue(updated.completed)

    def test_delete_existing(self):
        """Additional test: delete() should remove todo and return True."""
        self.repo.create("Task")
        result = self.repo.delete(1)

        self.assertTrue(result)
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_non_existent(self):
        """Additional test: delete() with invalid ID should return False."""
        result = self.repo.delete(999)
        self.assertFalse(result)

    def test_delete_is_idempotent(self):
        """Additional test: deleting same ID twice should be safe."""
        self.repo.create("Task")
        self.repo.delete(1)
        result = self.repo.delete(1)  # Delete again

        self.assertFalse(result)

    def test_id_not_reused_after_deletion(self):
        """Additional test: IDs should not be reused after deletion."""
        self.repo.create("Task 1")  # ID 1
        self.repo.create("Task 2")  # ID 2
        self.repo.delete(1)  # Delete ID 1

        new_todo = self.repo.create("Task 3")  # Should be ID 3, not 1
        self.assertEqual(new_todo.id, 3)

    def test_mark_complete(self):
        """Additional test: mark_complete() should set completed=True."""
        todo = self.repo.create("Task")
        self.assertFalse(todo.completed)

        completed = self.repo.mark_complete(1)
        self.assertTrue(completed.completed)

        # Verify in storage
        stored = self.repo.get_by_id(1)
        self.assertTrue(stored.completed)

    def test_mark_complete_non_existent_should_fail(self):
        """Additional test: mark_complete() with invalid ID should raise KeyError."""
        with self.assertRaises(KeyError):
            self.repo.mark_complete(999)

    def test_mark_complete_is_idempotent(self):
        """Additional test: marking complete multiple times should be safe."""
        self.repo.create("Task")
        self.repo.mark_complete(1)
        completed = self.repo.mark_complete(1)  # Mark again

        self.assertTrue(completed.completed)

    def test_exists(self):
        """Additional test: exists() should return True/False correctly."""
        self.assertFalse(self.repo.exists(1))

        self.repo.create("Task")
        self.assertTrue(self.repo.exists(1))

        self.repo.delete(1)
        self.assertFalse(self.repo.exists(1))


if __name__ == '__main__':
    unittest.main()
