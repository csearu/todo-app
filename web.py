import streamlit as st
import functions
import pandas as pd

st.title("ZenDo")
st.subheader("Todo App in Zen Mode")
st.write("This app is to increase your productivity")

# Load the existing CSV file
df = pd.read_csv("todo.csv")

# Display the current tasks
st.table(df)

# Add a new task
todo_name = st.text_input("Enter New ToDo")
priority = st.selectbox("Select priority", ["1", "2", "3", "4", "5"])
add_button = st.button("Add New ToDo")

# When the "Add Task" button is clicked
if add_button and todo_name:
    # Add the new task to the dataframe
    new_task_df = pd.DataFrame([[todo_name, functions.get_current_time(), priority]], columns=["todo_name", "create_time", "priority"])
    df = pd.concat([df, new_task_df], ignore_index=True)

    # Save the updated dataframe to CSV
    df.to_csv("todo.csv", index=False)

    # Display a confirmation message
    st.success(f"New task '{todo_name}' added with priority '{priority}'!")

# Show the updated tasks table
st.table(df)