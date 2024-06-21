import streamlit as st
import json

# Sidebar for database connection details
st.sidebar.title("Database Connection")
db_host = st.sidebar.text_input("Host")
db_port = st.sidebar.text_input("Port")
db_user = st.sidebar.text_input("Username")
db_password = st.sidebar.text_input("Password", type="password")
db_name = st.sidebar.text_input("Database Name")

# Save connection details
connection_details = {
    "host": db_host,
    "port": db_port,
    "user": db_user,
    "password": db_password,
    "database": db_name
}

# Chat-like interface for querying the database
st.title("DB Copilot")
query = st.text_area("Enter your SQL query here:")

# Create hidden endpoints for connection details and query
if st.button("Save"):
    with open('connection_details.json', 'w') as json_file:
        json.dump(connection_details, json_file)
    with open('query.sql', 'w') as query_file:
        query_file.write(query)
    st.success("Details saved successfully!")

@st.cache_data
def get_connection_details():
    with open('connection_details.json', 'r') as json_file:
        return json.load(json_file)

@st.cache_data
def get_query():
    with open('query.sql', 'r') as query_file:
        return query_file.read()

# Expose endpoints
st.json(get_connection_details())
st.code(get_query())
