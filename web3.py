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


# Display tasks in a table format
st.write("### Manage Your Tasks")

# Header for the table
st.write("#### To-Do List")
columns = st.columns([3, 2, 2, 2, 1, 1])  # Define column widths

with columns[0]:
    st.write("Task Name")
with columns[1]:
    st.write("Priority")
with columns[2]:
    st.write("Status")
with columns[3]:
    st.write("Creation Time")
with columns[4]:
    st.write("Complete")
with columns[5]:
    st.write("Delete")

# Loop through the DataFrame and display each task in a row
for i, row in df.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 1, 1])

    # Task name (editable)
    with col1:
        new_todo_name = st.text_input(f"Task {i + 1}", value=row['todo_name'], key=f"task_{i}")

    # Priority (editable dropdown)
    priority_value = row['priority']
    if pd.isna(priority_value):
        priority_value = "1"
    with col2:
        new_priority = st.selectbox(f"Priority {i + 1}", ["1", "2", "3", "4", "5"], index=int(priority_value) - 1,
                                    key=f"priority_{i}")

    # Status (editable dropdown)
    with col3:
        status = st.selectbox(f"Status {i + 1}", ["Incomplete", "Complete"],
                              index=0 if row['status'] == "Incomplete" else 1, key=f"status_{i}")

    # Creation time (display only)
    with col4:
        st.write(row['create_time'])

    # Complete button
    with col5:
        if status == "Incomplete" and st.button("Complete", key=f"complete_{i}"):
            df.loc[i, 'status'] = "Complete"
            save_df()
            st.success(f"Task {i + 1} marked as complete!")

    # Delete button
    with col6:
        if st.button("Delete", key=f"delete_{i}"):
            df = df.drop(i).reset_index(drop=True)
            save_df()
            st.success(f"Task {i + 1} deleted!")

    # Save changes when the task name or priority is updated
    if new_todo_name != row['todo_name'] or new_priority != row['priority']:
        df.loc[i, 'todo_name'] = new_todo_name
        df.loc[i, 'priority'] = new_priority
        df.loc[i, 'status'] = status
        save_df()
        st.success(f"Task {i + 1} updated!")

# Add a new task section
st.write("### Add New Task")
todo_name = st.text_input("Enter New ToDo", key="new_task")
priority = st.selectbox("Select priority", ["1", "2", "3", "4", "5"], key="new_priority")
add_button = st.button("Add New ToDo")

# When the "Add Task" button is clicked
if add_button and todo_name:
    # Add the new task to the dataframe
    new_task_df = pd.DataFrame([[todo_name, functions.get_current_time(), priority, "Incomplete"]],
                               columns=["todo_name", "create_time", "priority", "status"])
    df = pd.concat([df, new_task_df], ignore_index=True)
    save_df()
    st.success(f"New task '{todo_name}' added with priority '{priority}'!")

# Show the updated tasks table
st.write("### Updated ToDo List")
st.table(df)
