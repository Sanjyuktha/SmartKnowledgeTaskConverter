import hashlib
import os
import streamlit as st
from PIL import Image
from mongodb import db

users_collection = db["users"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def render_login_signup():
    # Initialize onboarding step state manager
    if "onboarding_step" not in st.session_state:
        st.session_state["onboarding_step"] = "splash"

    # ----------------------------------------------------
    # PREMIUM DESIGNER LIGHT INTERFACE STYLING
    # ----------------------------------------------------
    st.html("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
    /* Premium Light Theme App Canvas background layout mirroring template style */
    .stApp {
        background: linear-gradient(135deg, #E2E8F0 0%, #F8FAFC 100%) !important;
    }
    
    /* Global Typography Reset */
    h1, h2, h3, p, label, span, button {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Clean Premium White Workspace Card Wrapper Container */
    .premium-workspace-card {
        background: #FFFFFF !important;
        border-radius: 24px !important;
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.08) !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        padding: 50px !important;
        margin-top: 2vh;
    }
    
    /* Massive Bold Headings for First Page Splash */
    .splash-desktop-title {
        color: #0F172A !important;
        font-size: 54px !important;
        font-weight: 900 !important;
        letter-spacing: -2px !important;
        line-height: 1.1 !important;
        margin-bottom: 8px !important;
    }
    
    .splash-desktop-tagline {
        color: #475569 !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        font-style: italic !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        margin-bottom: 35px !important;
    }

    /* Massive Headings for Second Page Access */
    .transform-desktop-title {
        color: #0F172A !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        margin-bottom: 8px !important;
    }
    
    .transform-desktop-sub {
        color: #64748B !important;
        font-size: 16px !important;
        font-weight: 400 !important;
        margin-bottom: 30px !important;
    }
    
    /* Corporate Styled UI Buttons Override */
    div.stButton > button {
        background: #0F172A !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 14px 28px !important;
        box-shadow: 0 4px 12px rgba(15,23,42,0.15) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        background: #1E293B !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 20px rgba(15,23,42,0.25) !important;
        color: #FFFFFF !important;
    }
    
    /* Back Navigation Button Specific Style Override */
    div.stButton > button[key^="back_btn"] {
        background: transparent !important;
        color: #64748B !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: none !important;
        padding: 8px 16px !important;
        font-size: 13px !important;
        width: auto !important;
    }
    div.stButton > button[key^="back_btn"]:hover {
        background: #F1F5F9 !important;
        color: #0F172A !important;
    }
    
    /* Input Form Elements Override for Crisp Slate Theme */
    .stTextInput input {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        color: #0F172A !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
    }
    
    .stTextInput input:focus {
        border-color: #0F172A !important;
        box-shadow: 0 0 0 1px #0F172A !important;
    }
    
    label {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 6px !important;
    }
    
    /* Tabs Navigation Customization styling overrides */
    .stTabs [data-baseweb="tab"] {
        color: #64748B !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0F172A !important;
        border-bottom-color: #0F172A !important;
    }
    </style>
    """)

    # ----------------------------------------------------
    # PAGE 1: SPLASH SCREEN (CLEAN LIGHT DESKTOP SPLIT)
    # ----------------------------------------------------
    if st.session_state["onboarding_step"] == "splash":
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Outer alignment wrapper using standard native Streamlit grid matrix
        _, center_container, _ = st.columns([0.4, 2.5, 0.4])
        
        with center_container:
            st.markdown('<div class="premium-workspace-card">', unsafe_allow_html=True)
            
            # Interior desktop horizontal division block
            col_left, col_right = st.columns([1.1, 1.3], gap="large")
            
            with col_left:
                logo_filename = "logo.png"
                if os.path.exists(logo_filename):
                    img = Image.open(logo_filename)
                    st.image(img, use_container_width=True)
                else:
                    st.info("Upload 'logo.png' to GitHub repository folder layer.")
                    
            with col_right:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown('<h1 class="splash-desktop-title">REQ 2 TASK AI</h1>', unsafe_allow_html=True)
                st.markdown('<p class="splash-desktop-tagline">SMART REQUIREMENTS. INTELLIGENT TASKS. BETTER RESULTS.</p>', unsafe_allow_html=True)
                
                if st.button("GET STARTED!", key="splash_get_started_action"):
                    st.session_state["onboarding_step"] = "portal"
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------
    # PAGE 2: PORTAL ENTRY SCREEN (WITH EYE + FUNCTIONAL BACK NAVIGATION)
    # ----------------------------------------------------
    elif st.session_state["onboarding_step"] == "portal":
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        _, center_container, _ = st.columns([0.4, 2.5, 0.4])
        
        with center_container:
            st.markdown('<div class="premium-workspace-card">', unsafe_allow_html=True)
            
            # Interactive Back Button to return gracefully to Page 1
            if st.button("← Back to Welcome Screen", key="back_btn_nav"):
                st.session_state["onboarding_step"] = "splash"
                st.rerun()
                
            st.markdown("<br>", unsafe_allow_html=True)
            col_left, col_right = st.columns([1.1, 1.3], gap="large")
            
            with col_left:
                logo_filename = "logo.png"
                if os.path.exists(logo_filename):
                    img = Image.open(logo_filename)
                    st.image(img, use_container_width=True)
            
            with col_right:
                st.markdown('<h1 class="transform-desktop-title">READY TO TRANSFORM?</h1>', unsafe_allow_html=True)
                st.markdown('<p class="transform-desktop-sub">Log into your workspace environment or deploy a fresh instance.</p>', unsafe_allow_html=True)
                
                tab1, tab2 = st.tabs(["Sign In", "Create Account"])
                
                with tab1:
                    st.markdown("<br>", unsafe_allow_html=True)
                    login_user = st.text_input("Username / Email", key="login_user").strip().lower()
                    
                    # NATIVE EYE CONFIGURATION: Renders beautifully inside the field frame bounding box automatically
                    login_pass = st.text_input("Password", type="password", key="login_pass")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Access workspace", key="submit_login_btn"):
                        if login_user and login_pass:
                            user_record = users_collection.find_one({"username": login_user})
                            if user_record and user_record["password"] == hash_password(login_pass):
                                st.session_state["authenticated"] = True
                                st.session_state["username"] = login_user
                                st.success("Opening workspace...")
                                st.rerun()
                            else:
                                st.error("Invalid credentials.")
                        else:
                            st.warning("Please fill in all parameters.")

                with tab2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    reg_user = st.text_input("Choose Username / Email", key="reg_user").strip().lower()
                    reg_pass = st.text_input("Choose Password", type="password", key="reg_pass")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Create workspace", key="submit_register_btn"):
                        if reg_user and reg_pass:
                            existing_user = users_collection.find_one({"username": reg_user})
                            if existing_user:
                                st.error("Username already exists.")
                            else:
                                users_collection.insert_one({
                                    "username": reg_user,
                                    "password": hash_password(reg_pass)
                                })
                                st.success("Workspace created! Please Sign In.")
                        else:
                            st.warning("Please fill in all fields.")
                            
            st.markdown('</div>', unsafe_allow_html=True)
