import csv
import json
from datetime import datetime

# CSV header
fieldnames = ['todo_name', 'create_time', 'update_time', 'priority', 'status']

# List to store rows
rows = []
undo_stack = []
redo_stack = []

user_prompt = """Type one of the options
Add(1),Show(2),Edit(3),Complete(4),Rearrange(5),Display(6),Search(7),Archive(8),Export_JSON(9),
Import_JSON(10),
Exit(99)
                    Enter your option:
"""

def get_current_time():
    """Returns the current ISO formatted time."""
    return datetime.now().isoformat()

def get_todo_index(todos):
    """Show todos and get the index of the todo from user input."""
    show_user_input(todos)
    index = int(input("Enter the number of the todo: ")) - 1
    if 0 <= index < len(todos):
        return index
    else:
        print("Invalid index!")
        return None

def write_to_csv(rows):
    """Writes the current rows to the CSV file."""
    with open('todo.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def load_existing_todos():
    """Loads existing todos from the CSV file."""
    try:
        with open('todo.csv', 'r', encoding='UTF8', newline='') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return []

def show_user_input(todos):
    """Displays the todos."""
    for index, item in enumerate(todos):
        print(f"{index + 1} - {item['todo_name']} (Priority: {item['priority']}, Created: {item['create_time']}, Updated: {item['update_time']}, Status: {item['status']})")

def add_todo():
    """Adds a new todo."""
    todo_name = input("Enter Todo: ")
    priority = int(input("Enter Priority (1-5): "))
    row = {
        'todo_name': todo_name,
        'create_time': get_current_time(),
        'update_time': '',
        'priority': priority,
        'status': 'pending'
    }
    rows.append(row)
    write_to_csv(rows)

def edit_todo():
    """Edits an existing todo."""
    index = get_todo_index(rows)
    if index is not None:
        rows[index]['todo_name'] = input("Enter new Todo name: ")
        rows[index]['priority'] = int(input("Enter new Priority (1-5): "))
        rows[index]['update_time'] = get_current_time()
        write_to_csv(rows)

def complete_todo():
    """Marks a todo as complete."""
    index = get_todo_index(rows)
    if index is not None:
        rows[index]['status'] = 'complete'
        rows[index]['update_time'] = get_current_time()
        rows[index]['priority'] = 99
        write_to_csv(rows)

def rearrange_todos():
    """Rearranges todos based on priority."""
    def get_priority_value(todo):
        try:
            return int(todo['priority']) if todo['priority'] else 0
        except ValueError:
            return 0

    rows.sort(key=get_priority_value)
    write_to_csv(rows)
    print("Todos rearranged by priority.")

# Define a function to print the table
def display_todos_table(todos):
    # Print the header
    print(f"{'No.':<4} {'Todo Name':<20} {'Create Time':<26} {'Update Time':<26} {'Priority':<8} {'Status':<10}")
    print("-" * 150)

    # Print each row of data
    for index, todo in enumerate(todos, start=1):
        print(f"{index:<4} {todo['todo_name']:<20} {todo['create_time']:<26} {todo['update_time']:<26} {todo['priority']:<8} {todo['status']:<10}")

    print("-" * 150)


def search_todos(todos, search_term):
    results = [todo for todo in todos if search_term.lower() in todo['todo_name'].lower()]
    show_user_input(results)

def search_interface():
    search_term = input("Enter search term: ")
    search_todos(rows, search_term)

def check_for_notifications(todos):
    high_priority_todos = [todo for todo in todos if int(todo['priority']) == 5]
    for todo in high_priority_todos:
        print(f"Reminder: High-priority task '{todo['todo_name']}' is due soon!")


def archive_completed_todos(todos):
    completed_todos = [todo for todo in todos if todo['status'] == 'complete']

    if completed_todos:  # Check if there are completed todos
        with open('archived_todos.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            for todo in completed_todos:
                writer.writerow(todo)
        print(f"Successfully archived {len(completed_todos)} todos.")
    else:
        print("No completed todos to archive.")

    # Update the current todo list by removing completed todos
    todos[:] = [todo for todo in todos if todo['status'] != 'complete']
    write_to_csv(todos)


def add_undo_state(todos):
    undo_stack.append(todos.copy())

def undo(todos):
    if undo_stack:
        redo_stack.append(todos.copy())
        return undo_stack.pop()
    print("No actions to undo.")
    return todos

def redo(todos):
    if redo_stack:
        undo_stack.append(todos.copy())
        return redo_stack.pop()
    print("No actions to redo.")
    return todos



def export_todos_to_json(todos):
    with open('todos.json', 'w') as f:
        json.dump(todos, f, indent=4)
    # Print the number of rows written to the JSON file
    print(f"Todos Export complete - {len(todos)} rows written to 'todos.json'")


def import_todos_from_json(todos, csv_filename='todo.csv'):
    try:
        # Read from the JSON file
        with open('todos.json', 'r') as f:
            imported_todos = json.load(f)

        # Append the imported todos to the in-memory list
        todos.extend(imported_todos)

        # Append to the existing CSV file
        with open(csv_filename, 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # Write rows for the newly imported todos
            for todo in imported_todos:
                writer.writerow(todo)

        print(f"Todos Import complete from 'todos.json'. Imported {len(imported_todos)} items.")
    except FileNotFoundError:
        print("File 'todos.json' not found. No todos were imported.")


def export_todos_to_excel(todos):
    import pandas as pd
    df = pd.DataFrame(todos)
    df.to_excel('todos.xlsx', index=False)

def import_todos_from_excel():
    import pandas as pd
    try:
        df = pd.read_excel('todos.xlsx')
        return df.to_dict('records')
    except FileNotFoundError:
        return []


# Load existing todos at the start of the program
rows = load_existing_todos()

# Main loop to interact with the user
while True:
    user_action = input(user_prompt).strip()
    match user_action:
        case 'Add' | '1':
            add_todo()
        case 'Show' | '2':
            show_user_input(rows)
        case 'Edit' | '3':
            edit_todo()
        case 'Complete' | '4':
            complete_todo()
        case 'Rearrange' | '5':
            rearrange_todos()
        case 'Display' | '6':
            display_todos_table(rows)
        case 'Search' | '7':
            search_interface()
        case 'Archive' | '8':
            archive_completed_todos(rows)
        case 'Export_JSON' | '9':
            export_todos_to_json(rows)
        case 'Import_JSON' | '10':
            import_todos_from_json(rows)
        case 'Exit' | '99':
            break
        case _:
            print("Enter one of the options - 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, or 99")

print("Program exited.")
