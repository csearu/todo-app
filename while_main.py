user_prompt = "Type Add(1) or Show(2) or Edit(3) or Exit(4):"

todos = []

while True:
    user_action = input(user_prompt)
    user_action = user_action.strip()
    match user_action:
        case 'Add' | '1':
            todo = input('Enter a todo:')
            todos.append(todo.capitalize())
        case 'Show' | '2':
            for item in todos:
                print(item)
        case 'Edit' | '3':
            number = int(input("Number of the todo to edit:"))
            exist_todo = todos[number-1]
            print(exist_todo)
            new_todo = input('Enter a new todo:')
            todos[number-1] = new_todo
        case 'Exit' | '4':
            break
        case _:
            print("Enter one of the options - 1 , 2, 3")