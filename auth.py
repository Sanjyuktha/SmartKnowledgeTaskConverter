import hashlib
import streamlit as st
from mongodb import db # Imports your active client connection

users_collection = db["users"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def render_login_signup():
    st.markdown("<h2 style='text-align: center; color: #0B1F3A;'>🔐 Access Control Portal</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    
    with tab1:
        login_user = st.text_input("Username / Email", key="login_user").strip().lower()
        login_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login", use_container_width=True):
            if login_user and login_pass:
                user_record = users_collection.find_one({"username": login_user})
                if user_record and user_record["password"] == hash_password(login_pass):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = login_user
                    st.success("Welcome back!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            else:
                st.warning("Please fill in all fields.")

    with tab2:
        reg_user = st.text_input("Choose Username / Email", key="reg_user").strip().lower()
        reg_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        
        if st.button("Register", use_container_width=True):
            if reg_user and reg_pass:
                existing_user = users_collection.find_one({"username": reg_user})
                if existing_user:
                    st.error("Username already exists!")
                else:
                    users_collection.insert_one({
                        "username": reg_user,
                        "password": hash_password(reg_pass)
                    })
                    st.success("Account created successfully! Please Sign In.")
            else:
                st.warning("Please fill in all fields.")
