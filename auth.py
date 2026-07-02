import hashlib
import os
import streamlit as st
from PIL import Image
from mongodb import db

users_collection = db["users"]


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ----------------------------------------------------
# WIDE LAYOUT SETUP
# ----------------------------------------------------
def _ensure_wide_layout():
    try:
        st.set_page_config(
            page_title="REQ 2 TASK AI",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
    except st.errors.StreamlitAPIException:
        pass


# ----------------------------------------------------
# HIGH-END LUXURY DARK THEME INJECTION
# ----------------------------------------------------
def _inject_global_styles():
    # Enforced as a Raw String using r""" to safely bypass Python 3.14 type checking
    st.html(r"""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
    /* Full screen canvas overhaul to deep cinematic dark theme */
    .stApp {
        background: #080C14 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Clear Streamlit background clutter */
    [data-testid="stHeader"],
    [data-testid="stSidebarHideRepoButton"],
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    .main .block-container {
        padding: 5vh 5vw !important;
        max-width: 100% !important;
    }

    /* ---------- LUXURY MASTER CONTAINER CONTAINER ---------- */
    .st-key-master_card {
        background: rgba(15, 22, 36, 0.7) !important;
        border: 1px solid rgba(212, 162, 76, 0.15) !important;
        border-radius: 32px !important;
        box-shadow: 0 30px 70px rgba(0, 0, 0, 0.8), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        overflow: hidden;
        padding: 0 !important;
        backdrop-filter: blur(20px);
    }
    
    .st-key-master_card [data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
        min-height: 75vh;
    }
    .st-key-master_card [data-testid="stHorizontalBlock"] > div {
        height: 100%;
    }

    /* LEFT DISPLAY PANE - LOGO & FEATURE GRID */
    /* Blends your white logo seamlessly without edge boxes */
    .st-key-left_pane {
        background: #FFFFFF !important; 
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height: 100%;
        min-height: 75vh;
        padding: 50px !important;
    }

    /* RIGHT DISPLAY PANE - INTERACTIVE CONTROL GATE */
    .st-key-right_pane {
        background: #0B111E !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        min-height: 75vh;
        padding: 60px !important;
        position: relative;
    }

    /* ---------- TEXT MODEL TYPOGRAPHY ---------- */
    .welcome-text {
        color: #D4A24C !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        letter-spacing: 4px !important;
        text-transform: uppercase !important;
        margin-bottom: 5px !important;
    }
    
    .main-logo-heading {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 56px !important;
        font-weight: 900 !important;
        letter-spacing: -2px !important;
        margin: 0 0 15px 0 !important;
        line-height: 1.1 !important;
    }
    
    .main-logo-heading span {
        background: linear-gradient(90deg, #D4A24C, #FFF3D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sub-tagline-desc {
        color: #8A98A8 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
        margin-bottom: 35px !important;
    }

    /* ---------- SEPARATOR BAR OR ---------- */
    .separator-container {
        text-align: center !important;
        margin: 25px 0 !important;
        position: relative !important;
    }
    .separator-container::before {
        content: "" !important;
        position: absolute !important;
        top: 50% !important;
        left: 0 !important;
        width: 100% !important;
        height: 1px !important;
        background: rgba(255, 255, 255, 0.08) !important;
        z-index: 1 !important;
    }
    .separator-text {
        background: #0B111E !important;
        color: #566475 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        padding: 0 15px !important;
        position: relative !important;
        z-index: 2 !important;
        text-transform: uppercase !important;
    }

    /* ---------- INPUT MATRIX STYLING ---------- */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        color: #FFFFFF !important;
        padding: 14px 16px !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus {
        border-color: #D4A24C !important;
        box-shadow: 0 0 0 1px #D4A24C !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    label {
        color: #8A98A8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 6px !important;
    }

    /* ---------- TAB STRIP STYLES ---------- */
    .stTabs [data-baseweb="tab"] {
        color: #566475 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        padding-bottom: 10px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #D4A24C !important;
        border-bottom-color: #D4A24C !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #D4A24C !important;
    }

    /* ---------- LUXURY GOLD ACTIONS BUTTON ---------- */
    div.stButton > button {
        background: linear-gradient(90deg, #E5B25D 0%, #C3923B 100%) !important;
        color: #080C14 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 16px 32px !important;
        box-shadow: 0 8px 24px rgba(195, 146, 59, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #FAD38D 0%, #DBAA4F 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(195, 146, 59, 0.4) !important;
        color: #080C14 !important;
    }

    /* ---------- SECONDARY HOVER HOLLOW BUTTON ---------- */
    .st-key-sec_action_btn div.stButton > button {
        background: transparent !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: none !important;
    }
    .st-key-sec_action_btn div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.04) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
    }

    /* ---------- CLEAN BACK BUTTON ---------- */
    .st-key-back_btn_row div.stButton > button {
        background: transparent !important;
        color: #566475 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: none !important;
        padding: 8px 16px !important;
        font-size: 13px !important;
        text-transform: none !important;
        min-width: auto !important;
        width: auto !important;
    }
    .st-key-back_btn_row div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #FFFFFF !important;
    }

    /* ---------- BOTTOM FOOTER HORIZONTAL TECH TAGS ---------- */
    .tech-footer-container {
        display: flex !important;
        width: 100% !important;
        justify-content: space-between !important;
        border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding-top: 25px !important;
        margin-top: 30px !important;
    }
    .tech-tag-node {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        color: #8A98A8 !important;
        font-size: 13px !important;
    }
    .tech-tag-node strong {
        color: #FFFFFF !important;
        display: block !important;
        font-size: 13px !important;
    }
    .tech-tag-node span {
        font-size: 11px !important;
        color: #566475 !important;
        display: block !important;
    }

    /* ---------- SECONDARY TEXT STYLES ---------- */
    .portal-core-title {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(26px, 2.6vw, 40px) !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        margin: 0 0 8px 0 !important;
        white-space: nowrap !important;
    }
    .portal-core-sub {
        color: #566475 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        margin: 0 0 30px 0 !important;
    }

    /* ---------- LEFT LOGO FEATURE CARDS ROW ---------- */
    .feature-icon-row {
        display: flex !important;
        width: 100% !important;
        justify-content: space-between !important;
        margin-top: 40px !important;
    }
    .feature-mini-card {
        text-align: center !important;
        flex: 1 !important;
    }
    .feature-mini-card strong {
        color: #FFFFFF !important;
        font-size: 11px !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        display: block !important;
        margin-top: 8px !important;
    }
    .feature-mini-card span {
        color: #566475 !important;
        font-size: 11px !important;
        display: block !important;
        margin-top: 2px !important;
    }

    /* ---------- MINI BADGE TRACE ---------- */
    .ai-badge {
        position: absolute !important;
        top: 30px !important;
        right: 30px !important;
        background: rgba(212, 162, 76, 0.08) !important;
        border: 1px solid rgba(212, 162, 76, 0.2) !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        color: #D4A24C !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
    }

    /* ====================================================
       RESPONSIVE MATRIX ADJUSTMENTS FOR MOBILE VIEWPORTS
       ==================================================== */
    @media (max-width: 992px) {
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        .st-key-left_pane {
            border-right: none !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            padding: 40px 20px !important;
            min-height: auto !important;
        }
        .st-key-left_pane img, [data-testid="stImage"] img {
            max-width: 50% !important;
            margin: 0 auto !important;
        }
        .feature-icon-row {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 20px !important;
        }
        .st-key-right_pane {
            padding: 40px 20px !important;
            min-height: auto !important;
        }
        .main-logo-heading {
            font-size: 38px !important;
            text-align: center !important;
        }
        .sub-tagline-desc {
            text-align: center !important;
            font-size: 14px !important;
        }
        .tech-footer-container {
            flex-direction: column !important;
            gap: 15px !important;
        }
        .ai-badge {
            position: relative !important;
            top: 0 !important;
            right: 0 !important;
            margin: 0 auto 20px auto !important;
            width: fit-content !important;
        }
    }
    </style>
    """)


# ----------------------------------------------------
# LEFT CANVAS DECORATIONS RENDERER
# ----------------------------------------------------
def _render_logo():
    logo_filename = "logo.png"
    if os.path.exists(logo_filename):
        img = Image.open(logo_filename)
        st.image(img, use_container_width=True)
    else:
        st.markdown(
            "<div style='color:#566475; font-family:Inter, sans-serif; "
            "font-size:14px; text-align:center; padding: 60px 0;'>[ Integrated Identity Vector Panel ]</div>",
            unsafe_allow_html=True,
        )

    # Injects the lower 4 horizontal core feature badges directly underneath the logo icon 
    st.markdown("""
    <div class="feature-icon-row">
        <div class="feature-mini-card">
            <div style="font-size:20px;">📄</div>
            <strong>Analyze</strong>
            <span>Requirements</span>
        </div>
        <div class="feature-mini-card">
            <div style="font-size:20px;">🧠</div>
            <strong>Generate</strong>
            <span>Smart Tasks</span>
        </div>
        <div class="feature-mini-card">
            <div style="font-size:20px;">👥</div>
            <strong>Collaborate</strong>
            <span>With Teams</span>
        </div>
        <div class="feature-mini-card">
            <div style="font-size:20px;">📈</div>
            <strong>Deliver</strong>
            <span>Better Results</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ----------------------------------------------------
# RIGHT PORTAL RENDER LOGIC
# ----------------------------------------------------
def _render_splash_pane():
    st.markdown('<div class="ai-badge">✦ AI-POWERED</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="welcome-text">Welcome To</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-logo-heading">REQ 2 TASK <span>AI</span></h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-tagline-desc">Transform requirements into actionable tasks with the power of AI.</p>',
        unsafe_allow_html=True,
    )
    
    if st.button("🚀 Get Started", key="splash_onboarding_action_trigger"):
        st.session_state["onboarding_step"] = "portal"
        st.rerun()
        
    st.markdown('<div class="separator-container"><span class="separator-text">or</span></div>', unsafe_allow_html=True)
    
    with st.container(key="sec_action_btn"):
        if st.button("👤 Sign In To Account", key="splash_direct_login_trigger"):
            st.session_state["onboarding_step"] = "portal"
            st.rerun()

    # Injects the bottom tech indicator tags 
    st.markdown("""
    <div class="tech-footer-container">
        <div class="tech-tag-node">
            <div style="font-size:16px; color:#E5B25D;">🛡️</div>
            <div><strong>Secure</strong><span>Your Data is Safe</span></div>
        </div>
        <div class="tech-tag-node">
            <div style="font-size:16px; color:#E5B25D;">⚡</div>
            <div><strong>Intelligent</strong><span>AI-Powered Engine</span></div>
        </div>
        <div class="tech-tag-node">
            <div style="font-size:16px; color:#E5B25D;">👥</div>
            <div><strong>Collaborative</strong><span>Built for Teams</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_portal_pane():
    with st.container(key="back_btn_row"):
        if st.button("← Back to Welcome Screen", key="back_btn_nav"):
            st.session_state["onboarding_step"] = "splash"
            st.rerun()

    st.markdown('<h1 class="portal-core-title">READY TO TRANSFORM?</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="portal-core-sub">Log into your workspace environment or deploy a fresh instance.</p>',
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["Sign In", "Create Account"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        login_user = st.text_input("Username / Email", key="login_user").strip().lower()
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
                        "password": hash_password(reg_pass),
                    })
                    st.success("Workspace created! Please Sign In.")
            else:
                st.warning("Please fill in all fields.")


# ----------------------------------------------------
# ARCHITECTURAL ACCESS CORE
# ----------------------------------------------------
def render_login_signup():
    _ensure_wide_layout()

    if "onboarding_step" not in st.session_state:
        st.session_state["onboarding_step"] = "splash"

    _inject_global_styles()

    # Perfect page alignment framing the card layout
    _, master_grid, _ = st.columns([0.2, 3.6, 0.2])

    with master_grid:
        with st.container(key="master_card"):
            left_col, right_col = st.columns([1.1, 1.3])

            with left_col:
                with st.container(key="left_pane"):
                    _render_logo()

            with right_col:
                with st.container(key="right_pane"):
                    if st.session_state["onboarding_step"] == "splash":
                        _render_splash_pane()
                    else:
                        _render_portal_pane()
