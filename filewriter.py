import csv
from datetime import datetime

# CSV header
fieldnames = ['todo_name', 'create_time', 'update_time', 'priority', 'status']

# List to store rows
rows = []

user_prompt = "Type Add(1), Show(2), Edit(3), Complete(4), Rearrange(5), or Exit(6):"

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
    print(f"{'No.':<4} {'Todo Name':<20} {'Create Time':<40} {'Update Time':<40} {'Priority':<8} {'Status':<10}")
    print("-" * 150)

    # Print each row of data
    for index, todo in enumerate(todos, start=1):
        print(f"{index:<4} {todo['todo_name']:<20} {todo['create_time']:<40} {todo['update_time']:<40} {todo['priority']:<8} {todo['status']:<10}")


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
        case 'Exit' | '7':
            break
        case _:
            print("Enter one of the options - 1, 2, 3, 4, 5, 6, or 7")

print("Program exited.")
