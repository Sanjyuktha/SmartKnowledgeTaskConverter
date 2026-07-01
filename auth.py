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
    # PREMIUM UNIFIED DESIGNER CARD LAYOUT
    # ----------------------------------------------------
    st.html("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
    /* Absolute Clean Slate Light Theme Canvas Background */
    .stApp {
        background: linear-gradient(135deg, #EEF2F6 0%, #F8FAFC 100%) !important;
    }
    
    /* Remove default Streamlit top headers and padding completely */
    [data-testid="stHeader"], [data-testid="stSidebarHideRepoButton"] {
        display: none !important;
    }
    .main .block-container {
        padding-top: 4vh !important;
        max-width: 100% !important;
    }
    
    /* THE FIX: Unified Master Box Container matching your exact design templates */
    .master-designer-box {
        display: flex;
        flex-direction: row;
        width: 100%;
        min-height: 70vh;
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 24px !important;
        box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.08) !important;
        overflow: hidden;
    }
    
    /* Left Panel: Crisp Slate Graphic Frame */
    .workspace-left-pane {
        flex: 1;
        background: #F8FAFC;
        border-right: 1px solid #E2E8F0;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
    }
    
    .workspace-left-pane img {
        max-width: 85%;
        height: auto;
        border-radius: 16px;
    }
    
    /* Right Panel: Functional Core Elements */
    .workspace-right-pane {
        flex: 1.2;
        padding: 60px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: #FFFFFF;
    }
    
    /* Clean Non-overlapping Typography */
    .splash-core-title {
        color: #0F172A !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 52px !important;
        font-weight: 900 !important;
        letter-spacing: -2px !important;
        margin: 0 0 10px 0 !important;
        line-height: 1.1 !important;
    }
    
    .splash-core-tagline {
        color: #475569 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        font-style: italic !important;
        letter-spacing: 1.2px !important;
        margin: 0 0 40px 0 !important;
        line-height: 1.4 !important;
    }
    
    .portal-core-title {
        color: #0F172A !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 40px !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        margin: 0 0 8px 0 !important;
    }
    
    .portal-core-sub {
        color: #64748B !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        margin: 0 0 30px 0 !important;
    }
    
    /* Premium Solid Block Action Buttons */
    div.stButton > button {
        background: #0F172A !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 14px 28px !important;
        box-shadow: 0 4px 12px rgba(15,23,42,0.15) !important;
        transition: all 0.2s ease !important;
        width: auto !important;
        min-width: 200px !important;
    }
    
    div.stButton > button:hover {
        background: #1E293B !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 20px rgba(15,23,42,0.25) !important;
        color: #FFFFFF !important;
    }
    
    /* Clean Minimalist Nav Back Button Style Override */
    div.stButton > button[key^="back_btn_nav"] {
        background: transparent !important;
        color: #64748B !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: none !important;
        padding: 8px 16px !important;
        font-size: 13px !important;
        min-width: auto !important;
        width: auto !important;
        margin-bottom: 25px !important;
        text-transform: none !important;
    }
    div.stButton > button[key^="back_btn_nav"]:hover {
        background: #F1F5F9 !important;
        color: #0F172A !important;
    }
    
    /* Form input box field canvas styling updates */
    .stTextInput input {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        color: #0F172A !important;
        padding: 12px 14px !important;
        font-size: 15px !important;
    }
    .stTextInput input:focus {
        border-color: #0F172A !important;
        box-shadow: 0 0 0 1px #0F172A !important;
    }
    label {
        color: #475569 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    /* Tab Headers */
    .stTabs [data-baseweb="tab"] {
        color: #64748B !important;
        font-family: 'Inter', sans-serif !important;
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
    # PAGE 1: SPLASH WELCOME GATEWAY
    # ----------------------------------------------------
    if st.session_state["onboarding_step"] == "splash":
        
        _, master_grid, _ = st.columns([0.2, 3.6, 0.2])
        
        with master_grid:
            # Build outer split layout structure
            st.html("""
            <div class="master-designer-box">
                <div class="workspace-left-pane" id="splash-left-logo-hook"></div>
                <div class="workspace-right-pane" id="splash-right-text-hook">
                    <h1 class="splash-core-title">REQ 2 TASK AI</h1>
                    <p class="splash-core-tagline">SMART REQUIREMENTS. INTELLIGENT TASKS. BETTER RESULTS.</p>
                </div>
            </div>
            """)
            
            # Use fixed negative margin tracking to inject the logo into the left HTML frame cleanly
            st.markdown("<style>div[data-testid='stVerticalBlock'] > div:nth-child(3) { margin-top: -65vh; margin-left: 4%; width: 38%; }</style>", unsafe_allow_html=True)
            logo_filename = "logo.png"
            if os.path.exists(logo_filename):
                img = Image.open(logo_filename)
                st.image(img, use_container_width=True)
                
            # Place the GET STARTED button directly inside the right panel frame zone
            st.markdown("<style>div[data-testid='stVerticalBlock'] > div:nth-child(4) { margin-top: -32vh; margin-left: 50%; width: 40%; }</style>", unsafe_allow_html=True)
            if st.button("GET STARTED!", key="splash_onboarding_action_trigger"):
                st.session_state["onboarding_step"] = "portal"
                st.rerun()

    # ----------------------------------------------------
    # PAGE 2: ACCESS PORTAL INTERACTION FRAME
    # ----------------------------------------------------
    elif st.session_state["onboarding_step"] == "portal":
        
        _, master_grid, _ = st.columns([0.2, 3.6, 0.2])
        
        with master_grid:
            st.html("""
            <div class="master-designer-box">
                <div class="workspace-left-pane" id="portal-left-logo-hook"></div>
                <div class="workspace-right-pane" id="portal-right-form-hook">
                    <h1 class="portal-core-title">READY TO TRANSFORM?</h1>
                    <p class="portal-core-sub">Log into your workspace environment or deploy a fresh instance.</p>
                </div>
            </div>
            """)
            
            # Inject logo on the left pane cleanly
            st.markdown("<style>div[data-testid='stVerticalBlock'] > div:nth-child(3) { margin-top: -65vh; margin-left: 4%; width: 38%; }</style>", unsafe_allow_html=True)
            logo_filename = "logo.png"
            if os.path.exists(logo_filename):
                img = Image.open(logo_filename)
                st.image(img, use_container_width=True)
                
            # Overlay interactive registration/login cards onto the right panel frame zone
            st.markdown("<style>div[data-testid='stVerticalBlock'] > div:nth-child(4) { margin-top: -55vh; margin-left: 50%; width: 45%; }</style>", unsafe_allow_html=True)
            with st.container():
                
                # Native, perfectly positioned navigation back button
                if st.button("← Back", key="back_btn_nav"):
                    st.session_state["onboarding_step"] = "splash"
                    st.rerun()
                    
                tab1, tab2 = st.tabs(["Sign In", "Create Account"])
                
                with tab1:
                    st.markdown("<br>", unsafe_allow_html=True)
                    login_user = st.text_input("Username / Email", key="login_user").strip().lower()
                    
                    # NATIVE IN-FIELD VISIBILITY TOGGLE: Streamlit adds the eye completely inside the field box border frame border!
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
