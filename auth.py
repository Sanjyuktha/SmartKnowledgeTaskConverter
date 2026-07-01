import hashlib
import os
import streamlit as st
from PIL import Image
from mongodb import db

users_collection = db["users"]


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ----------------------------------------------------
# WIDE LAYOUT (fixes the narrow/"vertical" card)
# ----------------------------------------------------
def _ensure_wide_layout():
    # Streamlit's default "centered" layout caps page width at ~730px,
    # which is why the split card was rendering narrow and the heading
    # was wrapping onto 3 lines. Wide mode lets it use the full screen.
    # Must be the first st.* call in the whole app, and can only run once,
    # so we swallow the error if it was already set elsewhere (e.g. your
    # main entry file).
    try:
        st.set_page_config(
            page_title="REQ 2 TASK AI",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
    except st.errors.StreamlitAPIException:
        pass


# ----------------------------------------------------
# GLOBAL STYLES
# ----------------------------------------------------
def _inject_global_styles():
    st.html("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
    /* Clean light gradient canvas */
    .stApp {
        background: linear-gradient(135deg, #EEF2F6 0%, #F8FAFC 100%) !important;
    }

    /* Hide default Streamlit chrome */
    [data-testid="stHeader"],
    [data-testid="stSidebarHideRepoButton"],
    [data-testid="stDecoration"] {
        display: none !important;
    }
    .main .block-container {
        padding-top: 4vh !important;
        padding-bottom: 4vh !important;
        max-width: 100% !important;
    }

    /* ---------- MASTER CARD (a real st.container, not injected HTML) ---------- */
    .st-key-master_card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 24px !important;
        box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.08) !important;
        overflow: hidden;
        padding: 0 !important;
    }
    /* Make the row of columns inside the card stretch full height */
    .st-key-master_card [data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
        min-height: 65vh;
    }
    .st-key-master_card [data-testid="stHorizontalBlock"] > div {
        height: 100%;
    }

    /* Left pane: logo */
    .st-key-left_pane {
        background: #F8FAFC !important;
        border-right: 1px solid #E2E8F0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100%;
        min-height: 65vh;
        padding: 40px !important;
    }

    /* Right pane: titles / forms */
    .st-key-right_pane {
        background: #FFFFFF !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        min-height: 65vh;
        padding: 60px !important;
    }

    /* ---------- Typography ---------- */
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
        font-size: clamp(26px, 2.6vw, 40px) !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        margin: 0 0 8px 0 !important;
        white-space: nowrap !important;
    }
    .portal-core-sub {
        color: #64748B !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        margin: 0 0 30px 0 !important;
    }

    /* ---------- Primary buttons ---------- */
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

    /* ---------- Minimalist back button (scoped to its own container) ---------- */
    .st-key-back_btn_row {
        display: flex !important;
        justify-content: flex-end !important;
        margin-bottom: 20px !important;
    }
    .st-key-back_btn_row div.stButton > button {
        background: transparent !important;
        color: #64748B !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: none !important;
        padding: 8px 16px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        min-width: auto !important;
        width: auto !important;
        text-transform: none !important;
    }
    .st-key-back_btn_row div.stButton > button:hover {
        background: #F1F5F9 !important;
        color: #0F172A !important;
    }

    /* ---------- Inputs (native password eye stays in the box, untouched) ---------- */
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

    /* ---------- Tabs ---------- */
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
# HELPERS
# ----------------------------------------------------
def _render_logo():
    logo_filename = "logo.png"
    if os.path.exists(logo_filename):
        img = Image.open(logo_filename)
        st.image(img, use_container_width=True)
    else:
        st.markdown(
            "<div style='color:#94A3B8; font-family:Inter, sans-serif; "
            "font-size:14px; text-align:center;'>Logo image not found</div>",
            unsafe_allow_html=True,
        )


def _render_splash_pane():
    st.markdown('<h1 class="splash-core-title">REQ 2 TASK AI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="splash-core-tagline">SMART REQUIREMENTS. INTELLIGENT TASKS. BETTER RESULTS.</p>',
        unsafe_allow_html=True,
    )
    if st.button("GET STARTED!", key="splash_onboarding_action_trigger"):
        st.session_state["onboarding_step"] = "portal"
        st.rerun()


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
# MAIN ENTRY POINT
# ----------------------------------------------------
def render_login_signup():
    _ensure_wide_layout()

    if "onboarding_step" not in st.session_state:
        st.session_state["onboarding_step"] = "splash"

    _inject_global_styles()

    _, master_grid, _ = st.columns([0.5, 3, 0.5])

    with master_grid:
        # This container itself IS the white card -- no HTML overlay, no margin hacks.
        with st.container(key="master_card"):
            left_col, right_col = st.columns([1, 1.2])

            with left_col:
                with st.container(key="left_pane"):
                    _render_logo()

            with right_col:
                with st.container(key="right_pane"):
                    if st.session_state["onboarding_step"] == "splash":
                        _render_splash_pane()
                    else:
                        _render_portal_pane()
