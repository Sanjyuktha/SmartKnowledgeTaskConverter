import streamlit as st
import pandas as pd
from io import BytesIO
from pypdf import PdfReader
from db import tasks_collection
import matplotlib.pyplot as plt
from mongodb import collection
import plotly.express as px
from auth import render_login_signup

# Initialize authentication states
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Force login if user is unauthenticated
if not st.session_state["authenticated"]:
    render_login_signup()
    st.stop() # Stops execution here so they can't see the dashboard yet!


# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Smart Knowledge Intelligence",
     layout="wide"
)

# ---------------------------------
# CSS
# ---------------------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

.stApp{
    background:#F4F6F8;
}

[data-testid="stSidebar"]{
    background:linear-gradient(
        180deg,
        #081120 0%,
        #0F1E35 100%
    );
}


[data-testid="stSidebar"] *{
    color:white;
}

.main-title{
    color:#2C3539;
}

.sub-title{
    color:#3F4E4F;
}

.hero{
    background:#3F4E4F;
    color:white;
    padding:35px;
    border-radius:24px;
}
/* ==================================================== */
/* PERFECT SIDEBAR TOGGLE TO HAMBURGER MENU CONVERSION  */
/* ==================================================== */

/* 1. Target the button when the sidebar is OPEN */
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* 2. Target the button when the sidebar is CLOSED */
div[data-testid="collapsedControl"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Hide the default double-arrow SVG icon completely in BOTH states */
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button svg,
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button svg path,
div[data-testid="collapsedControl"] button svg,
div[data-testid="collapsedControl"] button svg path {
    display: none !important;
    opacity: 0 !important;
}

/* Inject the standard 3-line hamburger icon instead */
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button::before,
div[data-testid="collapsedControl"] button::before {
    content: "☰" !important;
    font-size: 24px !important;
    font-weight: bold !important;
    display: inline-block !important;
    font-family: 'Inter', sans-serif !important;
    transition: transform 0.2s ease-in-out, color 0.2s ease-in-out !important;
    line-height: 1 !important;
}

/* Color rule for when sidebar is OPEN (White text on dark background) */
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button::before {
    color: #FFFFFF !important;
}

/* Color rule for when sidebar is CLOSED (Dark blue text on light canvas background) */
div[data-testid="collapsedControl"] button::before {
    color: #0B1F3A !important;
    margin-left: 10px; /* Gives nice breathing space from screen edge when closed */
}

/* Premium gold hover reaction on mouse-over */
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover::before,
div[data-testid="collapsedControl"] button:hover::before {
    transform: scale(1.1);
    color: #D4A24C !important; 
}

/* ==================================================== */

/* ========================= */
/* ADD THE NEW CODE HERE */
/* ========================= */
/* Space between radio buttons */
.stRadio > div {
    gap: 10px;
}

/* Style only the radio options */
.stRadio [role="radiogroup"] label {
    background: rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 8px 12px;
    margin-bottom: 8px;
}

/* Hover */
.stRadio [role="radiogroup"] label:hover {
    background: #D4A24C;
    color: white !important;
}

/* Selected */
.stRadio input:checked + div {
    color: #A27B5B !important;
    font-weight: bold;
}





/* ========================= */

</style>
""", unsafe_allow_html=True)
# ---------------------------------
# SIDEBAR
# ---------------------------------
st.sidebar.markdown("""
<div style="
padding-top:10px;
padding-bottom:20px;
">
<h1 style="
color:white;
font-size:32px;
font-weight:700;
margin-bottom:0;
">
SmartKI
</h1>

<p style="
color:#A0AEC0;
font-size:14px;
margin-top:0;
">
Knowledge Intelligence
</p>
</div>
""", unsafe_allow_html=True)

# ==========================
# WORKSPACE HEADING
# ==========================

st.sidebar.markdown("""
<div style="
background:linear-gradient(90deg,#D4A24C,#F0C46C);
padding:12px;
border-radius:30px;
text-align:center;
font-size:15px;
font-weight:700;
letter-spacing:2px;
color:#081120;
box-shadow:0 8px 18px rgba(0,0,0,.25);
margin-bottom:20px;
">
WORKSPACE
</div>
""", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Team Members",
        "Upload Document",
        "Generated Tasks",
        "Analytics",
        "Saved Projects"
    ]
)
# ----------------------------------------------------
# FIXED UNIFIED LOGOUT SYSTEM (BULLETPROOF BYPASS)
# ----------------------------------------------------
st.sidebar.markdown("---")

# Use st.sidebar.html to create a completely custom, un-overridable button
st.sidebar.html("""
<form method="get" action="">
    <button type="submit" name="custom_logout_trigger" value="true" class="sidebar-master-logout-btn">
        Log Out
    </button>
</form>

<style>
.sidebar-master-logout-btn {
    background-color: #1E293B !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    width: 100% !important;
    display: block !important;
    cursor: pointer !important;
    text-align: center !important;
    transition: all 0.2s ease-in-out !important;
}

.sidebar-master-logout-btn:hover {
    background-color: #EF4444 !important;
    color: #FFFFFF !important;
    border-color: #EF4444 !important;
}
</style>
""")

# Catch the HTML form submission click event seamlessly
if st.query_params.get("custom_logout_trigger") == "true":
    # Clear the query param instantly so it doesn't loop logouts
    st.query_params.clear()
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.rerun()

# ---------------------------------
# HEADER
# ---------------------------------
# ----------------------------
# HEADER
# ----------------------------

st.markdown("""
<div style="padding-bottom:20px;">

<h1 style="
font-size:52px;
font-weight:900;
color:#0B1F3A;
margin-bottom:5px;
">
Req2Task AI
</h1>

<p style="
font-size:20px;
font-weight:600;
color:#D4A24C;
margin-top:0px;
">
AI-Powered Requirement Intelligence Platform
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------
# HERO SECTION
# ---------------------------------
if page == "Dashboard":
    # ----------------------------------------------------
    # SESSION STATE INITIALIZATION
    # ----------------------------------------------------
    if "dashboard_card" not in st.session_state:
        st.session_state.dashboard_card = "overview"

    try:
        projects = list(collection.find({"username": st.session_state["username"]}))
        
        if "card_view" not in st.session_state:
            st.session_state["card_view"] = None

        total_tasks = 0
        completed_tasks = 0
        high_tasks = 0

        for project in projects:
            tasks = project.get("tasks", [])
            total_tasks += len(tasks)
            completed_tasks += len([t for t in tasks if t.get("status", False)])
            high_tasks += len([t for t in tasks if t.get("priority") == "High"])

    except Exception:
        projects = []
        total_tasks = 0
        completed_tasks = 0
        high_tasks = 0

    project_count = collection.count_documents({"username": st.session_state["username"]})

    # ----------------------------------------------------
    # ADVANCED CONTAINER OVERLAY CSS (Eliminates Code Strings & Empty Boxes)
    # ----------------------------------------------------
    st.markdown("""
    <style>
    /* Make each column an isolation context for precise overlay tracking */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] {
        position: relative !important;
        display: flex !important;
        flex-direction: column !important;
    }

    /* Transform the empty native buttons into fully transparent overlay sheets */
    div[data-testid="stVerticalBlock"] div[data-testid="stButton"] button {
        position: absolute !important;
        top: -185px !important; /* Move up to precisely match the height of the card above it */
        left: 0 !important;
        width: 100% !important;
        height: 185px !important;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        box-shadow: none !important;
        z-index: 100 !important;
        cursor: pointer !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Prevent Streamlit layout shifting or hover/focus artifacts on invisible overlays */
    div[data-testid="stVerticalBlock"] div[data-testid="stButton"] button:hover,
    div[data-testid="stVerticalBlock"] div[data-testid="stButton"] button:focus,
    div[data-testid="stVerticalBlock"] div[data-testid="stButton"] button:active {
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        box-shadow: none !important;
    }

    /* Force the empty button block wrapper to occupy zero layout space beneath the card */
    div[data-testid="stVerticalBlock"] div[data-testid="stButton"] {
        height: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # 4 PREMIUM INTERACTIVE CARDS (ROBUST HTML + OVERLAY)
    # ----------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        is_active = st.session_state.dashboard_card == "tasks"
        border_style = "border: 3px solid #D4A24C; box-shadow: 0 12px 40px rgba(212,162,76,0.25);" if is_active else "border-top: 5px solid #D4A24C; box-shadow: 0 10px 35px rgba(0,0,0,0.08);"
        
        st.markdown(f"""
        <div style="background:white; border-radius:28px; padding:28px; height:185px; {border_style} transition: all 0.3s ease;">
            <p style="color:#6B7280; font-size:13px; font-weight:600; letter-spacing:1px; text-transform:uppercase; margin:0;">TOTAL TASKS</p>
            <h1 style="margin-top:14px; margin-bottom:0; font-size:44px; color:#22C55E; font-weight:700; line-height:1;">{total_tasks}</h1>
            <p style="color:#9CA3AF; font-size:14px; margin-top:8px; margin-bottom:0;">AI Generated Tasks</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("", key="action_trigger_tasks", use_container_width=True):
            st.session_state.dashboard_card = "overview" if is_active else "tasks"
            st.rerun()

    with c2:
        is_active = st.session_state.dashboard_card == "completed"
        border_style = "border: 3px solid #D4A24C; box-shadow: 0 12px 40px rgba(212,162,76,0.25);" if is_active else "border-top: 5px solid #D4A24C; box-shadow: 0 10px 35px rgba(0,0,0,0.08);"
        
        st.markdown(f"""
        <div style="background:white; border-radius:28px; padding:28px; height:185px; {border_style} transition: all 0.3s ease;">
            <p style="color:#6B7280; font-size:13px; font-weight:600; letter-spacing:1px; text-transform:uppercase; margin:0;">COMPLETED</p>
            <h1 style="margin-top:14px; margin-bottom:0; font-size:44px; color:#16A34A; font-weight:700; line-height:1;">{completed_tasks}</h1>
            <p style="color:#9CA3AF; font-size:14px; margin-top:8px; margin-bottom:0;">Successfully Finished</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("", key="action_trigger_completed", use_container_width=True):
            st.session_state.dashboard_card = "overview" if is_active else "completed"
            st.rerun()

    with c3:
        is_active = st.session_state.dashboard_card == "priority"
        border_style = "border: 3px solid #D4A24C; box-shadow: 0 12px 40px rgba(212,162,76,0.25);" if is_active else "border-top: 5px solid #D4A24C; box-shadow: 0 10px 35px rgba(0,0,0,0.08);"
        
        st.markdown(f"""
        <div style="background:white; border-radius:28px; padding:28px; height:185px; {border_style} transition: all 0.3s ease;">
            <p style="color:#6B7280; font-size:13px; font-weight:600; letter-spacing:1px; text-transform:uppercase; margin:0;">HIGH PRIORITY</p>
            <h1 style="margin-top:14px; margin-bottom:0; font-size:44px; color:#F59E0B; font-weight:700; line-height:1;">{high_tasks}</h1>
            <p style="color:#9CA3AF; font-size:14px; margin-top:8px; margin-bottom:0;">Needs Attention</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("", key="action_trigger_priority", use_container_width=True):
            st.session_state.dashboard_card = "overview" if is_active else "priority"
            st.rerun()

    with c4:
        is_active = st.session_state.dashboard_card == "projects"
        border_style = "border: 3px solid #D4A24C; box-shadow: 0 12px 40px rgba(212,162,76,0.25);" if is_active else "border-top: 5px solid #D4A24C; box-shadow: 0 10px 35px rgba(0,0,0,0.08);"
        
        st.markdown(f"""
        <div style="background:white; border-radius:28px; padding:28px; height:185px; {border_style} transition: all 0.3s ease;">
            <p style="color:#6B7280; font-size:13px; font-weight:600; letter-spacing:1px; text-transform:uppercase; margin:0;">PROJECTS</p>
            <h1 style="margin-top:14px; margin-bottom:0; font-size:44px; color:#3B82F6; font-weight:700; line-height:1;">{project_count}</h1>
            <p style="color:#9CA3AF; font-size:14px; margin-top:8px; margin-bottom:0;">Stored in MongoDB</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("", key="action_trigger_projects", use_container_width=True):
            st.session_state.dashboard_card = "overview" if is_active else "projects"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # DYNAMIC DASHBOARD WORKSPACE (2.2 : 1 SPLIT)
    # ----------------------------------------------------
    left, right = st.columns([2.2, 1])

    with left:
        # 1. DEFAULT OVERVIEW PANEL
        if st.session_state.dashboard_card == "overview":
            st.markdown("""<div style="background:white; border-radius:30px; padding:35px; box-shadow:0 10px 35px rgba(0,0,0,0.08); min-height:420px;"><h2 style="color:#0B1F3A; margin-bottom:10px;">Project Overview</h2><hr style="border:1px solid #ECECEC;"><h3 style="color:#D4A24C; margin-top:25px;">AI Document Intelligence</h3><p style="color:#6B7280; font-size:16px; line-height:1.8;">Req2Task AI transforms requirement documents into structured, actionable development tasks using artificial intelligence.</p><br><table style="width:100%; font-size:16px; color:#6B7280;"><tr><td style="padding:10px;">✔ Requirement Analysis</td><td>✔ Smart Task Generation</td></tr><tr><td style="padding:10px;">✔ Priority Detection</td><td>✔ Progress Tracking</td></tr><tr><td style="padding:10px;">✔ MongoDB Storage</td><td>✔ AI Powered Workflow</td></tr></table><br><div style="background:#FFF8EC; border-left:5px solid #D4A24C; border-radius:15px; padding:18px; color:#6B7280;">System ready to analyse uploaded requirement documents.</div></div>""", unsafe_allow_html=True)

        # 2. TOTAL TASKS DYNAMIC PANEL
        elif st.session_state.dashboard_card == "tasks":
            inner_html = ""
            for project in projects:
                name = project.get("document_name", "Untitled Project")
                count = len(project.get("tasks", []))
                inner_html += f"""<div style="display:flex; justify-content:space-between; border-bottom:1px dashed #E2E8F0; padding:12px 0;"><span style="font-weight:500; color:#0B1F3A;">{name}</span><span style="font-weight:bold; color:#D4A24C;">{count} Tasks</span></div>"""
            
            st.markdown(f"""<div style="background:white; border-radius:30px; padding:35px; border:2px solid #D4A24C; box-shadow:0 10px 35px rgba(0,0,0,0.08); min-height:420px;"><h2 style="color:#0B1F3A; margin-bottom:10px;">📋 Total Tasks Overview</h2><hr style="border:1px solid #ECECEC; margin-bottom:20px;"><div style="font-family: inherit; font-size:16px; background:#F8FAFC; padding:25px; border-radius:20px; line-height:1.8;">{inner_html}</div></div>""", unsafe_allow_html=True)

        # 3. COMPLETED TASKS DYNAMIC PANEL
        elif st.session_state.dashboard_card == "completed":
            inner_html = ""
            has_completed = False
            for project in projects:
                tasks = project.get("tasks", [])
                completed_list = [t for t in tasks if t.get("status", False)]
                if completed_list:
                    has_completed = True
                    inner_html += f"""<h4 style="color:#0B1F3A; margin-top:25px; margin-bottom:12px; border-left:4px solid #16A34A; padding-left:10px; font-weight:600;">{project.get("document_name", "Untitled Project")}</h4>"""
                    for t in completed_list:
                        inner_html += f"""<div style="color:#4B5563; font-size:15px; margin-bottom:8px; padding-left:15px;">✔ {t.get("task", "Unnamed Task")} Completed</div>"""
            
            if not has_completed:
                inner_html = "<p style='color:#6B7280; font-size:15px;'>No completed tasks available across projects.</p>"

            st.markdown(f"""<div style="background:white; border-radius:30px; padding:35px; border:2px solid #16A34A; box-shadow:0 10px 35px rgba(0,0,0,0.08); min-height:420px;"><h2 style="color:#0B1F3A; margin-bottom:10px;">✅ Completed Tasks Overview</h2><hr style="border:1px solid #ECECEC; margin-bottom:15px;"><div style="padding-top:5px;">{inner_html}</div></div>""", unsafe_allow_html=True)

        # 4. HIGH PRIORITY DYNAMIC PANEL
        elif st.session_state.dashboard_card == "priority":
            inner_html = ""
            has_priority = False
            for project in projects:
                tasks = project.get("tasks", [])
                priority_list = [t for t in tasks if t.get("priority") == "High"]
                if priority_list:
                    has_priority = True
                    inner_html += f"""<h4 style="color:#0B1F3A; margin-top:25px; margin-bottom:12px; border-left:4px solid #F59E0B; padding-left:10px; font-weight:600;">{project.get("document_name", "Untitled Project")}</h4>"""
                    for t in priority_list:
                        inner_html += f"""<div style="color:#4B5563; font-size:15px; margin-bottom:8px; padding-left:15px;">{t.get("task", "Unnamed Task")}</div>"""
            
            if not has_priority:
                inner_html = "<p style='color:#6B7280; font-size:15px;'>No high priority tasks available currently.</p>"

            st.markdown(f"""<div style="background:white; border-radius:30px; padding:35px; border:2px solid #F59E0B; box-shadow:0 10px 35px rgba(0,0,0,0.08); min-height:420px;"><h2 style="color:#0B1F3A; margin-bottom:10px;">🔥 High Priority Tasks</h2><hr style="border:1px solid #ECECEC; margin-bottom:15px;"><div style="padding-top:5px;">{inner_html}</div></div>""", unsafe_allow_html=True)

        # 5. PROJECTS LIST DYNAMIC PANEL
        elif st.session_state.dashboard_card == "projects":
            inner_html = ""
            if not projects:
                inner_html = "<p style='color:#6B7280; font-size:15px;'>No saved records in database module.</p>"
            else:
                for project in projects:
                    tasks = project.get("tasks", [])
                    total = len(tasks)
                    completed = len([t for t in tasks if t.get("status", False)])
                    progress = 0 if total == 0 else int((completed / total) * 100)
                    
                    bar_filled = "█" * (progress // 10)
                    bar_empty = "░" * (10 - len(bar_filled))
                    
                    inner_html += f"""
                    <div style="margin-bottom:25px; padding-bottom:15px; border-bottom:1px dashed #E2E8F0;">
                        <h4 style="color:#0B1F3A; margin-bottom:5px; font-weight:600;">{project.get("document_name", "Untitled Project")}</h4>
                        <p style="color:#6B7280; font-size:14px; margin:0 0 5px 0;">{total} Tasks</p>
                        <p style="font-family:monospace; color:#D4A24C; font-size:16px; margin:0; letter-spacing:1px;">{bar_filled}{bar_empty} <span style="font-weight:bold;">{progress}%</span></p>
                    </div>"""

            st.markdown(f"""<div style="background:white; border-radius:30px; padding:35px; border:2px solid #3B82F6; box-shadow:0 10px 35px rgba(0,0,0,0.08); min-height:420px;"><h2 style="color:#0B1F3A; margin-bottom:10px;">📁 Projects Matrix Overview</h2><hr style="border:1px solid #ECECEC; margin-bottom:20px;"><div style="padding-top:5px;">{inner_html}</div></div>""", unsafe_allow_html=True)

    with right:
        # SYSTEM STATUS (ALWAYS VISIBLE)
        st.markdown(f"""<div style="background:white; border-radius:30px; padding:30px; box-shadow:0 10px 35px rgba(0,0,0,0.08); min-height:420px;"><h2 style="color:#0B1F3A;">System Status</h2><hr style="border:1px solid #ECECEC;"><h3 style="color:#10B981;">● Online</h3><br><p><b>MongoDB</b> : Connected</p><p><b>AI Engine</b> : Active</p><p><b>Dashboard</b> : Ready</p><p><b>Projects</b> : {project_count}</p><p><b>Total Tasks</b> : {total_tasks}</p><p><b>Completed</b> : {completed_tasks}</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # RECENT PROJECTS FOOTER SECTION (ALWAYS VISIBLE)
    st.markdown("""<h2 style="color:#0B1F3A; margin-bottom:20px;">Recent Projects</h2>""", unsafe_allow_html=True)

    # Force cast the cursor into a proper Python list to safely read its length and slice it
    safe_projects = list(projects)

    if len(safe_projects) == 0:
        st.info("No projects available.")
    else:
        # Grabs up to the last 5 projects safely and reverses them for recent view
        recent_items = safe_projects[-5:]
        recent_items.reverse()

        for project in recent_items:
            tasks = project.get("tasks", [])
            total = len(tasks)
            completed = len([t for t in tasks if t.get("status", False)])
            progress = 0 if total == 0 else int((completed / total) * 100)

            # --- YOUR CUSTOM DESIGN HTML CARD RNDERING STARTS HERE ---
            st.markdown(f"""
                <div style="background:white; border-radius:25px; padding:25px; margin-bottom:18px; box-shadow:0 8px 30px rgba(0,0,0,0.07);">
                    <h4 style="margin:0 0 10px 0; color:#0B1F3A;">📁 {project.get('document_name', 'Untitled Project')}</h4>
                    <p style="margin:0; color:#64748B; font-size:14px;">
                        Progress: <strong>{progress}%</strong> ({completed}/{total} Tasks Completed)
                    </p>
                </div>
            """, unsafe_allow_html=True)
# ==========================================
# UPLOAD PAGE
# ==========================================
elif page == "Upload Document":

    st.subheader("Upload Knowledge Document")

    from mongodb import db, collection

    # 1. SAFEGUARD CHECK: Fetch user's team layout first to ensure it's not empty
    team_record = db["teams"].find_one({"username": st.session_state["username"]})
    active_team = team_record.get("members", []) if team_record else []

    uploaded_file = st.file_uploader(
        "Upload Requirement Document",
        type=["txt","pdf","docx"]
    )

    if uploaded_file:

        if uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")

        elif uploaded_file.type == "application/pdf":
            pdf = PdfReader(uploaded_file)
            text = ""
            for page_obj in pdf.pages:
                page_text = page_obj.extract_text()
                if page_text:
                    text += page_text + "\n"
        else:
            text = "" # Fallback for structural safety

        st.success("Document uploaded successfully!")

        st.subheader("Document Preview")

        st.text_area(
            "Content",
            text,
            height=200
        )

        # 2. ENFORCE TEAM ROSTER CONFIGURATION BEFORE GENERATION
        if not active_team:
            st.markdown("<br>", unsafe_allow_html=True)
            st.warning("⚠️ Your engineering team roster is currently empty! Please head over to the **'Team Members'** navigation panel and add your squad members first before parsing requirements.")
        else:
            if st.button("🚀 Generate Tasks"):

                from ai_engine import generate_tasks

                with st.spinner("AI is analyzing document and distributing tasks among your squad..."):

                    # Pass the dynamic user-defined team directly into the AI parsing workflow
                    tasks = generate_tasks(text, active_team)
                    
                    for task in tasks:
                        task["status"] = False
                        task["progress"] = 0

                        if "assigned_user" not in task:
                            task["assigned_user"] = "Unassigned"

                        if "time_period" not in task:
                            task["time_period"] = "Not Estimated"

                    st.session_state["tasks"] = tasks
     
                    # Added "username" parameter mapping to preserve database data isolation layers
                    result = collection.insert_one({
                        "username": st.session_state["username"],
                        "document_name": uploaded_file.name,
                        "content": text,
                        "tasks": tasks
                    })
                    st.write("Saved ID:", result.inserted_id)

                    st.success("Tasks generated and allocated successfully!")

# ==========================================
# GENERATED TASKS PAGE
# ==========================================
# ==========================================
# GENERATED TASKS PAGE
# ==========================================
# ==========================================
# GENERATED TASKS PAGE
# ==========================================
elif page == "Generated Tasks":

    st.subheader("Generated Tasks")

    from mongodb import collection, db

    # Filter project list by the currently logged-in user for total isolation layer security
    projects = list(collection.find({"username": st.session_state["username"]}))

    if len(projects) > 0:

        project_names = [p["document_name"] for p in projects]

        selected_project = st.selectbox(
            "Select Project",
            project_names
        )

        # Match both document name AND the user's username for multi-tenant data protection
        project = collection.find_one(
            {
                "document_name": selected_project,
                "username": st.session_state["username"]
            }
        )

        tasks = project.get("tasks", [])
        for task in tasks:
            if "progress" not in task:
                task["progress"] = 0

            if "assigned_user" not in task:
                task["assigned_user"] = "Unassigned"

            if "time_period" not in task:
                task["time_period"] = "Not Estimated"
                
        collection.update_one(
            {"document_name": selected_project, "username": st.session_state["username"]},
            {"$set": {"tasks": tasks}}
        )
        
        df = pd.DataFrame(tasks)
        df = df.rename(columns={
            "task": "Task",
            "priority": "Priority",
            "description": "Description",
            "status": "Completed",
            "assigned_user": "Assigned User",
            "time_period": "Time Period"
        })

        # DYNAMIC ROSTER LOOKUP: Fetch this specific user's custom engineering team
        team_record = db["teams"].find_one({"username": st.session_state["username"]})
        if team_record and team_record.get("members"):
            team_members = team_record.get("members")
        else:
            # Clean fallback option if they haven't onboarded any teammates yet
            team_members = ["Unassigned"]

        # Render the interactive data editor containing only the user's explicit team dropdown choices
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Assigned User": st.column_config.SelectboxColumn(
                    "Assigned User",
                    options=team_members
                 )
            }
        )
        
        tasks = edited_df.rename(columns={
            "Task": "task",
            "Priority": "priority",
            "Description": "description",
            "Progress (%)": "progress",
            "Completed": "status",
            "Assigned User": "assigned_user",
            "Time Period": "time_period"
        }).to_dict("records")

        # Push back any live manual changes to the specific project under the user's account
        collection.update_one(
            {"document_name": selected_project, "username": st.session_state["username"]},
            {"$set": {"tasks": tasks}}
        )

        st.session_state["tasks"] = tasks
        excel_buffer = BytesIO()

        with pd.ExcelWriter(
             excel_buffer,
             engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Tasks"
            )

        st.download_button(
            label="📥 Download Excel Report",
            data=excel_buffer.getvalue(),
            file_name="AI_Generated_Tasks.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.info("No tasks generated yet.")

# ==========================================
# TEAM MEMBERS (DYNAMIC ENTERPRISE SETUP)
# ==========================================
# ==========================================
# TEAM MEMBERS (DYNAMIC ENTERPRISE SETUP)
# ==========================================
elif page == "Team Members":

    from mongodb import db, collection
    teams_collection = db["teams"]

    if "selected_member" not in st.session_state:
        st.session_state.selected_member = None

    current_user = st.session_state["username"]

    # 1. FETCH CURRENT ROSTER FROM DATABASE (Starts completely empty if new user)
    team_record = teams_collection.find_one({"username": current_user})
    if not team_record:
        default_team = []
        teams_collection.insert_one({"username": current_user, "members": default_team})
        team_members = default_team
    else:
        team_members = team_record.get("members", [])

    st.markdown("""
    <h1 style='color:#0B1F3A; margin-bottom:0; font-weight:800;'>Team Production Matrix</h1>
    <p style='color:#7B8794; font-size:16px; margin-top:4px;'>Manage your custom engineering squad and monitor live resource distribution metrics.</p>
    """, unsafe_allow_html=True)

    # 2. FULLY DYNAMIC MANAGEMENT PANEL (ADD / REMOVE MEMBERS)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("### ⚙️ Workspace Roster Control")
        col_add, col_rem = st.columns(2)
        
        with col_add:
            new_member = st.text_input("Add New Teammate Name", placeholder="Type teammate name...", key="add_name_input").strip()
            if st.button("➕ Add Member to Team", use_container_width=True):
                if new_member:
                    if new_member not in team_members:
                        teams_collection.update_one({"username": current_user}, {"$push": {"members": new_member}})
                        st.success(f"Added '{new_member}' successfully!")
                        st.rerun()
                    else:
                        st.warning("This member is already in your team!")
                else:
                    st.error("Please enter a name.")
                    
        with col_rem:
            if team_members:
                member_to_remove = st.selectbox("Select Teammate to Remove", team_members, key="remove_name_select")
                if st.button("🗑️ Delete Member from Team", use_container_width=True):
                    teams_collection.update_one({"username": current_user}, {"$pull": {"members": member_to_remove}})
                    st.warning(f"Removed '{member_to_remove}' from your team roster.")
                    st.rerun()
            else:
                st.selectbox("Select Teammate to Remove", ["No team members added yet"], disabled=True)
                st.button("🗑️ Delete Member from Team", disabled=True, use_container_width=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)

    # 3. COMPUTE LIVE METRICS BASED ON THE DYNAMIC ROSTER
    projects = list(collection.find({"username": current_user}))

    member_stats = {}
    for member in team_members:
        member_stats[member] = {
            "assigned": 0,
            "completed": 0,
            "pending": 0,
            "projects_map": {}
        }

    total_assigned = 0
    total_completed = 0

    for project in projects:
        project_name = project.get("document_name", "Unnamed Project")
        for task in project.get("tasks", []):
            user = task.get("assigned_user", "")
            if user not in member_stats:
                continue

            total_assigned += 1
            member_stats[user]["assigned"] += 1

            if project_name not in member_stats[user]["projects_map"]:
                member_stats[user]["projects_map"][project_name] = {"pending": [], "completed": []}

            if task.get("status", False):
                total_completed += 1
                member_stats[user]["completed"] += 1
                member_stats[user]["projects_map"][project_name]["completed"].append(task)
            else:
                member_stats[user]["pending"] += 1
                member_stats[user]["projects_map"][project_name]["pending"].append(task)

    total_pending = total_assigned - total_completed

    # Display Top Overview Metric Headers
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Active Squad Size", len(team_members))
    with c2:
        st.metric("Assigned Sprint Tasks", total_assigned)
    with c3:
        st.metric("Completed Tasks", total_completed)
    with c4:
        st.metric("Pending Backlog", total_pending)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 4. RENDER TEAM CARDS DYNAMICALLY
    if not team_members:
        st.info("💡 Your engineering team roster is completely empty! Use the 'Workspace Roster Control' menu above to add your teammates and start tracking tasks.")
    else:
        cols = st.columns(3)
        for i, (member, stats) in enumerate(member_stats.items()):
            with cols[i % 3]:
                progress = int((stats["completed"] / stats["assigned"] * 100)) if stats["assigned"] > 0 else 0
                badge = '🔴 Heavy' if stats["pending"] >= 6 else ('🟡 Mod' if 3 <= stats["pending"] <= 5 else '🟢 Light')
                
                st.markdown(f"""
                <div style="background: white; border-radius: 24px; padding: 28px 28px 20px 28px; box-shadow: 0 12px 35px rgba(0,0,0,.06); margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 22px;">
                        <h3 style="margin: 0; color: #0B1F3A; font-weight: 700; font-size: 22px;">{member}</h3>
                        <span style="font-size:12px; font-weight:700;">{badge} Workload</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 15px; color: #4B5563;"><span>📋 Assigned Tasks</span><b>{stats['assigned']}</b></div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 15px; color: #4B5563;"><span>✅ Completed Sprint</span><b style="color:#16A34A;">{stats['completed']}</b></div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 20px; font-size: 15px; color: #4B5563;"><span>⏳ Pending Tasks</span><b style="color:#EF4444;">{stats['pending']}</b></div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(progress / 100)
                if st.button(f"🔍 Profile Portfolio: {member}", key=f"view_{member}", use_container_width=True):
                    st.session_state.selected_member = member
# ==========================================
# ANALYTICS PAGE
# ==========================================
# ==========================================
# ANALYTICS PAGE
# ==========================================
elif page == "Analytics":

    import plotly.express as px
    import pandas as pd
    from mongodb import collection


    # =====================================
    # LOAD DATA FROM MONGODB (Isolated by User)
    # =====================================

    # FIX: Only load projects that belong to the active logged-in user session
    projects = list(collection.find({"username": st.session_state["username"]}))

    total_tasks = 0
    completed_tasks = 0
    high_tasks = 0
    medium_tasks = 0
    low_tasks = 0

    for project in projects:

        tasks = project.get("tasks", [])
        for task in tasks:

            if "assigned_user" not in task:
                task["assigned_user"] = "Unassigned"

            if "time_period" not in task:
                task["time_period"] = "Not Estimated"

        total_tasks += len(tasks)

        completed_tasks += len(
            [t for t in tasks if t.get("status", False)]
        )

        high_tasks += len(
            [t for t in tasks if t.get("priority") == "High"]
        )

        medium_tasks += len(
            [t for t in tasks if t.get("priority") == "Medium"]
        )

        low_tasks += len(
            [t for t in tasks if t.get("priority") == "Low"]
        )

    pending_tasks = total_tasks - completed_tasks

    # =====================================
    # QUICK STATS
    # =====================================

    st.markdown("##  Quick Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Tasks", total_tasks)

    with c2:
        st.metric("Completed", completed_tasks)

    with c3:
        st.metric("High Priority", high_tasks)

    with c4:
        st.metric("Projects", len(projects))

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # RENDERING THE VISUALIZATIONS Safely
    # =====================================
    if total_tasks == 0:
        st.info("📊 No project metrics available yet. Go to 'Upload Document' to process files and view system analytics!")
    else:
        # =====================================
        # PRIORITY DISTRIBUTION
        # =====================================

        st.markdown("""
        <div style="background:white; padding:20px; border-radius:20px; margin-bottom:15px;">
        <h2 style="color:#0B1F3A;">Task Priority Distribution</h2>
        <p style="color:#8A8F98;">Overview of High, Medium and Low priority tasks</p>
        </div>
        """, unsafe_allow_html=True)

        priority_df = pd.DataFrame({
            "Priority": ["High", "Medium", "Low"],
            "Count": [high_tasks, medium_tasks, low_tasks]
        })

        fig1 = px.pie(
            priority_df,
            names="Priority",
            values="Count",
            hole=0.45
        )

        fig1.update_layout(height=450)
        st.plotly_chart(fig1, use_container_width=True)

        # =====================================
        # COMPLETION STATUS
        # =====================================

        st.markdown("""
        <div style="background:white; padding:20px; border-radius:20px; margin-top:25px; margin-bottom:15px;">
        <h2 style="color:#0B1F3A;">Task Completion Status</h2>
        <p style="color:#8A8F98;">Track completed and pending tasks across projects</p>
        </div>
        """, unsafe_allow_html=True)

        completion_df = pd.DataFrame({
            "Status": ["Completed", "Pending"],
            "Count": [completed_tasks, pending_tasks]
        })

        fig2 = px.bar(
            completion_df,
            x="Status",
            y="Count",
            text="Count"
        )

        fig2.update_layout(height=450)
        st.plotly_chart(fig2, use_container_width=True) 
# ==========================================
# SAVED PROJECTS
# ==========================================
elif page == "Saved Projects":

    st.subheader("Saved Projects")

    from mongodb import collection

    # FIX: Filter the search query so users only see their own saved records
    projects = list(collection.find({"username": st.session_state["username"]}))

    st.write("Number of Projects:", len(projects))

    if len(projects) == 0:

        st.info("No projects saved yet.")

    else:

        for project in projects:

            st.markdown("---")

            st.write(
                f"📄 {project.get('document_name', 'Unknown Document')}"
            )

            st.write(
                f"Tasks: {len(project.get('tasks', []))}"
            )
