# ✅ To-Do List CLI

A simple command-line to-do list application to manage your tasks efficiently.

## ✨ Features

- ➕ Add tasks with title, priority, and due date
- 📋 List tasks with various filtering options
- ✓ Mark tasks as completed
- 🗑️ Delete tasks you no longer need
- 🔄 Automatic sorting by completion status, due date, and priority
- 💾 Persistent storage using JSON


## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/todo-cli.git
cd todo-cli
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py <command> [options]
```

## ⚙️ Commands

- `add`: Add a new task
- `list`: List tasks
- `complete`: Mark a task as completed
- `delete`: Delete a task

## 📋 Command Options

### Add a task:
```bash
python main.py add "Task title" [options]
```

#### Options:

- `-p, --priority`: Task priority (high, medium, low)
- `-d, --due`: Due date (YYYY-MM-DD)

### List tasks:
```bash
python main.py list [options]
```

#### Options:

- `-a, --all`: Show all tasks including completed
- `-p, --priority`: Filter by priority (high, medium, low)
- `-s, --soon`: Show tasks due within a week

### Complete a task:
```bash
python main.py complete <task_id>
```

### Delete a task:
```bash
python main.py delete <task_id>
```

## 📝 Examples

### Add a task:
```bash
# Add a regular task
python main.py add "Buy groceries"
```

```bash
# Add a high priority task
python main.py add "Finish project report" -p high
```

```bash
# Add a task with a due date
python main.py add "Pay electricity bill" -d 2023-09-30
```


