import streamlit as st
import mysql.connector

# Function to connect to the database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="90006@Bhagi",  # Replace with your MySQL password
        database="user_auth"  # Replace with your database name
    )

# Function to add a user to the database
def add_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()

# Function to retrieve a user from the database
def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Sign-Up Page
def sign_up():
    st.title("Sign-Up")
    st.subheader("Create a new account")

    username = st.text_input("Enter a Username")
    password = st.text_input("Enter a Password", type="password")
    confirm_password = st.text_input("Confirm Your Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif not username or not password:
            st.error("Username and Password cannot be empty.")
        else:
            if add_user(username, password):
                st.success("Account created successfully! You can now log in.")
                st.info("Switch to the Login page from the sidebar.")
            else:
                st.error("Username already exists. Please choose a different one.")

# Login Page
def login():
    st.title("Login")
    st.subheader("Access Your Account")

    username = st.text_input("Enter Your Username")
    password = st.text_input("Enter Your Password", type="password")

    if st.button("Login"):
        user_record = get_user(username)
        if user_record and user_record[0] == password:
            st.success(f"Welcome, {username}!! Scroll Down 👇🏻 for DashBoard!")
            st.balloons()
            show_dashboard()  # Show the dashboard after successful login
        else:
            st.error("Invalid username or password. Please try again.")

# Dashboard Page (displayed after login)
def show_dashboard():
    st.title("India City GDP and Productivity Metrics")

    # Embed the Power BI report
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiZjdmYzAzMzktMWMxMC00YjFmLTliOGYtNDRlMGEyMzJkMWVkIiwidCI6IjVjYTE3NzIwLTcyNTYtNGE0Ni1hNWIyLTBhN2ZkNjNjMWI4YiJ9"

    # Create an iframe to display the Power BI report
    st.markdown(
        f"""
        <iframe 
            width="100%" 
            height="600" 
            src="{powerbi_url}" 
            frameborder="0" 
            allowFullScreen="true"></iframe>
        """,
        unsafe_allow_html=True,
    )

    # Add a logout button
    if st.button("Logout"):
        st.session_state.clear()  # Clear the session state
        st.success("You have been logged out!")
        st.info("Redirecting to Login page...")
        login()  # Go back to login page after logout

# Main App Logic
def main():
    # If user is already logged in, show the dashboard page
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        show_dashboard()  # Show the dashboard directly if logged in
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Login", "Sign-Up"])

        if page == "Sign-Up":
            sign_up()
        else:
            login()

if __name__ == "__main__":
    main()
