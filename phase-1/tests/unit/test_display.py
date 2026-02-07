"""
Unit tests for display formatting functions.

Tests output formatting for todos and messages.
"""

import unittest
from src.cli.display import (
    format_todo_list,
    format_single_todo,
    format_error,
    format_success
)
from src.models.todo import Todo


class TestDisplay(unittest.TestCase):
    """Test suite for display formatting functions."""

    def test_format_todo_list_with_empty_list(self):
        """T021 [US1]: format_todo_list() should show friendly message for empty list."""
        result = format_todo_list([])
        self.assertIn("No todos", result)
        self.assertIn("create", result.lower())

    def test_format_todo_list_with_multiple_todos(self):
        """T022 [US1]: format_todo_list() should format multiple todos correctly."""
        todos = [
            Todo(id=1, title="Buy groceries", description="", completed=False),
            Todo(id=2, title="Call dentist", description="", completed=True),
            Todo(id=3, title="Finish report", description="", completed=False)
        ]

        result = format_todo_list(todos)

        # Check header
        self.assertIn("Your Todos", result)
        self.assertIn("ID", result)
        self.assertIn("Status", result)
        self.assertIn("Title", result)

        # Check content
        self.assertIn("Buy groceries", result)
        self.assertIn("Call dentist", result)
        self.assertIn("Finish report", result)

        # Check status indicators
        self.assertIn("[ ]", result)  # Incomplete
        self.assertIn("[X]", result)  # Complete

    def test_format_todo_list_with_single_todo(self):
        """Additional test: format_todo_list() with single todo."""
        todos = [Todo(id=1, title="Test Task", completed=False)]
        result = format_todo_list(todos)

        self.assertIn("Test Task", result)
        self.assertIn("1", result)
        self.assertIn("[ ]", result)

    def test_format_todo_list_shows_correct_status_icons(self):
        """Additional test: format_todo_list() shows [X] for complete, [ ] for incomplete."""
        complete_todo = Todo(id=1, title="Complete", completed=True)
        incomplete_todo = Todo(id=2, title="Incomplete", completed=False)

        result_complete = format_todo_list([complete_todo])
        result_incomplete = format_todo_list([incomplete_todo])

        self.assertIn("[X]", result_complete)
        self.assertNotIn("[ ]", result_complete)

        self.assertIn("[ ]", result_incomplete)
        self.assertNotIn("[X]", result_incomplete)

    def test_format_single_todo(self):
        """Additional test: format_single_todo() shows all todo details."""
        todo = Todo(
            id=1,
            title="Buy groceries",
            description="Milk, eggs, bread",
            completed=False
        )

        result = format_single_todo(todo)

        self.assertIn("1", result)
        self.assertIn("Buy groceries", result)
        self.assertIn("Milk, eggs, bread", result)
        self.assertIn("[ ]", result)
        self.assertIn("Incomplete", result)

    def test_format_single_todo_complete(self):
        """Additional test: format_single_todo() shows complete status."""
        todo = Todo(id=1, title="Task", description="", completed=True)
        result = format_single_todo(todo)

        self.assertIn("[X]", result)
        self.assertIn("Complete", result)

    def test_format_single_todo_no_description(self):
        """Additional test: format_single_todo() handles empty description."""
        todo = Todo(id=1, title="Task", description="", completed=False)
        result = format_single_todo(todo)

        self.assertIn("no description", result.lower())

    def test_format_error(self):
        """Additional test: format_error() prefixes with error icon."""
        result = format_error("Something went wrong")
        self.assertIn("[X]", result)
        self.assertIn("Error", result)
        self.assertIn("Something went wrong", result)

    def test_format_success(self):
        """Additional test: format_success() prefixes with success icon."""
        result = format_success("Operation completed")
        self.assertIn("[OK]", result)
        self.assertIn("Operation completed", result)


if __name__ == '__main__':
    unittest.main()
