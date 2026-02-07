"""
Unit tests for CLI command handlers.

Tests command handler functions with mocked input/output.
"""

import unittest
from unittest.mock import patch
from io import StringIO
from src.repository.todo_repository import TodoRepository
from src.cli.commands import handle_create, handle_list


class TestCommands(unittest.TestCase):
    """Test suite for CLI command handlers."""

    def setUp(self):
        """Create a fresh repository for each test."""
        self.repo = TodoRepository()

    @patch('builtins.input', side_effect=["Buy groceries", "Milk, eggs"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_create_success(self, mock_stdout, mock_input):
        """Test handle_create() with valid input."""
        handle_create(self.repo)
        output = mock_stdout.getvalue()

        self.assertIn("[OK]", output)
        self.assertIn("created", output.lower())
        self.assertIn("1", output)  # ID

    @patch('builtins.input', side_effect=["", ""])
    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_create_empty_title(self, mock_stdout, mock_input):
        """Test handle_create() with empty title."""
        handle_create(self.repo)
        output = mock_stdout.getvalue()

        self.assertIn("[X]", output)
        self.assertIn("empty", output.lower())

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_list_empty(self, mock_stdout):
        """Test handle_list() with no todos."""
        handle_list(self.repo)
        output = mock_stdout.getvalue()

        self.assertIn("No todos", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_list_with_todos(self, mock_stdout):
        """Test handle_list() with multiple todos."""
        self.repo.create("Task 1")
        self.repo.create("Task 2")

        handle_list(self.repo)
        output = mock_stdout.getvalue()

        self.assertIn("Task 1", output)
        self.assertIn("Task 2", output)
        self.assertIn("[ ]", output)  # Incomplete status


if __name__ == '__main__':
    unittest.main()
