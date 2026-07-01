import hashlib
import os
import streamlit as st
from PIL import Image
from mongodb import db

users_collection = db["users"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def render_login_signup():
    if "onboarding_step" not in st.session_state:
        st.session_state["onboarding_step"] = "splash"

    # Initialize password visibility states if not present
    if "show_login_pass" not in st.session_state:
        st.session_state["show_login_pass"] = False
    if "show_reg_pass" not in st.session_state:
        st.session_state["show_reg_pass"] = False

    # ----------------------------------------------------
    # PREMIUM PORTAL LUXURY STYLING
    # ----------------------------------------------------
    st.html("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
    <style>
    .stApp {
        background: #081120 !important;
    }
    
    .splash-container {
        text-align: center;
        padding-top: 6vh;
        font-family: 'Inter', sans-serif;
    }
    
    .splash-title {
        color: #FFFFFF !important;
        font-size: 58px !important;
        font-weight: 900 !important;
        letter-spacing: -1px !important;
        margin-top: 15px !important;
        margin-bottom: 5px !important;
    }
    
    .splash-tagline {
        color: #D4A24C !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        font-style: italic !important;
        letter-spacing: 1px !important;
        margin-bottom: 40px !important;
    }
    
    /* Medium-sized premium button adjustment */
    div.stButton > button {
        background: linear-gradient(90deg, #D4A24C, #F0C46C) !important;
        color: #081120 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 20px !important;
        box-shadow: 0 6px 16px rgba(212,162,76,0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 10px 24px rgba(212,162,76,0.35) !important;
        color: #081120 !important;
    }
    
    label, p, span {
        color: #E2E8F0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #A0AEC0 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #D4A24C !important;
    }
    
    /* Password Eye Toggle Layout Alignment */
    .pass-container {
        position: relative;
    }
    </style>
    """)

    # ----------------------------------------------------
    # PHASE 1: WELCOME BRAND SPLASH SCREEN
    # ----------------------------------------------------
    if st.session_state["onboarding_step"] == "splash":
        st.markdown('<div class="splash-container">', unsafe_allow_html=True)
        
        logo_filename = "edited-image.png"
        
        if os.path.exists(logo_filename):
            img = Image.open(logo_filename)
            _, img_col, _ = st.columns([1, 0.6, 1])
            with img_col:
                st.image(img, use_container_width=True)
        else:
            st.markdown('<div style="font-size:40px; color:#D4A24C; margin-bottom:20px;">[ LOGO PLACEHOLDER ]</div>', unsafe_allow_html=True)

        st.markdown("""
            <div class="splash-title">REQ 2 TASK AI</div>
            <div class="splash-tagline">SMART REQUIREMENTS. INTELLIGENT TASKS. BETTER RESULTS.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        _, button_col, _ = st.columns([1, 1.0, 1])
        with button_col:
            if st.button("GET STARTED!", use_container_width=True):
                st.session_state["onboarding_step"] = "portal"
                st.rerun()

    # ----------------------------------------------------
    # PHASE 2: ACCESS CONTROL PORTAL (NO EMOJIS + DYNAMIC EYE PASSWORD)
    # ----------------------------------------------------
    elif st.session_state["onboarding_step"] == "portal":
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        _, form_col, _ = st.columns([1, 2, 1])
        with form_col:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 25px;">
                <h2 style='color: white !important; font-weight: 800; margin-bottom: 0;'>READY TO TRANSFORM?</h2>
                <p style='color: #A0AEC0 !important; font-size: 14px;'>Log into your workspace environment or deploy a fresh instance.</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.container(border=True):
                tab1, tab2 = st.tabs(["Sign In", "Create Account"])
                
                with tab1:
                    st.markdown("<br>", unsafe_allow_html=True)
                    login_user = st.text_input("Username / Email", key="login_user").strip().lower()
                    
                    # Password Input + Dynamic Eye State Toggle Configuration
                    pass_col, eye_col = st.columns([6, 1])
                    with pass_col:
                        login_type = "text" if st.session_state["show_login_pass"] else "password"
                        login_pass = st.text_input("Password", type=login_type, key="login_pass_field")
                    with eye_col:
                        st.markdown("<div style='padding-top:28px;'></div>", unsafe_allow_html=True)
                        eye_icon = "👁️" if st.session_state["show_login_pass"] else "👁️‍🗨️"
                        if st.button(eye_icon, key="toggle_login_eye", help="Toggle password view"):
                            st.session_state["show_login_pass"] = not st.session_state["show_login_pass"]
                            st.rerun()
                            
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Access workspace", use_container_width=True):
                        if login_user and login_pass:
                            user_record = users_collection.find_one({"username": login_user})
                            if user_record and user_record["password"] == hash_password(login_pass):
                                st.session_state["authenticated"] = True
                                st.session_state["username"] = login_user
                                st.success("Authorization Granted. Opening workspace...")
                                st.rerun()
                            else:
                                st.error("Access Denied: Invalid credentials.")
                        else:
                            st.warning("Please fill in all verification parameters.")

                with tab2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    reg_user = st.text_input("Choose Username / Email", key="reg_user").strip().lower()
                    
                    # Password Input + Dynamic Eye State Toggle Configuration
                    reg_pass_col, reg_eye_col = st.columns([6, 1])
                    with reg_pass_col:
                        reg_type = "text" if st.session_state["show_reg_pass"] else "password"
                        reg_pass = st.text_input("Choose Password", type=reg_type, key="reg_pass_field")
                    with reg_eye_col:
                        st.markdown("<div style='padding-top:28px;'></div>", unsafe_allow_html=True)
                        reg_eye_icon = "👁️" if st.session_state["show_reg_pass"] else "👁️‍🗨️"
                        if st.button(reg_eye_icon, key="toggle_reg_eye", help="Toggle password view"):
                            st.session_state["show_reg_pass"] = not st.session_state["show_reg_pass"]
                            st.rerun()
                            
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Create workspace", use_container_width=True):
                        if reg_user and reg_pass:
                            existing_user = users_collection.find_one({"username": reg_user})
                            if existing_user:
                                st.error("Account registration blocked: Username already exists.")
                            else:
                                users_collection.insert_one({
                                    "username": reg_user,
                                    "password": hash_password(reg_pass)
                                })
                                st.success("Workspace provisioned! Proceed to Sign In tab.")
                        else:
                            st.warning("Please define all structural configurations.")
