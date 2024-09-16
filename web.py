import streamlit as st
import functions
import pandas as pd

todos = functions.load_existing_todos()

st.title("ZenDo")
st.subheader("Todo App in Zen Mode")
st.write("This app is to increase your productivity")

todos_tbl = pd.DataFrame(columns=['todo_name', 'create_time', 'update_time', 'priority', 'status'])

df = pd.read_csv("todo.csv")
st.write(df)


#for todo in todos:
#    st.checkbox(todo['todo_name'])

#pd.read_csv(todos.csv)


#st.text_input(label="", placeholder="Add New Todo")

#st.table(todos_tbl)
