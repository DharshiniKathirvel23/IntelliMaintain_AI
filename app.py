
import os
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st
import chromadb

from database import (
    initialize_database,
    save_incident,
    get_machine_history
)


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="IntelliMaintain AI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. GLOBAL DARK THEME
# =====================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #07111f 0%,
        #0b1628 55%,
        #101d32 100%
    );
    color: #e5edf8;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header */
header[data-testid="stHeader"] {
    background: #091426 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #091426 !important;
    border-right: 1px solid #24405f;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #cbdcf0 !important;
}

/* General text */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #ffffff !important;
}

.stApp p,
.stApp label,
.stApp li {
    color: #d5e2f1;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #142944,
        #102039
    );
    border: 1px solid #28547a;
    border-radius: 14px;
    padding: 20px;
}

[data-testid="stMetricLabel"] {
    color: #93c5fd !important;
}

[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
    font-weight: 700;
}

/* Text inputs */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #142944 !important;
    color: #ffffff !important;
    border: 1px solid #315477 !important;
    border-radius: 9px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #9bb0c9 !important;
}

/* Dropdowns */
.stSelectbox [data-baseweb="select"] > div {
    background: #142944 !important;
    border: 1px solid #315477 !important;
    color: #ffffff !important;
}

.stSelectbox [data-baseweb="select"] * {
    color: #ffffff !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background: #142944 !important;
}

[data-baseweb="option"] {
    background: #142944 !important;
    color: #ffffff !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(
        90deg,
        #1677d2,
        #06a6c9
    ) !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 600;
    padding: 10px 20px;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    box-shadow: 0 0 18px rgba(14,165,233,0.35);
    border: 1px solid #38bdf8 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #142944 !important;
    border: 1px dashed #3484bd !important;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stFileUploader"] * {
    color: #e5edf8 !important;
}

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid #294765;
    border-radius: 10px;
}

/* Expanders */
[data-testid="stExpander"] {
    background: #102039;
    border: 1px solid #285078;
    border-radius: 10px;
}

[data-testid="stExpander"] summary {
    color: #ffffff !important;
}

/* Custom feature cards */
.feature-card {
    background: linear-gradient(
        145deg,
        #142944,
        #102039
    );
    border: 1px solid #28547a;
    border-radius: 14px;
    padding: 22px;
    min-height: 145px;
    margin-bottom: 12px;
}

.feature-card h3 {
    color: #38bdf8 !important;
    font-size: 19px;
    margin-bottom: 12px;
}

.feature-card p {
    color: #d5e2f1 !important;
    font-size: 14px;
    line-height: 1.6;
}

/* Hero section */
.hero-card {
    background: linear-gradient(
        120deg,
        #12345a,
        #102039,
        #123d55
    );
    border: 1px solid #2872a8;
    border-radius: 18px;
    padding: 30px;
    margin-bottom: 25px;
}

.hero-card h1 {
    color: #ffffff !important;
    font-size: 34px;
    margin-bottom: 10px;
}

.hero-card p {
    color: #c7e6ff !important;
    font-size: 16px;
}

/* Agent cards */
.agent-card {
    background: #102039;
    border: 1px solid #28547a;
    border-radius: 12px;
    padding: 18px;
    min-height: 130px;
}

.agent-card h4 {
    color: #38bdf8 !important;
    margin-bottom: 10px;
}

.agent-card p {
    color: #d5e2f1 !important;
    font-size: 13px;
}

/* Status text */
.status-text {
    color: #4ade80 !important;
    font-weight: 600;
}

/* Divider */
hr {
    border-color: #294765 !important;
}

/* Links */
.stApp a {
    color: #38bdf8 !important;
}

/* Hide footer */
footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. DATABASE INITIALIZATION
# =====================================================

initialize_database()

os.makedirs("data", exist_ok=True)

DATABASE_PATH = "data/machine_memory.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize_machine_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT UNIQUE NOT NULL,
            machine_name TEXT NOT NULL,
            machine_type TEXT,
            location TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


initialize_machine_table()


# =====================================================
# 4. CHROMADB CONNECTION
# =====================================================

