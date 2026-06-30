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

# Add a logout capability at the bottom of your sidebar options
if st.sidebar.button("🚪 Log Out", use_container_width=True):
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.rerun()
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

    border-right:1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"]{
    width:280px !important;
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
        "Upload Document",
        "Generated Tasks",
        "Team Members",
        "Analytics",
        "Saved Projects"
    ]
)
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
        projects = list(collection.find({"username"}))
        
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

    if len(projects) == 0:
        st.info("No projects available.")
    else:
        for project in reversed(projects[-5:]):
            tasks = project.get("tasks", [])
            total = len(tasks)
            completed = len([t for t in tasks if t.get("status", False)])
            progress = 0 if total == 0 else int((completed / total) * 100)

            st.markdown(f"""<div style="background:white; border-radius:25px; padding:25px; margin-bottom:18px; box-shadow:0 8px 30px rgba(0,0,0,0.07);"><h4 style="margin-bottom:8px; color:#0B1F3A;">{project.get("document_name","Untitled Project")}</h4><p style="color:#6B7280;">{total} Tasks &nbsp;&nbsp;|&nbsp;&nbsp; {completed} Completed</p><div style="width:100%; height:10px; background:#ECECEC; border-radius:20px; overflow:hidden; margin-top:12px;"><div style="width:{progress}%; height:10px; background:#D4A24C;"></div></div><p style="margin-top:12px; color:#6B7280;">Progress : <b>{progress}%</b></p></div>""", unsafe_allow_html=True)
# ==========================================
# UPLOAD PAGE
# ==========================================
elif page == "Upload Document":

    st.subheader("📄 Upload Knowledge Document")

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

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        st.success("Document uploaded successfully!")

        st.subheader("Document Preview")

        st.text_area(
            "Content",
            text,
            height=200
        )

        if st.button("🚀 Generate Tasks"):

            from ai_engine import generate_tasks

            with st.spinner("AI is analyzing document..."):

                tasks = generate_tasks(text)
                

                for task in tasks:

                    task["status"] = False

                    task["progress"] = 0

                    if "assigned_user" not in task:
                        task["assigned_user"] = "Unassigned"

                    if "time_period" not in task:
                        task["time_period"] = "Not Estimated"

                st.session_state["tasks"] = tasks
                from mongodb import collection
 
                result =  collection.insert_one({
                    "username": st.session_state["username"],
                    "document_name": uploaded_file.name,
                    "content": text,
                    "tasks": tasks
                })
                st.write("Saved ID:", result.inserted_id)

                st.success("Tasks generated successfully!")

# ==========================================
# GENERATED TASKS PAGE
# ==========================================

