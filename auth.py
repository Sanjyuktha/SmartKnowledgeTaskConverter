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

    # ----------------------------------------------------
    # PREMIUM SPLIT-SCREEN DESIGN ENGINE
    # ----------------------------------------------------
    st.html("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
    /* Global Canvas Reset */
    .stApp {
        background: #050B14 !important;
    }
    
    /* Premium Typography & Layout Variables */
    h1, h2, h3, p, label, span {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Left Panel Aesthetic Sidecard */
    .design-sidecard {
        background: linear-gradient(135deg, #0A1626 0%, #050B14 100%);
        border: 1px solid rgba(212, 162, 76, 0.15);
        border-radius: 32px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 25px 60px rgba(0,0,0,0.4);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 75vh;
    }
    
    /* Right Panel Context Elements */
    .content-right {
        padding: 20px 40px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 75vh;
    }
    
    /* Massive Bold Headings for First Page */
    .huge-title {
        color: #FFFFFF !important;
        font-size: 64px !important;
        font-weight: 900 !important;
        letter-spacing: -2px !important;
        line-height: 1.1 !important;
        margin-bottom: 12px !important;
    }
    
    .gold-tagline {
        color: #D4A24C !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        font-style: italic !important;
        letter-spacing: 1.5px !important;
        line-height: 1.4 !important;
        text-transform: uppercase;
        margin-bottom: 40px !important;
    }

    /* Massive Headings for Second Page */
    .transform-title {
        color: #FFFFFF !important;
        font-size: 52px !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        margin-bottom: 8px !important;
        line-height: 1.2 !important;
    }
    
    .transform-sub {
        color: #8A99AD !important;
        font-size: 18px !important;
        font-weight: 400 !important;
        margin-bottom: 35px !important;
    }
    
    /* Premium Solid UI Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #D4A24C 0%, #F0C46C 100%) !important;
        color: #050B14 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 0.5px !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px 28px !important;
        box-shadow: 0 8px 24px rgba(212,162,76,0.25) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 32px rgba(212,162,76,0.45) !important;
        color: #050B14 !important;
    }
    
    /* Overriding Streamlit Form Inputs for Dark Premium Feel */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        color: #FFFFFF !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
    }
    
    .stTextInput input:focus {
        border-color: #D4A24C !important;
        box-shadow: 0 0 0 1px #D4A24C !important;
    }
    
    label {
        color: #A0AEC0 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-bottom: 6px !important;
    }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab"] {
        color: #718096 !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        padding-bottom: 10px !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #D4A24C !important;
        border-bottom-color: #D4A24C !important;
    }
    </style>
    """)

    # ----------------------------------------------------
    # PHASE 1: WELCOME BRAND SPLASH SCREEN (DESIGNER SPLIT)
    # ----------------------------------------------------
    if st.session_state["onboarding_step"] == "splash":
        st.markdown("<br><br>", unsafe_allow_html=True)
        col_left, col_right = st.columns([1.1, 1.3], gap="large")
        
        with col_left:
            st.markdown('<div class="design-sidecard">', unsafe_allow_html=True)
            logo_filename = "edited-image.png"
            if os.path.exists(logo_filename):
                img = Image.open(logo_filename)
                st.image(img, width=280)
            else:
                st.markdown('<div style="font-size:40px; color:#D4A24C;">[ REQ2TASK LOGO ]</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_right:
            st.markdown('<div class="content-right">', unsafe_allow_html=True)
            st.markdown('<h1 class="huge-title">REQ 2 TASK AI</h1>', unsafe_allow_html=True)
            st.markdown('<p class="gold-tagline">SMART REQUIREMENTS. INTELLIGENT TASKS. BETTER RESULTS.</p>', unsafe_allow_html=True)
            
            # Form-width matching call to action
            if st.button("GET STARTED!", key="btn_get_started"):
                st.session_state["onboarding_step"] = "portal"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------
    # PHASE 2: ACCESS CONTROL PORTAL (SPLIT + IN-BOX PASS EYE)
    # ----------------------------------------------------
    elif st.session_state["onboarding_step"] == "portal":
        st.markdown("<br><br>", unsafe_allow_html=True)
        col_left, col_right = st.columns([1.1, 1.3], gap="large")
        
        with col_left:
            st.markdown('<div class="design-sidecard">', unsafe_allow_html=True)
            logo_filename = "logo.png"
            if os.path.exists(logo_filename):
                img = Image.open(logo_filename)
                st.image(img, width=280)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_right:
            st.markdown('<div class="content-right">', unsafe_allow_html=True)
            st.markdown('<h1 class="transform-title">READY TO TRANSFORM?</h1>', unsafe_allow_html=True)
            st.markdown('<p class="transform-sub">Log into your workspace environment or deploy a fresh instance.</p>', unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Sign In", "Create Account"])
            
            with tab1:
                st.markdown("<br>", unsafe_allow_html=True)
                login_user = st.text_input("Username / Email", key="login_user").strip().lower()
                
                # Dynamic Native Streamlit Password Box (Eye is natively inside the frame right edge!)
                login_pass = st.text_input("Password", type="password", key="login_pass")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Access workspace", key="btn_access_ws"):
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
                
                # Dynamic Native Streamlit Password Box
                reg_pass = st.text_input("Choose Password", type="password", key="reg_pass")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Create workspace", key="btn_create_ws"):
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
            st.markdown('</div>', unsafe_allow_html=True)
