import csv
from datetime import datetime

# csv header
fieldnames = ['todo_name', 'create_time']

# List to store rows
rows = []


user_prompt = "Type Add(1) or Show(2) or Edit(3) or Complete(4) or Exit(5):"

todos = []

while True:
    user_action = input(user_prompt)
    user_action = user_action.strip()
    match user_action:
        case 'Add' | '1':
            todo = input('Enter a todo:') + "\n"
            todos.append(todo.capitalize())
            file = open('todos.txt', 'w')
            file.writelines(todos)
            file.close()
           # with open('todos.txt', 'w', encoding='UTF8', newline='') as f:
            #    writer = csv.writer(f)
                # write the header
             #  writer.writerow(fieldnames)

              #  write multiple rows
            #create_time = datetime.now().isoformat()

    #           writer.writerows(todos +','+create_time)
        case 'Show' | '2':
            file = open('todos.txt', 'r')
            todos = file.readlines()
            file.close()
            for index, item in enumerate(todos):
                print(f"{index + 1}-{item}")
        case 'Edit' | '3':
            number = int(input("Number of the todo to edit:"))
            file = open('todos.txt', 'r')
            todos = file.readlines()
            file.close()
            exist_todo = todos[number-1]
            print(exist_todo)
            new_todo = input('Enter a new todo:') + "\n"
            todos[number-1] = new_todo
            file = open('todos.txt', 'w')
            file.writelines(todos)
            file.close()
        case 'Complete' | '4':
            number = int(input("Enter the todo to complete:"))
            file = open('todos.txt', 'r')
            todos = file.readlines()
            file.close()
            if len(todos) > 1:
                todos.pop(number-1)

                file = open('todos.txt', 'w')
                file.writelines(todos)
                file.close()
            else:
                print("Length of List is Zero. Try Again!!!")
        case 'Exit' | '5':
            break
        case _:
            print("Enter one of the options - 1 , 2, 3")