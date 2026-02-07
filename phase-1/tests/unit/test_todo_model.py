"""
Unit tests for Todo domain entity.

Tests the Todo dataclass including creation, validation, immutability,
and business methods.
"""

import unittest
from src.models.todo import Todo


class TestTodoModel(unittest.TestCase):
    """Test suite for Todo entity."""

    def test_create_todo_with_valid_title(self):
        """T011 [US1]: Todo creation with valid title should succeed."""
        todo = Todo(id=1, title="Buy groceries")
        self.assertEqual(todo.id, 1)
        self.assertEqual(todo.title, "Buy groceries")
        self.assertEqual(todo.description, "")
        self.assertFalse(todo.completed)

    def test_create_todo_with_empty_title_should_fail(self):
        """T012 [US1]: Todo creation with empty title should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            Todo(id=1, title="")
        self.assertIn("empty", str(context.exception).lower())

    def test_create_todo_with_whitespace_only_title_should_fail(self):
        """T013 [US1]: Todo creation with whitespace-only title should raise ValueError."""
        with self.assertRaises(ValueError) as context:
            Todo(id=1, title="   ")
        self.assertIn("empty", str(context.exception).lower())

        # Test with tabs and newlines too
        with self.assertRaises(ValueError):
            Todo(id=1, title="\t\n")

    def test_todo_default_values(self):
        """T014 [US1]: Todo should have correct default values."""
        todo = Todo(id=1, title="Test Task")
        self.assertEqual(todo.description, "")
        self.assertFalse(todo.completed)

    def test_todo_with_all_fields(self):
        """Additional test: Todo creation with all fields specified."""
        todo = Todo(
            id=1,
            title="Buy groceries",
            description="Milk, eggs, bread",
            completed=True
        )
        self.assertEqual(todo.id, 1)
        self.assertEqual(todo.title, "Buy groceries")
        self.assertEqual(todo.description, "Milk, eggs, bread")
        self.assertTrue(todo.completed)

    def test_todo_immutability(self):
        """Additional test: Todo should be immutable (frozen)."""
        todo = Todo(id=1, title="Test")
        with self.assertRaises(Exception):  # FrozenInstanceError
            todo.title = "Modified"  # type: ignore

    def test_todo_mark_complete(self):
        """Additional test: mark_complete() should return new instance with completed=True."""
        todo = Todo(id=1, title="Task", completed=False)
        completed_todo = todo.mark_complete()

        # Original unchanged
        self.assertFalse(todo.completed)

        # New instance is complete
        self.assertTrue(completed_todo.completed)
        self.assertEqual(completed_todo.id, todo.id)
        self.assertEqual(completed_todo.title, todo.title)

    def test_todo_update_title(self):
        """Additional test: update() should return new instance with updated title."""
        todo = Todo(id=1, title="Old Title", description="Desc")
        updated = todo.update(title="New Title")

        # Original unchanged
        self.assertEqual(todo.title, "Old Title")

        # New instance has updated title
        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.description, "Desc")
        self.assertEqual(updated.id, 1)

    def test_todo_update_description(self):
        """Additional test: update() should update description."""
        todo = Todo(id=1, title="Title", description="Old")
        updated = todo.update(description="New")

        self.assertEqual(updated.description, "New")
        self.assertEqual(updated.title, "Title")

    def test_todo_update_preserves_completion_status(self):
        """Additional test: update() should preserve completion status."""
        todo = Todo(id=1, title="Title", completed=True)
        updated = todo.update(title="New Title")

        self.assertTrue(updated.completed)


if __name__ == '__main__':
    unittest.main()
