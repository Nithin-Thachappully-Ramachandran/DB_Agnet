import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import sqlite3

# Database setup
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY,
    x REAL,
    y REAL,
    idx REAL,
    rand REAL
)
''')
conn.commit()

# Sidebar navigation
st.sidebar.title("DB Agent")
section = st.sidebar.radio("Go to", ["Home", "Add Data", "View Data", "Update Data", "Delete Data", "Visualize"])

# Home section
if section == "Home":
    st.title("Welcome to the Database Agent")
    st.write("Use the sidebar to navigate through different options.")

# Add Data section
elif section == "Add Data":
    st.title("Add Data")
    with st.form("add_form"):
        x = st.number_input("X value", value=0.0)
        y = st.number_input("Y value", value=0.0)
        idx = st.number_input("Index value", value=0.0)
        rand = st.number_input("Random value", value=0.0)
        submitted = st.form_submit_button("Add")
        if submitted:
            c.execute("INSERT INTO data (x, y, idx, rand) VALUES (?, ?, ?, ?)", (x, y, idx, rand))
            conn.commit()
            st.success("Data added successfully!")

# View Data section
elif section == "View Data":
    st.title("View Data")
    df = pd.read_sql_query("SELECT * FROM data", conn)
    st.write(df)

# Update Data section
elif section == "Update Data":
    st.title("Update Data")
    df = pd.read_sql_query("SELECT * FROM data", conn)
    ids = df['id'].tolist()
    selected_id = st.selectbox("Select ID to update", ids)
    if selected_id:
        row = df[df['id'] == selected_id]
        x = st.number_input("X value", value=row['x'].values[0])
        y = st.number_input("Y value", value=row['y'].values[0])
        idx = st.number_input("Index value", value=row['idx'].values[0])
        rand = st.number_input("Random value", value=row['rand'].values[0])
        if st.button("Update"):
            c.execute("UPDATE data SET x=?, y=?, idx=?, rand=? WHERE id=?", (x, y, idx, rand, selected_id))
            conn.commit()
            st.success("Data updated successfully!")

# Delete Data section
elif section == "Delete Data":
    st.title("Delete Data")
    df = pd.read_sql_query("SELECT * FROM data", conn)
    ids = df['id'].tolist()
    selected_id = st.selectbox("Select ID to delete", ids)
    if selected_id:
        if st.button("Delete"):
            c.execute("DELETE FROM data WHERE id=?", (selected_id,))
            conn.commit()
            st.success("Data deleted successfully!")

# Visualize Data section
elif section == "Visualize":
    st.title("Visualize Data")
    df = pd.read_sql_query("SELECT * FROM data", conn)
    
    if not df.empty:
        num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
        num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

        indices = np.linspace(0, 1, num_points)
        theta = 2 * np.pi * num_turns * indices
        radius = indices

        x = radius * np.cos(theta)
        y = radius * np.sin(theta)

        df = pd.DataFrame({
            "x": x,
            "y": y,
            "idx": indices,
            "rand": np.random.randn(num_points),
        })

        st.altair_chart(alt.Chart(df, height=700, width=700)
            .mark_point(filled=True)
            .encode(
                x=alt.X("x", axis=None),
                y=alt.Y("y", axis=None),
                color=alt.Color("idx", legend=None, scale=alt.Scale()),
                size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
            ))
    else:
        st.write("No data available to visualize.")

# Close the database connection
conn.close()