chroma_client = chromadb.PersistentClient(
    path="data/chroma_db"
)

document_collection = chroma_client.get_or_create_collection(
    name="machine_documents"
)


# =====================================================
# 5. HELPER FUNCTIONS
# =====================================================

def get_incident_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM machine_incidents"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


def get_machine_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM machines
    """)

    registered_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT machine_id)
        FROM machine_incidents
        WHERE machine_id NOT IN (
            SELECT machine_id FROM machines
        )
    """)

    incident_count = cursor.fetchone()[0]

    connection.close()

    return registered_count + incident_count


def get_all_machines():

    connection = get_connection()

    df = pd.read_sql_query("""
        SELECT *
        FROM machines
        ORDER BY id DESC
    """, connection)

    connection.close()

    return df


def get_all_incidents():

    connection = get_connection()

    df = pd.read_sql_query("""
        SELECT
            id,
            machine_id,
            reported_fault,
            created_at
        FROM machine_incidents
        ORDER BY id DESC
    """, connection)

    connection.close()

    return df


def dark_card(title, description, icon):

    st.markdown(f"""
    <div class="feature-card">
        <h3>{icon} {title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# 6. SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.markdown(
        "<h2>⚙️ IntelliMaintain AI</h2>",
        unsafe_allow_html=True
    )

    st.caption(
        "Agentic AI-Powered Industrial Maintenance System"
    )

    st.divider()

    st.markdown("### Navigation")

    pages = [
        "Dashboard",
        "Machine Management",
        "Document Upload",
        "AI Maintenance Copilot",
        "Incident Investigation",
        "Maintenance History"
    ]

    page = st.selectbox(
        "Select Page",
        pages,
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("""
    <div class="feature-card">
        <h3>🤖 AI Assistant</h3>
        <p>
        Intelligent industrial maintenance
        and machine fault investigation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p class='status-text'>● System Online</p>",
        unsafe_allow_html=True
    )


# =====================================================
# 7. DASHBOARD
# =====================================================


# =====================================================
# PREMIUM INDUSTRIAL COMMAND CENTER
# =====================================================

