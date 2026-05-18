import streamlit as st
from db import execute_query


def create_user_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employee (
        employee_id INT NOT NULL AUTO_INCREMENT,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        PRIMARY KEY (employee_id)
    )
    """
    execute_query(create_table_query, fetch=False)


def signup(username, password):
    if not username or not password:
        st.error("Provide username and password.")
        return
    check_query = "SELECT * FROM employee WHERE username = %s"
    existing = execute_query(check_query, (username,))
    if not existing.empty:
        st.error("Username already exists. Please choose a different username.")
        return
    insert_query = "INSERT INTO employee (username, password) VALUES (%s, %s)"
    execute_query(insert_query, (username, password), fetch=False)
    st.success("Signup successful. You can now log in.")


def login(username, password):
    if not username or not password:
        st.error("Provide username and password.")
        return
    query = "SELECT * FROM employee WHERE username = %s AND password = %s"
    result = execute_query(query, (username, password))
    if not result.empty:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.success("Login successful!")
    else:
        st.error("Invalid username or password.")


def check_authentication():
    if not st.session_state.get('authenticated'):
        st.error("Not authenticated. Please log in.")
        st.stop()
