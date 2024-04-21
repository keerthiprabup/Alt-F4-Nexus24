import pickle
from pathlib import Path
import hashlib
import streamlit as st

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

users_data_file = Path("users_data.pkl")
if users_data_file.exists():
    with users_data_file.open("rb") as file:
        users_data = pickle.load(file)
else:
    users_data = {}

def save_user_data():
    with users_data_file.open("wb") as file:
        pickle.dump(users_data, file)

def register_user(email, username, password):
    if username in users_data:
        st.error("Username already exists. Please choose a different one.")
        return
    
    hashed_password = hash_password(password)
    users_data[username] = {"email": email, "password": hashed_password}
    save_user_data()
    # st.success("Registration successful!")
    st.session_state["logged_in"] = username
    st.experimental_rerun()

def verify_login(username, password):
    hashed_password = hash_password(password)
    return users_data.get(username, {}).get("password") == hashed_password

def main():
    st.title("Saheli Authentication System")
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = None

    if st.session_state["logged_in"] is None:
        page = st.sidebar.radio("Navigation", ["Login", "Register"])
    else:
        st.sidebar.write("Logged in as:", st.session_state["logged_in"])
        page = st.sidebar.radio("Navigation", ["Dashboard", "Logout"])

    if page == "Register":
        st.header("User Registration")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Register"):
            if password == confirm_password:
                register_user(email, username, password)
            else:
                st.error("Passwords do not match.")

    elif page == "Login":
        st.header("User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_login(username, password):
                st.session_state["logged_in"] = username
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")

    elif page == "Dashboard":
        st.header("Dashboard")
        if st.session_state["logged_in"] is not None:
            st.write(f"Welcome to the dashboard, {st.session_state['logged_in']}!")
            st.write("You can add your dashboard content here.")
        else:
            st.error("You need to log in first.")

    elif page == "Logout":
        if st.session_state["logged_in"] is not None:
            # st.success(f"Goodbye, {st.session_state['logged_in']}!")
            st.session_state["logged_in"] = None
            st.experimental_rerun()

if __name__ == "__main__":
    main()
