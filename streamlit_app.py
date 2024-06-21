import streamlit as st
import os
import json

# Sidebar for database connection details
st.sidebar.title("Database Connection")
db_host = st.sidebar.text_input("Host")
db_port = st.sidebar.text_input("Port")
db_user = st.sidebar.text_input("Username")
db_password = st.sidebar.text_input("Password", type="password")
db_name = st.sidebar.text_input("Database Name")

# Input validation for connection details
if st.sidebar.button("Save Connection Details"):
    if db_host and db_port and db_user and db_password and db_name:
        connection_details = {
            "host": db_host,
            "port": db_port,
            "user": db_user,
            "password": db_password,
            "database": db_name
        }
        with open('connection_details.json', 'w') as json_file:
            json.dump(connection_details, json_file)
        st.sidebar.success("Connection details saved successfully!")
    else:
        st.sidebar.warning("Please enter all the database connection details.")

# Chat-like interface for querying the database
st.title("DB Copilot")
query = st.text_area("Enter your SQL query here:")

if st.button("Save Query"):
    if query:
        with open('query.sql', 'w') as query_file:
            query_file.write(query)
        st.success("Query saved successfully!")
    else:
        st.warning("Please enter a query.")
