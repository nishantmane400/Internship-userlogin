import streamlit as st
import json
import os
from datetime import datetime

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="CMS Portal", page_icon="🔐", layout="centered")

# --- DATABASE LOGIC (STORES FULL USER DETAILS) ---
DB_FILE = "users_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    # Initial Default Admin as per your documentation
    return {
        "admin@system.com": {
            "full_name": "System Admin",
            "password": "admin123",
            "role": "Admin",
            "status": "active",
            "created_at": str(datetime.now())
        }
    }

def save_user(email, name, password, role):
    db = load_db()
    db[email] = {
        "full_name": name,
        "password": password,
        "role": role,
        "status": "active",
        "created_at": str(datetime.now())
    }
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = None

# --- UI THEMING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #3b82f6; color: white; }
    h1, h2, h3 { color: #3b82f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🛡️ CMS AUTH")
    if not st.session_state['logged_in']:
        choice = st.radio("MENU", ["Login", "Register"])
    else:
        st.write(f"**Logged in as:** {st.session_state['user_data']['full_name']}")
        st.write(f"**Role:** {st.session_state['user_data']['role']}")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['user_data'] = None
            st.rerun()
        choice = "Dashboard"

# 3. MAIN INTERFACE LOGIC
db = load_db()

if not st.session_state['logged_in']:
    if choice == "Login":
        st.header("Admin or User Login")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if st.button("SIGN IN"):
            if email in db and db[email]['password'] == password:
                st.session_state['logged_in'] = True
                st.session_state['user_data'] = db[email]
                st.rerun()
            else:
                st.error("Authentication failed. Please check credentials.")

    elif choice == "Register":
        st.header("User Registration")
        new_name = st.text_input("Full Name")
        new_email = st.text_input("Email (Unique ID)")
        new_pass = st.text_input("Password", type="password")
        # Role selection as per your "Functionalites to be Designed" image
        new_role = st.selectbox("Assign Role", ["User", "Salesperson", "Admin"])
        
        if st.button("CREATE ACCOUNT"):
            if not new_name or not new_email or not new_pass:
                st.error("All fields are mandatory.")
            elif new_email in db:
                st.warning("User already exists with this email.")
            else:
                save_user(new_email, new_name, new_pass, new_role)
                st.success("Registration Successful! You can now login.")

else:
    # 4. DASHBOARD (Role-Based Access)
    user = st.session_state['user_data']
    st.header(f"Welcome to Dashboard, {user['full_name']}!")
    
    # Visualizing Role-Based Access as per your requirement
    if user['role'] == "Admin":
        st.info("🔓 **ADMIN PRIVILEGES GRANTED**: You can manage users and invoices.")
        st.write("### System Statistics")
        st.columns(3)[0].metric("Total Users", len(db))
    
    elif user['role'] == "Salesperson":
        st.warning("🔒 **RESTRICTED ACCESS**: You can only access Sales & Leads features.")
        
    else:
        st.success("👤 **STANDARD USER**: You can view your personal profile and data.")

    st.write("---")
    st.json(user) # Displaying the session data based on the User Table schema
