#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime, timedelta

# Constants
TODO_FILE = "todo.json"

def load_tasks():
    """Load tasks from file"""
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {TODO_FILE} is corrupted. Creating a new task list.")
            return []
    return []

def save_tasks(tasks):
    """Save tasks to file"""
    with open(TODO_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(title, priority="medium", due=None):
    """Add a new task"""
    tasks = load_tasks()
    
    # Find the next ID
    task_id = 1
    if tasks:
        task_id = max(task["id"] for task in tasks) + 1
    
    # Create new task
    task = {
        "id": task_id,
        "title": title,
        "priority": priority,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "completed": False,
        "due": due
    }
    
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task {task_id} added: {title}")

def list_tasks(show_completed=False, priority=None, due_soon=False):
    """List tasks"""
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks found")
        return
    
    # Filter tasks
    filtered_tasks = []
    for task in tasks:
        if not show_completed and task["completed"]:
            continue
        
        if priority and task["priority"] != priority:
            continue
        
        if due_soon and task["due"]:
            due_date = datetime.strptime(task["due"], "%Y-%m-%d")
            today = datetime.now()
            if (due_date - today).days > 7:  # Due in more than a week
                continue
        
        filtered_tasks.append(task)
    
    if not filtered_tasks:
        print("No matching tasks found")
        return
    
    # Sort tasks: first by completion status, then by due date, then by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    filtered_tasks.sort(key=lambda x: (
        x["completed"],
        x["due"] if x["due"] else "9999-99-99",
        priority_order.get(x["priority"], 99)
    ))
    
    # Print tasks
    print("\nID | Title                        | Priority | Due Date   | Status")
    print("-" * 65)
    
    for task in filtered_tasks:
        status = "✓ Done" if task["completed"] else "○ Pending"
        due_str = task["due"] if task["due"] else ""
        priority_display = task["priority"].capitalize()
        
        # Colorize priority (using ANSI escape codes)
        if task["priority"] == "high":
            priority_display = f"\033[91m{priority_display}\033[0m"  # Red
        elif task["priority"] == "medium":
            priority_display = f"\033[93m{priority_display}\033[0m"  # Yellow
        
        print(f"{task['id']:<3}| {task['title']:<28} | {priority_display:<8} | {due_str:<10} | {status}")
    
    print(f"\nTotal: {len(filtered_tasks)} tasks")

def complete_task(task_id):
    """Mark a task as completed"""
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Task {task_id} marked as completed")
            return
    
    print(f"Task {task_id} not found")

def delete_task(task_id):
    """Delete a task"""
    tasks = load_tasks()
    
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            save_tasks(tasks)
            print(f"Task {task_id} deleted")
            return
    
    print(f"Task {task_id} not found")

def main():
    parser = argparse.ArgumentParser(description="Simple To-Do List CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add task command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-p", "--priority", choices=["high", "medium", "low"],
                           default="medium", help="Task priority")
    add_parser.add_argument("-d", "--due", help="Due date (YYYY-MM-DD)")
    
    # List tasks command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("-a", "--all", action="store_true", help="Show all tasks including completed")
    list_parser.add_argument("-p", "--priority", choices=["high", "medium", "low"],
                            help="Filter by priority")
    list_parser.add_argument("-s", "--soon", action="store_true", help="Show tasks due within a week")
    
    # Complete task command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("id", type=int, help="Task ID")
    
    # Delete task command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_task(args.title, args.priority, args.due)
    
    elif args.command == "list":
        list_tasks(args.all, args.priority, args.soon)
    
    elif args.command == "complete":
        complete_task(args.id)
    
    elif args.command == "delete":
        delete_task(args.id)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