elif page == "Generated Tasks":

    st.subheader("Generated Tasks")

    from mongodb import collection

    projects = list(collection.find({"username": st.session_state["username"]}))

    if len(projects) > 0:

        project_names = [p["document_name"] for p in projects]

        selected_project = st.selectbox(
            "Select Project",
            project_names
        )

        project = collection.find_one(
            {"document_name": selected_project,
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

        team_members = [
            "Sanju",
            "Joanna",
            "Sahana",
            "Pradeep",
            "Rakshanaa",
            "Parkavi"
        ]
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

        collection.update_one(
            {"document_name": selected_project},
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
# TEAM MEMBERS (PREMIUM REDESIGN WITH PER-PROJECT SEGREGATION)
# ==========================================
elif page == "Team Members":

    from mongodb import collection

    if "selected_member" not in st.session_state:
        st.session_state.selected_member = None

    projects = list(collection.find({"username": st.session_state["username"]}))

    team_members = [
        "Sanju",
        "Joanna",
        "Sahana",
        "Pradeep",
        "Rakshanaa",
        "Parkavi"
    ]

    # Structure data mapping to preserve task arrays along with their parent project context
    member_stats = {}
    for member in team_members:
        member_stats[member] = {
            "assigned": 0,
            "completed": 0,
            "pending": 0,
            "projects_map": {}  # Structure: {"Project Name": {"pending": [], "completed": []}}
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

            # Initialize project buckets if tracking them for the first time for this user
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

    # ----------------------------------------------------
    # PREMIUM UI SYSTEM STYLING INSIGHTS
    # ----------------------------------------------------
    st.markdown("""
    <style>
    /* Clean up default Streamlit progress bar spacing */
    div[data-testid="stProgress"] {
        margin-top: -10px !important;
        margin-bottom: 15px !important;
    }
    
    /* Premium style normalization for secondary action buttons */
    div[data-testid="stBlock"] div[data-testid="stButton"] button {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        color: #0B1F3A !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stBlock"] div[data-testid="stButton"] button:hover {
        background-color: #D4A24C !important;
        color: white !important;
        border-color: #D4A24C !important;
        box-shadow: 0 4px 12px rgba(212,162,76,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style='color:#0B1F3A; margin-bottom:0; font-weight:800;'>Team Production Matrix</h1>
    <p style='color:#7B8794; font-size:16px; margin-top:4px;'>Manage task distribution profiles across your core development engineering sprint cycle.</p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Summary Metrics Headers
    c1, c2, c3, c4 = st.columns(4)

    def summary_card(title, value, color, border_color):
        st.markdown(f"""
        <div style="background: white; border-radius: 22px; padding: 22px; border-top: 5px solid {border_color}; box-shadow: 0 10px 30px rgba(0,0,0,0.06); height: 140px;">
            <p style="color: #6B7280; font-size: 12px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin: 0;">{title}</p>
            <h1 style="color: {color}; font-size: 42px; font-weight: 800; margin-top: 10px; margin-bottom: 0; line-height: 1;">{value}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c1:
        summary_card("Total Active Engine Users", 6, "#0B1F3A", "#0B1F3A")
    with c2:
        summary_card("Assigned Sprint Tasks", total_assigned, "#D4A24C", "#D4A24C")
    with c3:
        summary_card("Completed Tasks", total_completed, "#16A34A", "#16A34A")
    with c4:
        summary_card("Pending Backlog Tasks", total_pending, "#EF4444", "#EF4444")

    st.markdown("<br><br>", unsafe_allow_html=True)
    cols = st.columns(3)

    for i, (member, stats) in enumerate(member_stats.items()):
        with cols[i % 3]:
            progress = 0
            if stats["assigned"] > 0:
                progress = int((stats["completed"] / stats["assigned"]) * 100)

            if stats["pending"] >= 6:
                badge_html = '<span style="background:#FEE2E2; color:#B91C1C; font-size:12px; font-weight:700; padding:6px 14px; border-radius:20px;">🔴 Heavy Workload</span>'
            elif 3 <= stats["pending"] <= 5:
                badge_html = '<span style="background:#FEF3C7; color:#B45309; font-size:12px; font-weight:700; padding:6px 14px; border-radius:20px;">🟡 Moderate Workload</span>'
            else:
                badge_html = '<span style="background:#DCFCE7; color:#15803D; font-size:12px; font-weight:700; padding:6px 14px; border-radius:20px;">🟢 Light Workload</span>'

            st.markdown(f"""
            <div style="background: white; border-radius: 24px; padding: 28px 28px 20px 28px; box-shadow: 0 12px 35px rgba(0,0,0,.06); margin-bottom: 10px; position: relative;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 22px;">
                    <h3 style="margin: 0; color: #0B1F3A; font-weight: 700; font-size: 22px;">{member}</h3>
                    {badge_html}
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 15px; color: #4B5563;">
                    <span>📋 Assigned Tasks</span>
                    <span style="font-weight: 700; color: #0B1F3A;">{stats['assigned']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 15px; color: #4B5563;">
                    <span>✅ Completed Sprint</span>
                    <span style="font-weight: 700; color: #16A34A;">{stats['completed']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 20px; font-size: 15px; color: #4B5563;">
                    <span>⏳ Pending Tasks</span>
                    <span style="font-weight: 700; color: #EF4444;">{stats['pending']}</span>
                </div>
                <div style="font-size: 13px; color: #9CA3AF; margin-bottom: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Sprint Progress</div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(progress / 100)
            
            if st.button(f"🔍 Profile Portfolio: {member}", key=f"view_{member}", use_container_width=True):
                st.session_state.selected_member = member

# ----------------------------------------------------
# DRILLDOWN PANEL: MULTI-PROJECT SEGREGATED LEDGER VIEW
# ----------------------------------------------------
if st.session_state.get("selected_member"):
    member = st.session_state.selected_member

    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    back_col, title_col = st.columns([1, 6])
    with back_col:
        st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
        if st.button("⬅ Back", key="back_button", use_container_width=True):
            st.session_state.selected_member = None
            st.rerun()
            
    with title_col:
        st.markdown(f"<h2 style='color:#0B1F3A; margin: 0; font-weight: 700;'>Task Ledger for {member}</h2>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    user_projects = member_stats[member]["projects_map"]

    if len(user_projects) == 0:
        st.info("No developmental tasks registered to this specific project owner account.")
    else:
        # Helper card layout engine to keep styling completely clean
        def render_task_card(task, is_completed):
            status_pill = '<span style="background:#DCFCE7; color:#15803D; padding:4px 12px; border-radius:12px; font-size:13px; font-weight:600;">✅ Completed</span>' if is_completed else '<span style="background:#FEF3C7; color:#B45309; padding:4px 12px; border-radius:12px; font-size:13px; font-weight:600;">⏳ Pending</span>'
            priority_color = "#EF4444" if task.get("priority") == "High" else ("#F59E0B" if task.get("priority") == "Medium" else "#3B82F6")
            
            st.markdown(f"""
            <div style="background: white; padding: 25px; border-radius: 20px; margin-bottom: 18px; box-shadow: 0 8px 25px rgba(0,0,0,.04); border-left: 5px solid {priority_color};">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                    <h4 style="margin: 0; color: #0B1F3A; font-size: 18px; font-weight: 700;">{task.get("task","Task")}</h4>
                    <div>
                        <span style="background:#F1F5F9; color:#475569; padding:4px 12px; border-radius:12px; font-size:13px; font-weight:600; margin-right:8px;">⏱ {task.get("time_period","-")}</span>
                        {status_pill}
                    </div>
                </div>
                <p style="color: #4B5563; font-size: 15px; margin: 0; line-height: 1.6;">{task.get("description","")}</p>
            </div>
            """, unsafe_allow_html=True)

        # Loop through each project that has tasks belonging to this user
        for proj_name, status_buckets in user_projects.items():
            p_pending = status_buckets["pending"]
            p_completed = status_buckets["completed"]
            
            # Skip compiling layout if a project exists in db but holds zero items for this specific engineer
            if not p_pending and not p_completed:
                continue

            # Render Project Title Block Section Container Header
            st.markdown(f"""
            <div style="background: #0B1F3A; padding: 14px 25px; border-radius: 14px; margin-top: 30px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(11,31,58,0.15);">
                <h3 style="margin: 0; color: white; font-weight: 700; font-size: 20px; letter-spacing: 0.5px;">📁 PROJECT: {proj_name.upper()}</h3>
            </div>
            """, unsafe_allow_html=True)

            # Sub-split 1: Pending Tasks under this specific project title
            st.markdown("<h4 style='color:#EF4444; margin-bottom:12px; font-weight:700; padding-left:5px;'>⏳ Pending Backlog</h4>", unsafe_allow_html=True)
            if not p_pending:
                st.markdown("<p style='color:#6B7280; font-size:14px; padding-left:15px; margin-bottom:20px;'>🎉 No pending tasks for this project.</p>", unsafe_allow_html=True)
            else:
                for task in p_pending:
                    render_task_card(task, is_completed=False)

            # Sub-split 2: Completed Tasks under this specific project title
            st.markdown("<h4 style='color:#16A34A; margin-bottom:12px; font-weight:700; padding-left:5px; margin-top:15px;'>✅ Completed Tasks</h4>", unsafe_allow_html=True)
            if not p_completed:
                st.markdown("<p style='color:#6B7280; font-size:14px; padding-left:15px; margin-bottom:20px;'>No completed tasks under this project yet.</p>", unsafe_allow_html=True)
            else:
                for task in p_completed:
                    render_task_card(task, is_completed=True)
# ==========================================
# ANALYTICS PAGE
# ==========================================
elif page == "Analytics":

    import plotly.express as px
    import pandas as pd
    from mongodb import collection


    # =====================================
    # LOAD DATA FROM MONGODB
    # =====================================

    projects = list(collection.find({}))

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
    # PRIORITY DISTRIBUTION
    # =====================================

    st.markdown("""
    <div style="
    background:white;
    padding:20px;
    border-radius:20px;
    margin-bottom:15px;
    ">
    <h2 style="color:#0B1F3A;">
       Task Priority Distribution
    </h2>

    <p style="color:#8A8F98;">
    Overview of High, Medium and Low priority tasks
    </p>
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
    <div style="
    background:white;
    padding:20px;
    border-radius:20px;
    margin-top:25px;
    margin-bottom:15px;
    ">
    <h2 style="color:#0B1F3A;">
       Task Completion Status
    </h2>

    <p style="color:#8A8F98;">
    Track completed and pending tasks across projects
    </p>
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

    st.subheader("📁 Saved Projects")

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
