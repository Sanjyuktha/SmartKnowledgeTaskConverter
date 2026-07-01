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
    # PREMIUM CANVAS STYLING
    # ----------------------------------------------------
    st.html("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
    /* Reset and Canvas Control */
    .stApp {
        background: #060C16 !important;
    }
    
    /* Hide default Streamlit block spacing headers */
    [data-testid="stHeader"], [data-testid="stSidebarHideRepoButton"] {
        display: none !important;
    }
    
    /* Layout Wrapper to mimic the designer templates */
    .split-layout {
        display: flex;
        flex-direction: row;
        width: 90%;
        max-width: 1200px;
        margin: 5vh auto;
        min-height: 80vh;
        background: #0A1324;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 28px;
        overflow: hidden;
        box-shadow: 0 30px 70px rgba(0,0,0,0.5);
    }
    
    /* Left panel for branding */
    .panel-left {
        flex: 1;
        background: linear-gradient(145deg, #0E1C33 0%, #060C16 100%);
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .panel-left img {
        max-width: 80%;
        height: auto;
        border-radius: 20px;
    }
    
    /* Right panel for text controls */
    .panel-right {
        flex: 1.2;
        padding: 60px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: #0A1324;
    }
    
    /* Clean Custom Typography */
    .app-main-title {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 56px !important;
        font-weight: 900 !important;
        letter-spacing: -2px !important;
        margin: 0 0 10px 0 !important;
        line-height: 1.1 !important;
    }
    
    .app-italic-tagline {
        color: #D4A24C !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        font-style: italic !important;
        letter-spacing: 1.5px !important;
        margin: 0 0 40px 0 !important;
        line-height: 1.4 !important;
    }
    
    .app-transform-title {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 44px !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        margin: 0 0 10px 0 !important;
    }
    
    .app-transform-sub {
        color: #718096 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        margin: 0 0 30px 0 !important;
    }
    
    /* Premium Solid UI Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #D4A24C 0%, #F0C46C 100%) !important;
        color: #060C16 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 14px 24px !important;
        box-shadow: 0 8px 20px rgba(212,162,76,0.2) !important;
        transition: all 0.2s ease !important;
        width: auto !important;
        min-width: 180px !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 12px 28px rgba(212,162,76,0.35) !important;
    }
    
    /* Input element overrides for modern look */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        padding: 12px 14px !important;
    }
    
    .stTextInput input:focus {
        border-color: #D4A24C !important;
        box-shadow: 0 0 0 1px #D4A24C !important;
    }
    
    label {
        color: #A0AEC0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab"] {
        color: #4A5568 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #D4A24C !important;
    }
    
    /* Responsive adjustment for small monitors */
    @media (max-width: 768px) {
        .split-layout { display: flex; flex-direction: column; }
        .panel-left { min-height: 30vh; }
    }
    </style>
    """)

    logo_path = "logo.png"

    # ----------------------------------------------------
    # PAGE 1: SPLASH SCREEN (DESIGNER SPLIT WINDOW)
    # ----------------------------------------------------
    if st.session_state["onboarding_step"] == "splash":
        
        # Build layout grid via clean container blocks
        container_html = f"""
        <div class="split-layout">
            <div class="panel-left">
                <img src="data:image/png;base64," style="display:none;" onerror="
                    this.onerror=null;
                    var el=this.parentElement;
                    el.innerHTML='';
                    var img=document.createElement('img');
                    img.src='https://raw.githubusercontent.com/{st.router.get_repo_owner() if hasattr(st, 'router') else 'Sanjyuktha'}/SmartKnowledgeTaskConverter/main/edited-image.png';
                    el.appendChild(img);
                " />
            </div>
            <div class="panel-right" id="splash-right-injection">
                <h1 class="app-main-title">REQ 2 TASK AI</h1>
                <p class="app-italic-tagline">SMART REQUIREMENTS. INTELLIGENT TASKS. BETTER RESULTS.</p>
            </div>
        </div>
        """
        st.html(container_html)
        
        # Insert the functional start button right where the layout expects it
        with st.container():
            # Adjust padding alignment container to visually attach button into right pane
            st.markdown("<style>div[data-testid='stVerticalBlock'] > div:nth-child(3) { margin-top: -33vh; margin-left: calc(45% + 60px); }</style>", unsafe_allow_html=True)
            if st.button("GET STARTED!", key="splash_get_started_btn"):
                st.session_state["onboarding_step"] = "portal"
                st.rerun()

    # ----------------------------------------------------
    # PAGE 2: PORTAL FORM ENTRY (WITH NATIVE INTEGRATED EYE)
    # ----------------------------------------------------
    elif st.session_state["onboarding_step"] == "portal":
        
        portal_html = """
        <div class="split-layout">
            <div class="panel-left"></div>
            <div class="panel-right" id="portal-right-injection">
                <h1 class="app-transform-title">READY TO TRANSFORM?</h1>
                <p class="app-transform-sub">Log into your workspace environment or deploy a fresh instance.</p>
            </div>
        </div>
        """
        st.html(portal_html)
        
        # Overlays structural workspace tab forms into the right-hand panel grid perfectly
        st.markdown("<style>div[data-testid='stVerticalBlock'] > div:nth-child(3) { margin-top: -55vh; margin-left: calc(45% + 60px); width: 45%; }</style>", unsafe_allow_html=True)
        
        with st.container():
            tab1, tab2 = st.tabs(["Sign In", "Create Account"])
            
            with tab1:
                st.markdown("<br>", unsafe_allow_html=True)
                login_user = st.text_input("Username / Email", key="login_user").strip().lower()
                
                # NATIVE EYE CONFIGURATION: Streamlit builds the eye button completely inside the input field!
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