if page == "Dashboard":

    # Dashboard header
    st.markdown("""
    <div style="
        background:linear-gradient(120deg,#102c4d,#123c59,#102039);
        border:1px solid #2872a8;
        border-radius:18px;
        padding:30px;
        margin-bottom:25px;
    ">
        <div style="color:#38bdf8;font-size:12px;
                    font-weight:bold;letter-spacing:2px;">
            INDUSTRIAL INTELLIGENCE CENTER
        </div>
        <h1 style="font-size:34px;margin:12px 0;color:white;">
            ⚙ IntelliMaintain AI
        </h1>
        <p style="color:#c7e6ff;font-size:15px;">
            Intelligent machine monitoring, fault investigation
            and predictive maintenance assistance.
        </p>
        <div style="color:#4ade80;font-size:13px;">
            ● PLATFORM READY
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Actual database statistics
    machine_total = get_machine_count()
    incident_total = get_incident_count()
    document_total = document_collection.count()

    st.markdown("### 📊 Operations Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🏭 Machines", machine_total)

    with c2:
        st.metric("🔍 Investigations", incident_total)

    with c3:
        st.metric("📚 Document Chunks", document_total)

    with c4:
        st.metric("🤖 AI Agents", 3)

    st.markdown("---")

    # Main dashboard columns
    left, right = st.columns([1.5, 1])

    with left:

        st.markdown("### 🏭 Recent Machine Activity")

        recent = get_all_incidents()

        if not recent.empty:

            for _, record in recent.head(4).iterrows():

                machine_id = str(record["machine_id"])
                fault = str(record["reported_fault"])
                created_at = str(record["created_at"])

                with st.container(border=True):
                    st.markdown(f"**:blue[MACHINE {machine_id}]**")
                    st.write(fault)
                    st.caption(f"Investigation Date: {created_at}")

        else:
            st.info("No maintenance activity recorded yet.")

    with right:

        st.markdown("### 🧠 AI System Health")

        modules = [
            ("Hybrid RAG", "Technical document retrieval"),
            ("Machine Memory", "Historical incident storage"),
            ("Knowledge Agent", "Technical knowledge retrieval"),
            ("Fault Agent", "Fault investigation"),
            ("Recommendation Agent", "Maintenance planning")
        ]

        for name, description in modules:

            st.markdown(f"""
            <div style="
                background:#142944;
                border:1px solid #28547a;
                border-radius:9px;
                padding:12px;
                margin-bottom:10px;
            ">
                <div style="display:flex;
                            justify-content:space-between;">
                    <span style="color:#ffffff;font-weight:600;">
                        {name}
                    </span>
                    <span style="color:#4ade80;">● Ready</span>
                </div>
                <div style="color:#9bb0c9;font-size:12px;
                            margin-top:5px;">
                    {description}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Analytics
    st.markdown("### 📈 Maintenance Analytics")

    analytics_left, analytics_right = st.columns(2)

    with analytics_left:

        st.markdown("#### Investigations by Machine")

        if not recent.empty:

            machine_counts = (
                recent["machine_id"]
                .value_counts()
            )

            st.bar_chart(machine_counts)

        else:

            st.caption("Investigation data will appear here.")

    with analytics_right:

        st.markdown("#### Investigation Summary")

        st.markdown(f"""
        <div style="
            background:linear-gradient(145deg,#142944,#102039);
            border:1px solid #28547a;
            border-radius:13px;
            padding:20px;
        ">
            <div style="color:#93c5fd;font-size:13px;">
                TOTAL SAVED INVESTIGATIONS
            </div>
            <div style="color:#38bdf8;font-size:38px;
                        font-weight:bold;margin:8px 0;">
                {incident_total}
            </div>
            <div style="color:#cbdcf0;font-size:13px;">
                Machine-specific records stored in SQLite.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="text-align:center;padding:15px;">
        <span style="color:#38bdf8;font-weight:bold;">
            INTELLIMAINTAIN AI
        </span>
        <p style="color:#8da6c2;font-size:12px;">
            Hybrid RAG • CAG • Machine Memory • Multi-Agent AI
        </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 8. MACHINE MANAGEMENT
# =====================================================

elif page == "Machine Management":

    st.title("🏭 Machine Management")

    st.write(
        "Register and manage industrial machines."
    )

    with st.form("machine_registration_form"):

        st.subheader("Register New Machine")

        machine_id = st.text_input(
            "Machine ID",
            placeholder="Example: M102"
        )

        machine_name = st.text_input(
            "Machine Name",
            placeholder="Example: Industrial Pump"
        )

        machine_type = st.selectbox(
            "Machine Type",
            [
                "Industrial Motor",
                "Pump",
                "Compressor",
                "Conveyor",
                "Generator",
                "Other"
            ]
        )

        location = st.text_input(
            "Machine Location",
            placeholder="Example: Production Unit 1"
        )

        submitted = st.form_submit_button(
            "Register Machine"
        )

        if submitted:

            if not machine_id.strip() or not machine_name.strip():

                st.warning(
                    "Please enter Machine ID and Machine Name."
                )

            else:

                try:

                    connection = get_connection()
                    cursor = connection.cursor()

                    cursor.execute("""
                        INSERT INTO machines (
                            machine_id,
                            machine_name,
                            machine_type,
                            location,
                            created_at
                        )
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        machine_id.strip(),
                        machine_name.strip(),
                        machine_type,
                        location.strip(),
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    ))

                    connection.commit()
                    connection.close()

                    st.success(
                        "Machine registered successfully!"
                    )

                    st.rerun()

                except sqlite3.IntegrityError:

                    st.error(
                        "This Machine ID already exists."
                    )

    st.divider()

    st.subheader("Registered Machines")

    machines_df = get_all_machines()

    if not machines_df.empty:

        st.dataframe(
            machines_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No machines registered yet. Add your first machine above."
        )


# =====================================================
# 9. DOCUMENT UPLOAD
# =====================================================

