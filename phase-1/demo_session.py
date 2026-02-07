"""
Interactive demo session for Todo application.
Simulates a real user session.
"""

import sys
from unittest.mock import patch
from src.repository.todo_repository import TodoRepository
from src.cli.menu import TodoMenu

def demo_session():
    """Run an interactive demo session."""

    # Simulate user choices and inputs
    user_inputs = [
        # Create first todo
        "1",  # Choice: Create
        "Buy groceries",  # Title
        "Milk, eggs, bread, cheese",  # Description

        # Create second todo
        "1",  # Choice: Create
        "Call dentist",  # Title
        "Schedule annual checkup",  # Description

        # Create third todo
        "1",  # Choice: Create
        "Finish project report",  # Title
        "Q4 summary and analysis",  # Description

        # View all todos
        "2",  # Choice: View all

        # Mark one as complete
        "5",  # Choice: Mark complete
        "2",  # ID: 2 (Call dentist)

        # View again to see the change
        "2",  # Choice: View all

        # Update a todo
        "3",  # Choice: Update
        "1",  # ID: 1 (Buy groceries)
        "Buy groceries and snacks",  # New title
        "Milk, eggs, bread, cheese, chips",  # New description

        # View again
        "2",  # Choice: View all

        # Delete a todo
        "4",  # Choice: Delete
        "3",  # ID: 3 (Finish project report)

        # View final state
        "2",  # Choice: View all

        # Exit
        "6"   # Choice: Exit
    ]

    print("=" * 70)
    print("LIVE DEMO: Todo In-Memory Console Application")
    print("=" * 70)
    print("\nStarting application...\n")

    # Create repository and menu
    repo = TodoRepository()
    menu = TodoMenu(repo)

    # Mock input with our simulated user choices
    with patch('builtins.input', side_effect=user_inputs):
        # Display welcome
        print("Welcome to Todo Manager!")
        print("All data is stored in memory and will be lost on exit.\n")

        # Run the menu
        menu.run()

        # Display goodbye
        print("\nGoodbye!")

    print("\n" + "=" * 70)
    print("Demo session complete!")
    print("=" * 70)
    print("\nWhat happened in this session:")
    print("1. Created 3 todos (Buy groceries, Call dentist, Finish report)")
    print("2. Viewed the complete list")
    print("3. Marked 'Call dentist' as complete [X]")
    print("4. Updated 'Buy groceries' title and description")
    print("5. Deleted 'Finish project report'")
    print("6. Final state: 2 todos remaining (1 incomplete, 1 complete)")
    print("\n[OK] Application demonstrated successfully!")

if __name__ == "__main__":
    demo_session()
