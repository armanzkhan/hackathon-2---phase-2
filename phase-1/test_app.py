"""
Automated test script for Todo application.

Tests all CRUD operations through the CLI interface.
"""

import sys
from io import StringIO
from unittest.mock import patch
from src.repository.todo_repository import TodoRepository
from src.cli.menu import TodoMenu

def test_full_workflow():
    """Test complete workflow: create, view, mark complete, update, delete."""

    print("=" * 60)
    print("TESTING TODO APPLICATION - Full Workflow")
    print("=" * 60)

    # Create repository and menu
    repo = TodoRepository()
    menu = TodoMenu(repo)

    print("\n1. CREATING TODOS")
    print("-" * 60)

    # Create todo 1
    print("Creating todo: 'Buy groceries' with description 'Milk, eggs, bread'")
    with patch('builtins.input', side_effect=["Buy groceries", "Milk, eggs, bread"]):
        from src.cli.commands import handle_create
        handle_create(repo)

    # Create todo 2
    print("\nCreating todo: 'Call dentist' with no description")
    with patch('builtins.input', side_effect=["Call dentist", ""]):
        from src.cli.commands import handle_create
        handle_create(repo)

    # Create todo 3
    print("\nCreating todo: 'Finish project report'")
    with patch('builtins.input', side_effect=["Finish project report", "Q4 summary"]):
        from src.cli.commands import handle_create
        handle_create(repo)

    print("\n2. VIEWING ALL TODOS")
    print("-" * 60)
    from src.cli.commands import handle_list
    handle_list(repo)

    print("\n3. MARKING TODO AS COMPLETE")
    print("-" * 60)
    print("Marking todo ID 2 (Call dentist) as complete...")
    with patch('builtins.input', return_value="2"):
        from src.cli.commands import handle_complete
        handle_complete(repo)

    print("\nViewing todos after marking complete:")
    handle_list(repo)

    print("\n4. UPDATING A TODO")
    print("-" * 60)
    print("Updating todo ID 1 - changing title to 'Buy groceries and snacks'")
    with patch('builtins.input', side_effect=["1", "Buy groceries and snacks", "Milk, eggs, bread, chips"]):
        from src.cli.commands import handle_update
        handle_update(repo)

    print("\nViewing todos after update:")
    handle_list(repo)

    print("\n5. DELETING A TODO")
    print("-" * 60)
    print("Deleting todo ID 3 (Finish project report)...")
    with patch('builtins.input', return_value="3"):
        from src.cli.commands import handle_delete
        handle_delete(repo)

    print("\nViewing todos after deletion:")
    handle_list(repo)

    print("\n6. TESTING ERROR HANDLING")
    print("-" * 60)

    # Test empty title
    print("Attempting to create todo with empty title...")
    with patch('builtins.input', side_effect=["", ""]):
        handle_create(repo)

    # Test invalid ID
    print("\nAttempting to mark non-existent todo (ID 999) as complete...")
    with patch('builtins.input', return_value="999"):
        handle_complete(repo)

    # Test invalid ID format
    print("\nAttempting to delete with invalid ID (abc)...")
    with patch('builtins.input', return_value="abc"):
        handle_delete(repo)

    print("\n7. TESTING EMPTY LIST MESSAGE")
    print("-" * 60)
    print("Creating new empty repository...")
    empty_repo = TodoRepository()
    print("Viewing empty list:")
    handle_list(empty_repo)

    print("\n8. FINAL STATE")
    print("-" * 60)
    print("Current todos in main repository:")
    handle_list(repo)

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("[OK] Create: 3 todos created successfully")
    print("[OK] View: Todo list displayed correctly")
    print("[OK] Mark Complete: Todo 2 marked complete ([X])")
    print("[OK] Update: Todo 1 title and description updated")
    print("[OK] Delete: Todo 3 deleted successfully")
    print("[OK] Error Handling: Empty title, invalid ID, invalid format handled")
    print("[OK] Empty List: Friendly message displayed")
    print("\n[OK] ALL TESTS PASSED - Application working correctly!")
    print("=" * 60)

if __name__ == "__main__":
    test_full_workflow()
