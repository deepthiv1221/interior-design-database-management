import streamlit as st
import mysql.connector
import pandas as pd

# Configure MySQL connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1221",
        database="druthi"
    )

# Login function
def login(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE Email=%s AND Password=%s", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Display table data
def display_table_data(table):
    conn = get_connection()
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Insert data into tables
def insert_data(table, data):
    conn = get_connection()
    cursor = conn.cursor()

    if table == "Users":
        cursor.execute(
            "INSERT INTO Users (UserID, Name, Address, Phone, Email, Password) VALUES (%s, %s, %s, %s, %s, %s)",
            (data["UserID"], data["Name"], data["Address"], data["Phone"], data["Email"], data["Password"])
        )
    elif table == "Clients":
        cursor.execute(
            "INSERT INTO Clients (ClientID, Name, ContactInfo, Address) VALUES (%s, %s, %s, %s)",
            (data["ClientID"], data["Name"], data["ContactInfo"], data["Address"])
        )
    elif table == "Designers":
        cursor.execute(
            "INSERT INTO Designers (DesignerID, Name, Specialization, ContactInfo) VALUES (%s, %s, %s, %s)",
            (data["DesignerID"], data["Name"], data["Specialization"], data["ContactInfo"])
        )
    elif table == "Projects":
        cursor.execute(
            "INSERT INTO Projects (ProjectID, ProjectName, StartDate, EndDate, ClientID, DesignerID) VALUES (%s, %s, %s, %s, %s, %s)",
            (data["ProjectID"], data["ProjectName"], data["StartDate"], data["EndDate"], data["ClientID"], data["DesignerID"])
        )
    elif table == "Rooms":
        cursor.execute(
            "INSERT INTO Rooms (RoomID, RoomType, ProjectID) VALUES (%s, %s, %s)",
            (data["RoomID"], data["RoomType"], data["ProjectID"])
        )
    elif table == "Furniture":
        cursor.execute(
            "INSERT INTO Furniture (FurnitureID, FurnitureName, FurnitureType, RoomID, MaterialID) VALUES (%s, %s, %s, %s, %s)",
            (data["FurnitureID"], data["FurnitureName"], data["FurnitureType"], data["RoomID"], data["MaterialID"])
        )
    elif table == "Materials":
        cursor.execute(
            "INSERT INTO Materials (MaterialID, MaterialName, Description) VALUES (%s, %s, %s)",
            (data["MaterialID"], data["MaterialName"], data["Description"])
        )

    conn.commit()
    conn.close()

# Update data in tables
def update_data(table, primary_key, primary_value, data):
    conn = get_connection()
    cursor = conn.cursor()

    set_clause = ", ".join([f"{key}=%s" for key in data.keys()])
    values = list(data.values())
    values.append(primary_value)

    query = f"UPDATE {table} SET {set_clause} WHERE {primary_key}=%s"
    cursor.execute(query, values)

    conn.commit()
    conn.close()

# Delete data from tables
def delete_data(table, primary_key, primary_value):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"DELETE FROM {table} WHERE {primary_key}=%s"
    cursor.execute(query, (primary_value,))
    conn.commit()
    conn.close()

def home_page():
    st.title("Interior Designing Management System")
    st.subheader("Home")

    # Background image and introduction
    st.image("C:\\Users\\deept\\Downloads\\blue background.jpeg", use_column_width=True)
    st.write("""
        Welcome to the world of interior designing! Explore and manage your projects, clients, and materials with ease.
    """)

    st.markdown("---")

    # Interactive features section with icons
    st.subheader("Explore Features")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("🏠 Projects")
        st.write("Manage your projects from inception to completion.")
        st.image("C:\\Users\\deept\\Downloads\\projects.jpeg", use_column_width=True)

    with col2:
        st.header("👩‍💼 Clients")
        st.write("Keep track of client details and communications.")
        st.image("C:\\Users\\deept\\Downloads\\clients.jpeg", use_column_width=True)

    with col3:
        st.header("🛋️ Furniture")
        st.write("Catalog and manage furniture for each room.")
        st.image("C:\\Users\\deept\\Downloads\\furniture.jpeg", use_column_width=True)

    st.markdown("---")

    # Testimonials or client feedback section
    st.subheader("What Our Clients Say")
    st.write("Insert testimonials or client feedback here.")
    
    st.markdown("---")

    # Call to action with a playful touch
    st.subheader("Get Started")
    st.write("Ready to transform spaces? Login below!")
    
    if st.button("Login"):
        st.session_state.page = "Login"

    # Add footer or additional sections as needed

# Check if user is logged in and routing logic remains unchanged

def login_page():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid email or password")

def main():
    st.title("Interior Designing Management System")

    menu = ["Home", "Search", "Manage Data"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to Interior Designing")
        st.image("C:\\Users\\deept\\Downloads\\blue background.jpeg", use_column_width=True)
        st.write("""
            Explore the world of interior designing and manage your projects, clients, and materials with ease.
        """)

    elif choice == "Search":
        st.subheader("Search Data")
        table_choice = st.selectbox("Choose Table to View", ["Users", "Clients", "Designers", "Projects", "Rooms", "Furniture", "Materials"])
        df = display_table_data(table_choice)
        st.write(df)

    elif choice == "Manage Data":
        st.subheader("Manage Data")
        table_choice = st.selectbox("Choose Table", ["Users", "Clients", "Designers", "Projects", "Rooms", "Furniture", "Materials"])
        primary_keys = {
            "Users": "UserID",
            "Clients": "ClientID",
            "Designers": "DesignerID",
            "Projects": "ProjectID",
            "Rooms": "RoomID",
            "Furniture": "FurnitureID",
            "Materials": "MaterialID"
        }
        action = st.selectbox("Action", ["Insert", "Update", "Delete"])

        if action == "Insert":
            data = {}
            for column in display_table_data(table_choice).columns:
                data[column] = st.text_input(column)
            if st.button(f"Insert into {table_choice}"):
                insert_data(table_choice, data)
                st.success(f"{table_choice} inserted successfully!")

        elif action == "Update":
            primary_id = st.text_input(f"{primary_keys[table_choice]}")
            data = {}
            for column in display_table_data(table_choice).columns:
                if column != primary_keys[table_choice]:
                    data[column] = st.text_input(column)
            if st.button(f"Update {table_choice}"):
                update_data(table_choice, primary_keys[table_choice], primary_id, data)
                st.success(f"{table_choice} updated successfully!")

        elif action == "Delete":
            primary_id = st.text_input(f"{primary_keys[table_choice]}")
            if st.button(f"Delete {table_choice}"):
                delete_data(table_choice, primary_keys[table_choice], primary_id)
                st.success(f"{table_choice} deleted successfully!")

# Check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Routing logic
if st.session_state.logged_in:
    main()
else:
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Login":
        login_page()

# Define your CSS
css = """
.main {
    background-color: #cfe7ff; /* Light pink background */
    color: black;
}
input[type="text"], textarea {
    background-color: #aad4ff !important; /* Slightly darker shade of light pink */
    color: black !important; /* Text color to black */
}
table {
    background-color: #8ac6ff !important;
    color: black !important;
}
"""

# Inject HTML and CSS using markdown
st.markdown(f"""
    <style>
        {css}
    </style>
""", unsafe_allow_html=True)
