import streamlit as st
from PIL import Image
import base64
import io
import json
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Nishant - Login Form",
    page_icon="👤",
    layout="centered"
)

# ---------------- DATABASE ----------------
DB_FILE = "users_db.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"admin": "admin123"}  # default user

def save_user(username, password):
    users = load_users()
    users[username] = password
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

# ---------------- IMAGE HELPER ----------------
def get_base64_image(img_path):
    try:
        img = Image.open(img_path)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    except:
        return ""

# ---------------- CSS THEME ----------------
st.markdown("""
<style>
/* Animated Gradient Background */
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1a1a2e !important;
}

/* Headers */
h2, h3 {
    color: #e0e0ff !important;
    font-family: 'Segoe UI', sans-serif;
}

/* Inputs */
input {
    background-color: #1f1f3a !important;
    color: white !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    color: white !important;
    width: 100%;
    border-radius: 8px;
    border: none;
    height: 45px;
    font-size: 16px;
}

/* Success / Error */
div[data-baseweb="notification"] {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    pfp_data = get_base64_image("pfp.jpg")
    if pfp_data:
        st.markdown(f"""
            <div style="text-align:center;">
                <img src="data:image/jpeg;base64,{pfp_data}"
                     style="width:120px;height:120px;border-radius:15px;
                     border:2px solid white;margin-bottom:15px;">
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center;'>Nishant</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#bbb;'>Secure Login System</p>", unsafe_allow_html=True)
    st.markdown("---")

    mode = st.radio("CHOOSE ACTION", ["LOGIN", "REGISTER"])
    st.markdown("---")
    st.caption("Permanent Database Enabled")

# ---------------- MAIN CONTENT ----------------
if mode == "LOGIN":
    st.markdown("## Account Login")

    user_input = st.text_input("USERNAME")
    pass_input = st.text_input("PASSWORD", type="password")

    if st.button("SIGN IN"):
        if user_input in users and users[user_input] == pass_input:
            st.success(f"Welcome back, {user_input}!")
            st.balloons()
        else:
            st.error("Invalid Username or Password")

elif mode == "REGISTER":
    st.markdown("## Create Account")

    new_user = st.text_input("NEW USERNAME")
    new_pass = st.text_input("NEW PASSWORD", type="password")
    confirm_pass = st.text_input("CONFIRM PASSWORD", type="password")

    if st.button("REGISTER"):
        if new_user in users:
            st.warning("Username already taken.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif new_user and new_pass:
            save_user(new_user, new_pass)
            st.success("Registration Successful! You can now login.")
        else:
            st.error("Fields cannot be empty.")
