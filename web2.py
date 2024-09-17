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


# Display the tasks in a table format with interactive controls
st.write("### Manage Your Tasks")

for i, row in df.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])

    # Editable text input for the task name
    with col1:
        new_todo_name = st.text_input(f"Task {i + 1}", value=row['todo_name'], key=f"task_{i}")

    # Check if priority is NaN, if it is, default to "1"
    priority_value = row['priority']
    if pd.isna(priority_value):
        priority_value = "1"  # Default priority if NaN is found

    # Dropdown for priority selection
    with col2:
        new_priority = st.selectbox(f"Priority {i + 1}", ["1", "2", "3", "4", "5"], index=int(priority_value) - 1,
                                    key=f"priority_{i}")

    # Mark as complete or incomplete
    with col3:
        status = st.selectbox(f"Status {i + 1}", ["Incomplete", "Complete"],
                              index=0 if row['status'] == "Incomplete" else 1, key=f"status_{i}")

    # Button to save changes (edit task and priority)
    with col4:
        if st.button("Save Changes", key=f"save_{i}"):
            df.loc[i, 'todo_name'] = new_todo_name
            df.loc[i, 'priority'] = new_priority
            df.loc[i, 'status'] = status
            save_df()
            st.success(f"Task {i + 1} updated!")

    # Button to delete the task
    with col5:
        if st.button("Delete", key=f"delete_{i}"):
            df = df.drop(i).reset_index(drop=True)
            save_df()
            st.success(f"Task {i + 1} deleted!")

    # Button to mark as complete if it's not already completed
    with col6:
        if status == "Incomplete" and st.button("Complete", key=f"complete_{i}"):
            df.loc[i, 'status'] = "Complete"
            save_df()
            st.success(f"Task {i + 1} marked as complete!")

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