elif page == "Document Upload":

    from rag.document_processor import (
        extract_pdf_text,
        split_text
    )

    from rag.retriever import store_chunks

    st.title("📄 Machine Document Upload")

    st.write(
        "Upload machine manuals and maintenance reports "
        "for AI-based technical knowledge retrieval."
    )

    st.markdown("""
    <div class="feature-card">
        <h3>📚 Hybrid RAG Document Processing</h3>
        <p>
        PDF Extraction → Text Chunking →
        Embedding Generation → ChromaDB Storage
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Machine Manual or Maintenance Report",
        type=["pdf"]
    )

    machine_id = st.text_input(
        "Enter Machine ID for this document",
        value="M101"
    )

    if uploaded_file is not None:

        st.success(
            f"Selected document: {uploaded_file.name}"
        )

        if st.button("Process and Store Document"):

            if not machine_id.strip():

                st.warning(
                    "Please enter a Machine ID."
                )

            else:

                try:

                    uploaded_file.seek(0)

                    extracted_text = extract_pdf_text(
                        uploaded_file
                    )

                    if not extracted_text.strip():

                        st.warning(
                            "No readable text found in this PDF."
                        )

                    else:

                        chunks = split_text(
                            extracted_text
                        )

                        store_chunks(
                            chunks,
                            uploaded_file.name,
                            machine_id=machine_id.strip()
                        )

                        st.success(
                            "Document processed and stored successfully!"
                        )

                        col1, col2 = st.columns(2)

                        col1.metric(
                            "Extracted Characters",
                            len(extracted_text)
                        )

                        col2.metric(
                            "Generated Chunks",
                            len(chunks)
                        )

                        with st.expander(
                            "Preview Extracted Text"
                        ):

                            st.text(
                                extracted_text[:3000]
                            )

                except Exception as e:

                    st.error(
                        f"Document processing error: {e}"
                    )

    st.divider()

    st.subheader("Document Database")

    st.metric(
        "Total Stored Chunks",
        document_collection.count()
    )


# =====================================================
# 10. AI MAINTENANCE COPILOT
# =====================================================

elif page == "AI Maintenance Copilot":

    from agents.workflow import maintenance_app

    st.title("🤖 AI Maintenance Copilot")

    st.write(
        "Investigate machine faults using a multi-agent AI workflow."
    )

    st.markdown("""
    <div class="feature-card">
        <h3>Intelligent Fault Investigation</h3>
        <p>
        The three AI agents work together to retrieve knowledge,
        investigate possible faults and prepare maintenance recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    machines_df = get_all_machines()

    registered_ids = (
        machines_df["machine_id"].tolist()
        if not machines_df.empty else []
    )

    machine_id = st.text_input(
        "Enter Machine ID",
        value="M101"
    )

    question = st.text_area(
        "Describe the Machine Problem",
        placeholder=(
            "Example: The industrial motor is experiencing "
            "excessive vibration during operation."
        ),
        height=130
    )

    if st.button(
        "🔍 Investigate Machine Fault",
        use_container_width=True
    ):

        if not machine_id.strip():

            st.warning(
                "Please enter a Machine ID."
            )

        elif not question.strip():

            st.warning(
                "Please describe the machine problem."
            )

        else:

            initial_state = {
                "machine_id": machine_id.strip(),
                "question": question,
                "technical_context": "",
                "fault_analysis": "",
                "maintenance_plan": ""
            }

            try:

                with st.spinner(
                    "AI agents are investigating the machine problem..."
                ):

                    result = maintenance_app.invoke(
                        initial_state
                    )

                st.success(
                    "Machine investigation completed!"
                )

                st.session_state["last_result"] = result

                st.subheader(
                    "Investigation Results"
                )

                with st.expander(
                    "1. Technical Information",
                    expanded=True
                ):

                    st.markdown(
                        result["technical_context"]
                    )

                with st.expander(
                    "2. Fault Investigation",
                    expanded=True
                ):

                    st.markdown(
                        result["fault_analysis"]
                    )

                with st.expander(
                    "3. Maintenance Recommendation",
                    expanded=True
                ):

                    st.markdown(
                        result["maintenance_plan"]
                    )

                save_incident(
                    machine_id.strip(),
                    question,
                    result["technical_context"],
                    result["fault_analysis"],
                    result["maintenance_plan"]
                )

                st.success(
                    "Investigation saved in Machine Memory."
                )

            except Exception as e:

                st.error(
                    f"Investigation error: {e}"
                )

    # Show previous result after Streamlit reruns
    elif "last_result" in st.session_state:

        result = st.session_state["last_result"]

        st.subheader("Last Investigation")

        with st.expander("Technical Information"):

            st.markdown(
                result["technical_context"]
            )

        with st.expander("Fault Investigation"):

            st.markdown(
                result["fault_analysis"]
            )

        with st.expander("Maintenance Recommendation"):

            st.markdown(
                result["maintenance_plan"]
            )


# =====================================================
# 11. INCIDENT INVESTIGATION
# =====================================================

elif page == "Incident Investigation":

    st.title("🔎 Incident Investigation")

    st.write(
        "View previously recorded machine incidents."
    )

    incidents_df = get_all_incidents()

    if not incidents_df.empty:

        st.metric(
            "Total Recorded Incidents",
            len(incidents_df)
        )

        st.dataframe(
            incidents_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("View Incident Details")

        incident_id = st.selectbox(
            "Select Incident ID",
            incidents_df["id"].tolist()
        )

        selected_incident = incidents_df[
            incidents_df["id"] == incident_id
        ].iloc[0]

        records = get_machine_history(
            selected_incident["machine_id"]
        )

        matching_record = next(
            (
                record for record in records
                if record[0] == incident_id
            ),
            None
        )

        if matching_record:

            st.markdown(
                f"### Machine: {matching_record[1]}"
            )

            st.markdown(
                f"**Reported Problem:** {matching_record[2]}"
            )

            with st.expander(
                "Technical Context"
            ):

                st.markdown(
                    matching_record[3] or "No technical context."
                )

            with st.expander(
                "Fault Analysis"
            ):

                st.markdown(
                    matching_record[4] or "No fault analysis."
                )

            with st.expander(
                "Maintenance Recommendation"
            ):

                st.markdown(
                    matching_record[5] or "No maintenance plan."
                )

            st.caption(
                f"Recorded at: {matching_record[6]}"
            )

    else:

        st.info(
            "No incidents available. Use the AI Maintenance Copilot first."
        )


# =====================================================
# 12. MAINTENANCE HISTORY
# =====================================================

elif page == "Maintenance History":

    st.title("📊 Maintenance History")

    st.write(
        "Review historical maintenance records for individual machines."
    )

    connection = get_connection()

    history_df = pd.read_sql_query("""
        SELECT
            id,
            machine_id,
            reported_fault,
            created_at
        FROM machine_incidents
        ORDER BY id DESC
    """, connection)

    connection.close()

    if not history_df.empty:

        col1, col2 = st.columns(2)

        col1.metric(
            "Total Maintenance Records",
            len(history_df)
        )

        col2.metric(
            "Machines with Incidents",
            history_df["machine_id"].nunique()
        )

        st.divider()

        machine_options = [
            "All Machines"
        ] + sorted(
            history_df["machine_id"].unique().tolist()
        )

        selected_machine = st.selectbox(
            "Filter by Machine",
            machine_options
        )

        if selected_machine != "All Machines":

            filtered_df = history_df[
                history_df["machine_id"] == selected_machine
            ]

        else:

            filtered_df = history_df

        st.subheader("Maintenance Records")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("Incident Distribution by Machine")

        chart_data = (
            history_df["machine_id"]
            .value_counts()
        )

        st.bar_chart(chart_data)

    else:

        st.info(
            "No maintenance history available yet."
        )


# =====================================================
# 13. FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    padding:15px;
    color:#8da6c2;
">
    <p>
    ⚙️ IntelliMaintain AI |
    Agentic AI-Powered Industrial Maintenance System
    </p>
    <p>
    Hybrid RAG • CAG • Machine Memory • Multi-Agent AI
    </p>
</div>
""", unsafe_allow_html=True)
