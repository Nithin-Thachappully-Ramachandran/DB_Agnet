import os
import streamlit as st
import altair as alt
import pandas as pd
from hdbcli import dbapi

# Install necessary packages
os.system('pip install hdbcli')

# Sidebar for database connection details
st.sidebar.title("Database Connection")
db_host = st.sidebar.text_input("Host")
db_port = st.sidebar.text_input("Port")
db_user = st.sidebar.text_input("Username")
db_password = st.sidebar.text_input("Password", type="password")
db_name = st.sidebar.text_input("Database Name")

# Function to create a database connection
def create_db_connection(host, port, user, password, db_name):
    try:
        conn = dbapi.connect(
            address=host,
            port=int(port),
            user=user,
            password=password,
            database=db_name
        )
        return conn
    except Exception as e:
        st.sidebar.error(f"Failed to connect to the database: {e}")
        return None

# Input validation for connection details
if db_host and db_port and db_user and db_password and db_name:
    conn = create_db_connection(db_host, db_port, db_user, db_password, db_name)
    if conn:
        st.sidebar.success("Connected to the database!")
else:
    conn = None
    st.sidebar.warning("Please enter all the database connection details.")

# Upload trace or log files
st.sidebar.title("Upload Files")
uploaded_files = st.sidebar.file_uploader("Upload Trace/Log Files", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.sidebar.success("Files uploaded successfully!")

# Main interface
st.title("DB Copilot")

# Chat-like interface for querying the database
st.write("### Chat with your Database")
query = st.text_area("Enter your SQL query here:")

if st.button("Execute"):
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            st.write(df)
            cursor.close()
        except Exception as e:
            st.error(f"Error executing query: {e}")
    else:
        st.error("No database connection available. Please provide valid connection details.")

# Analyze uploaded trace or log files
if uploaded_files:
    st.write("### Analyze Uploaded Files")
    for uploaded_file in uploaded_files:
        st.write(f"**{uploaded_file.name}**")
        file_contents = uploaded_file.read().decode("utf-8")
        st.text(file_contents)

# Close the database connection when done
if conn:
    conn.close()
