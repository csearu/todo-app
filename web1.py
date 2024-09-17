import streamlit as st
import pandas as pd
import functions

st.title("ZenDo")
st.subheader("Todo App in Zen Mode")
st.write("This app is to increase your productivity")

# Load the existing CSV file
df = pd.read_csv("todo.csv")

# Function to save the DataFrame back to CSV
def save_df():
    df.to_csv("todo.csv", index=False)

# Display the current tasks
st.table(df)

# Add a new task
todo_name = st.text_input("Enter New ToDo")
priority = st.selectbox("Select priority", ["1", "2", "3", "4", "5"])
add_button = st.button("Add New ToDo")

# When the "Add Task" button is clicked
if add_button and todo_name:
    # Add the new task to the dataframe
    new_task_df = pd.DataFrame([[todo_name, functions.get_current_time(), priority, "Incomplete"]],
                               columns=["todo_name", "create_time", "priority", "status"])
    df = pd.concat([df, new_task_df], ignore_index=True)

    # Save the updated dataframe to CSV
    save_df()

    # Display a confirmation message
    st.success(f"New task '{todo_name}' added with priority '{priority}'!")

# Option to complete a task
st.write("### Mark Task as Completed")
task_to_complete = st.selectbox("Select a task to complete", df[df['status'] == "Incomplete"]['todo_name'])
complete_button = st.button("Complete Task")

if complete_button and task_to_complete:
    # Mark the selected task as completed
    df.loc[df['todo_name'] == task_to_complete, 'status'] = "Complete"
    save_df()
    st.success(f"Task '{task_to_complete}' marked as completed!")

# Option to edit a task
st.write("### Edit an Existing Task")
task_to_edit = st.selectbox("Select a task to edit", df['todo_name'])
new_todo_name = st.text_input("Enter new name for the task", value=task_to_edit)
new_priority = st.selectbox("Select new priority", ["1", "2", "3", "4", "5"], index=int(df[df['todo_name'] == task_to_edit]['priority'].values[0])-1)
edit_button = st.button("Edit Task")

if edit_button and new_todo_name:
    # Update the task with the new name and priority
    df.loc[df['todo_name'] == task_to_edit, 'todo_name'] = new_todo_name
    df.loc[df['todo_name'] == new_todo_name, 'priority'] = new_priority
    save_df()
    st.success(f"Task '{task_to_edit}' updated!")

# Option to delete a task
st.write("### Delete a Task")
task_to_delete = st.selectbox("Select a task to delete", df['todo_name'])
delete_button = st.button("Delete Task")

if delete_button and task_to_delete:
    # Delete the selected task
    df = df[df['todo_name'] != task_to_delete]
    save_df()
    st.success(f"Task '{task_to_delete}' deleted!")

# Show the updated tasks table
st.write("### Updated ToDo List")
st.table(df)
