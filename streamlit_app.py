import streamlit as st
import pandas as pd
import numpy as np
import pickle
import re
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageOps
from datetime import date, datetime, time
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.units import mm
from io import BytesIO


model = pickle.load(open("model.pkl", "rb"))

try:
    dataset = pd.read_csv("Diabetic_Prediction.csv")
except Exception:
    dataset = None

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Diabetes Health",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "dashboard_page" not in st.session_state:
    st.session_state.dashboard_page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "selected_member_id" not in st.session_state:
    st.session_state.selected_member_id = None

if "selected_member_name" not in st.session_state:
    st.session_state.selected_member_name = None


# =========================================================
# THEME
# =========================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .stApp {
        background-color: #070b10;
        color: white;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: white !important;
    }

    p, label {
        color: #aeb8c5 !important;
    }

    div.stButton > button {
        min-height: 52px;
        border-radius: 12px;
        border: 1px solid rgba(212, 175, 55, 0.55);

        background:
            linear-gradient(
                135deg,
                rgba(212, 175, 55, 0.14),
                rgba(63, 169, 245, 0.10),
                rgba(11, 107, 79, 0.14)
            );

        color: #f5f5f5;
        font-size: 16px;
        font-weight: 700;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.25);

        transition:
            background 0.25s ease,
            border-color 0.25s ease,
            box-shadow 0.25s ease,
            transform 0.25s ease;
    }

    div.stButton > button:hover {
        background:
            linear-gradient(
                135deg,
                rgba(212, 175, 55, 0.28),
                rgba(63, 169, 245, 0.18),
                rgba(11, 107, 79, 0.25)
            );

        border-color: #d4af37;
        color: #ffffff;

        box-shadow:
            0 10px 30px rgba(212, 175, 55, 0.14),
            0 0 18px rgba(63, 169, 245, 0.08);

        transform: translateY(-2px);
    }

    div.stButton > button:active {
        transform: translateY(0px);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #0d141c;
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NAVBAR
# =========================================================
def navbar():

    left, right = st.columns([3.5, 1])

    with left:

        logo_col, title_col = st.columns(
            [0.4, 4],
            gap="small"
        )

        with logo_col:
            st.image("Logo.png", width=54)

        with title_col:
            st.markdown(
                """
                <div style="
                    font-size:44px;
                    font-weight:750;
                    color:#ffffff;
                    margin-top:3px;
                    margin-left:-18px;
                    line-height:1.2;
                    white-space:nowrap;
                ">
                    Diabetes <span style="color:#d4af37;">Health</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    with right:
        st.markdown(
            """
            <div style="
                text-align:right;
                padding-top:15px;
                padding-right:5px;
                color:#d4af37;
                font-size:20px;
                white-space:nowrap;
            ">
                Understand&nbsp;&nbsp;•&nbsp;&nbsp;Track&nbsp;&nbsp;•&nbsp;&nbsp;Take Action
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# DASHBOARD SIDEBAR
# =========================================================

def dashboard_sidebar():

    with st.sidebar:

        st.markdown("## DiabetesHealth")
        st.caption("Personal Health Support")

        st.divider()

        if st.button(
            "⌂  Dashboard",
            use_container_width=True
        ):
            st.session_state.dashboard_page = "home"
            st.rerun()

        if st.button(
            "🩺  Assessment",
            use_container_width=True
        ):
            st.session_state.dashboard_page = "assessment"
            st.rerun()

        if st.button(
            "👤  My Assessment",
            use_container_width=True
        ):
            st.session_state.dashboard_page = "my_assessment"
            st.rerun()

        if st.button(
            "👨‍👩‍👧  Family Members Assessment",
            use_container_width=True
        ):
            st.session_state.dashboard_page = "family"
            st.rerun()

        if st.button(
            "📊  Analytics",
            use_container_width=True
        ):
            st.session_state.dashboard_page = "analytics"
            st.rerun()

        if st.button(
            "📈  Progress",
            use_container_width=True
        ):
            st.session_state.dashboard_page = "progress"
            st.rerun()

        if st.button(
            "🔔  Reminders",
            use_container_width=True
        ):
            st.session_state.dashboard_page = "reminders"
            st.rerun()

        if st.button(
            "📚  Health Knowledge",
            use_container_width=True
        ):
            st.session_state.dashboard_page = "knowledge"
            st.rerun()

        if st.button(
            "📄  Reports",
            use_container_width=True
        ):
            st.session_state.dashboard_page = "reports"
            st.rerun()

        st.divider()

        if st.button(
            "⚙️  Profile",
            use_container_width=True
        ):
            st.session_state.dashboard_page = "profile"
            st.rerun()

        if st.button(
            "Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.session_state.page = "landing"
            st.session_state.dashboard_page = "home"

            st.rerun()


# =========================================================
# LANDING PAGE
# =========================================================

def landing_page():

    navbar()

    st.markdown(
    """
    <style>

    .st-key-feature-card-1,
    .st-key-feature-card-2,
    .st-key-feature-card-3,
    .st-key-process-card-1,
    .st-key-process-card-2,
    .st-key-process-card-3,
    .st-key-process-card-4,
    .st-key-info-card-1,
    .st-key-info-card-2{
        border: 1px solid rgba(212, 175, 55, 0.50);
        box-shadow: 0 6px 24px rgba(212, 175, 55, 0.16);
        border-radius: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    st.caption("MACHINE LEARNING POWERED HEALTH ASSESSMENT")

    st.markdown("# Understand your health.")
    st.markdown("## Track your diabetes risk.")

    st.write(
        "A personal health-support platform that uses machine learning "
        "to assess diabetes risk, preserve your assessment history, "
        "track changes over time, and provide useful health information."
    )

    st.write("")

    button1, button2, empty = st.columns([1, 1, 2])

    with button1:

        if st.button(
            "Get Started",
            use_container_width=True
        ):

            st.session_state.page = "signup"
            st.rerun()

    with button2:

        if st.button(
            "Login",
            use_container_width=True
        ):

            st.session_state.page = "login"
            st.rerun()

    st.write("")
    st.write("")

    st.markdown("## Everything in one place")
    st.caption("More than a one-time prediction.")

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True, key="feature-card-1"):

            st.markdown("### 🩺 Health Assessment")

            st.write(
                "Assess diabetes risk using important health "
                "indicators such as BMI, HbA1c, blood glucose "
                "and other relevant factors."
            )

    with col2:

        with st.container(border=True, key="feature-card-2"):

            st.markdown("### 📈 Track Progress")

            st.write(
                "Keep previous assessments and understand how "
                "your health indicators change over time."
            )

    with col3:

        with st.container(border=True, key="feature-card-3"):

            st.markdown("### 👨‍👩‍👧 Family Tracking")

            st.write(
                "Keep assessment histories for family members "
                "from one personal account."
            )

    st.write("")
    st.write("")

    st.markdown("## How it works")

    st.caption(
        "A simple process designed around your health journey."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        with st.container(border=True, key="process-card-1"):

            st.markdown("### 01")
            st.markdown("#### Create Account")

            st.write(
                "Create your personal account and manage "
                "your information securely."
            )

    with col2:

        with st.container(border=True, key="process-card-2"):

            st.markdown("### 02")
            st.markdown("#### Enter Health Data")

            st.write(
                "Provide the health information required "
                "for your assessment."
            )

    with col3:

        with st.container(border=True, key="process-card-3"):

            st.markdown("### 03")
            st.markdown("#### Get Assessment")

            st.write(
                "The machine learning model analyzes "
                "the information you provide."
            )

    with col4:

        with st.container(border=True, key="process-card-4"):

            st.markdown("### 04")
            st.markdown("#### Track & Learn")

            st.write(
                "Save assessments, view progress and "
                "explore useful health knowledge."
            )

    st.write("")
    st.write("")

    with st.container(border=True, key="info-card-1"):

        st.markdown("### From Prediction to Personal Health Tracking")

        st.write(
            "DiabetesHealth is designed to go beyond a single "
            "machine-learning prediction. Your assessment history "
            "can help you understand changes in health indicators "
            "over time, while health information and reminders "
            "can support better awareness and follow-up."
        )

    st.write("")

    with st.container(border=True, key="info-card-2"):

        st.markdown("### Important Health Information")

        st.write(
            "This platform provides a machine-learning-based risk "
            "assessment for educational and informational purposes. "
            "It is not a medical diagnosis and should not replace "
            "advice, diagnosis, or treatment from a qualified "
            "healthcare professional."
        )

    st.divider()

    st.caption(
        "DiabetesHealth • Machine Learning Health Support Platform"
    )


# =========================================================
# SIGNUP PAGE
# =========================================================

def signup_page():

    navbar()

    st.write("")
    st.write("")

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown("# Create your account")

        st.caption(
            "Start your personal health journey."
        )

        st.write(
            "Create an account to save assessments, "
            "track progress and manage your health "
            "information in one place."
        )

        st.write("")

        with st.container(border=True):

            with st.form("signup_form"):

                full_name = st.text_input(
                    "Full Name",
                    placeholder="Enter your full name"
                )

                email = st.text_input(
                    "Email",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter password"
                )

                st.caption(
                    "12+ characters • uppercase • lowercase • number • special character"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter password"
                )

                create_account = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )

        if create_account:

            full_name = full_name.strip()
            email = email.strip().lower()

            # -------------------------
            # BASIC VALIDATION
            # -------------------------

            if not full_name:

                st.error(
                    "Please enter your full name."
                )

            elif not email:

                st.error(
                    "Please enter your email."
                )

            # Proper email validation
            elif not re.match(
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                email
            ):

                st.error(
                    "Please enter a valid email address."
                )

            elif not password:

                st.error(
                    "Please enter a password."
                )

            # -------------------------
            # PASSWORD VALIDATION
            # -------------------------

            elif len(password) < 12:

                st.error(
                    "Password must contain at least 12 characters."
                )

            elif not re.search(r"[A-Z]", password):

                st.error(
                    "Password must contain at least one uppercase letter."
                )

            elif not re.search(r"[a-z]", password):

                st.error(
                    "Password must contain at least one lowercase letter."
                )

            elif not re.search(r"\d", password):

                st.error(
                    "Password must contain at least one number."
                )

            elif not re.search(
                r"[^A-Za-z0-9]",
                password
            ):

                st.error(
                    "Password must contain at least one special character."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                db = None
                cursor = None

                try:

                    db = get_db_connection()
                    cursor = db.cursor()

                    cursor.execute(
                        """
                        SELECT user_id
                        FROM users
                        WHERE email = %s
                        """,
                        (email,)
                    )

                    existing_user = cursor.fetchone()

                    if existing_user:

                        st.error(
                            "An account with this email already exists."
                        )

                    else:

                        hashed_password = generate_password_hash(
                            password
                        )

                        cursor.execute(
                            """
                            INSERT INTO users
                            (
                                full_name,
                                email,
                                password
                            )
                            VALUES (%s, %s, %s)
                            """,
                            (
                                full_name,
                                email,
                                hashed_password
                            )
                        )

                        db.commit()

                        user_id = cursor.lastrowid

                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.user_name = full_name

                        st.session_state.page = "dashboard"
                        st.session_state.dashboard_page = "home"

                        st.success(
                            "Account created successfully!"
                        )

                        st.rerun()

                except Exception as e:

                    st.error(
                        f"Database error: {e}"
                    )

                finally:

                    if cursor:
                        cursor.close()

                    if db:
                        db.close()

        st.write("")

        if st.button(
            "← Back to Home",
            use_container_width=True
        ):

            st.session_state.page = "landing"
            st.rerun()
# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    navbar()

    st.markdown(
        """
        <style>

        .login-wrapper {
            max-width: 400px;
            margin: 45px auto 0 auto;
        }

        .login-header {
            text-align: center;
            margin-bottom: 22px;
        }

        .login-title {
            font-size: 34px;
            font-weight: 700;
            color: white;
            margin-top: 10px;
        }

        .login-subtitle {
            color: #9fa8bd;
            font-size: 15px;
            margin-top: 6px;
        }

        .login-card {
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 18px;
            padding: 32px 30px;
            background: rgba(15, 23, 42, 0.65);
            box-shadow: 0 10px 35px rgba(212, 175, 55, 0.13);
        }

        .login-label {
            color: #d4af37;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 5px;
        }

        .login-footer {
            text-align: center;
            color: #8f98aa;
            font-size: 13px;
            margin-top: 18px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-wrapper">',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    st.markdown(
        "<h1 style='text-align:center;'>Welcome back</h1>",
        unsafe_allow_html=True
    )

    st.caption(
        "Login to continue your health journey."
    )

    # --------------------------------------------------
    # Login Card
    # --------------------------------------------------

    with st.container(
        border=True,
        key="login-card"
    ):

        with st.form("login_form"):

            email = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            st.write("")

            login = st.form_submit_button(
                "Login",
                use_container_width=True
            )

    # --------------------------------------------------
    # Login Logic
    # --------------------------------------------------

    if login:

        if not email or not password:

            st.error(
                "Please enter both email and password."
            )

        else:

            db = None
            cursor = None

            try:

                db = get_db_connection()

                cursor = db.cursor(
                    dictionary=True
                )

                cursor.execute(
                    """
                    SELECT
                        user_id,
                        full_name,
                        email,
                        password
                    FROM users
                    WHERE email = %s
                    """,
                    (email,)
                )

                user = cursor.fetchone()

                if user and check_password_hash(
                    user["password"],
                    password
                ):

                    st.session_state.logged_in = True
                    st.session_state.user_id = user["user_id"]
                    st.session_state.user_name = user["full_name"]

                    st.session_state.page = "dashboard"
                    st.session_state.dashboard_page = "home"

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )

            except Exception as e:

                st.error(
                    f"Login error: {e}"
                )

            finally:

                if cursor:
                    cursor.close()

                if db:
                    db.close()
    # --------------------------------------------------
    # Bottom Navigation Buttons
    # --------------------------------------------------

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            st.session_state.page = "signup"
            st.rerun()

    with col2:

        if st.button(
            "🔐 Admin Portal",
            use_container_width=True
        ):

            st.session_state.page = "admin_login"
            st.rerun()

    with col3:

        if st.button(
            "← Back to Home",
            use_container_width=True
        ):

            st.session_state.page = "landing"
            st.rerun()
# =========================================================
# Admin login
# =========================================================
def admin_login():

    navbar()

    st.markdown(
        """
        <style>

        .admin-login-wrapper {
            max-width: 400px;
            margin: 45px auto 0 auto;
        }

        .admin-title {
            text-align: center;
            font-size: 34px;
            font-weight: 700;
            color: white;
            margin-top: 10px;
        }

        .admin-subtitle {
            text-align: center;
            color: #9fa8bd;
            font-size: 15px;
            margin-top: 6px;
            margin-bottom: 22px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="admin-login-wrapper">',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    st.markdown(
        "<h1 class='admin-title'>🔐 Admin Portal</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='admin-subtitle'>Administrator access</div>",
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Admin Login Form
    # --------------------------------------------------

    with st.container(
        border=True,
        key="admin-login-card"
    ):

        with st.form("admin_login_form"):

            email = st.text_input(
                "Admin Email",
                placeholder="Enter admin email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter admin password"
            )

            st.write("")

            login = st.form_submit_button(
                "Admin Login",
                use_container_width=True
            )

    # --------------------------------------------------
    # Login Logic
    # --------------------------------------------------

    if login:

        if not email or not password:

            st.error(
                "Please enter both email and password."
            )

        else:

            db = None
            cursor = None

            try:

                db = get_db_connection()

                cursor = db.cursor(
                    dictionary=True
                )

                cursor.execute(
                    """
                    SELECT
                        admin_id,
                        admin_name,
                        email,
                        password
                    FROM admins
                    WHERE email = %s
                    """,
                    (email,)
                )

                admin = cursor.fetchone()

                if admin and check_password_hash(
                    admin["password"],
                    password
                ):

                    st.session_state.admin_logged_in = True
                    st.session_state.admin_id = admin["admin_id"]
                    st.session_state.admin_name = admin["admin_name"]
                    st.session_state.admin_email = admin["email"]

                    st.session_state.page = "admin_dashboard"

                    st.success(
                        "Admin login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid admin email or password."
                    )

            except Exception as e:

                st.error(
                    f"Admin login error: {e}"
                )

            finally:

                if cursor:
                    cursor.close()

                if db:
                    db.close()

    # --------------------------------------------------
    # Back Buttons
    # --------------------------------------------------

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← User Login",
            use_container_width=True
        ):

            st.session_state.page = "login"
            st.rerun()

    with col2:

        if st.button(
            "← Back to Home",
            use_container_width=True
        ):

            st.session_state.page = "landing"
            st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =========================================================
# Admin dashboard
# =========================================================
def admin_dashboard():

    # ---------------------------------------------------------
    # ADMIN ACCESS CHECK
    # ---------------------------------------------------------
    if not st.session_state.get("admin_logged_in", False):
        st.session_state.page = "admin_login"
        st.rerun()

    # ---------------------------------------------------------
    # PAGE STYLING
    # ---------------------------------------------------------
    st.markdown(
        """
        <style>

        .admin-header {
            padding-top: 8px;
            margin-bottom: 25px;
        }

        .admin-title {
            font-size: 36px;
            font-weight: 700;
            color: white;
            margin: 0;
            padding: 0;
        }

        .admin-subtitle {
            color: #9fa8bd;
            font-size: 15px;
            margin-top: 6px;
        }

        .admin-welcome {
            color: #d4af37;
            font-size: 15px;
            margin-top: 5px;
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 650;
            color: white;
            margin-top: 20px;
            margin-bottom: 15px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------------------------------------
    # ADMIN HEADER WITH LOGO
    # ---------------------------------------------------------
    logo_col, title_col = st.columns(
            [0.13, 0.87],
            vertical_alignment="center"
        )

    with logo_col:

        st.image(
            "Logo.png",
            width=78
        )

    with title_col:

        st.markdown(
            "<div class='admin-title'>Admin Dashboard</div>",
            unsafe_allow_html=True
        )

    st.markdown(
                "<div class='admin-subtitle'>"
                "Manage users, assessments and family health records."
                "</div>",
                unsafe_allow_html=True
            )

    # ---------------------------------------------------------
    # WELCOME MESSAGE
    # ---------------------------------------------------------
    st.markdown(
        f"""
        <div class="admin-welcome">
            Welcome, <strong>
            {st.session_state.get("admin_name", "Administrator")}
            </strong>
        </div>
        """,
        unsafe_allow_html=True
    )

    db = None
    cursor = None

    try:

        # -----------------------------------------------------
        # DATABASE CONNECTION
        # -----------------------------------------------------
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # -----------------------------------------------------
        # TOTAL REGISTERED USERS
        # -----------------------------------------------------
        cursor.execute(
            """
            SELECT COUNT(*) AS total_users
            FROM users
            """
        )

        total_users = cursor.fetchone()["total_users"]

        # -----------------------------------------------------
        # TOTAL ASSESSMENTS
        # -----------------------------------------------------
        cursor.execute(
            """
            SELECT COUNT(*) AS total_predictions
            FROM assessments
            """
        )

        total_predictions = cursor.fetchone()["total_predictions"]

        # -----------------------------------------------------
        # DIABETES RISK
        # -----------------------------------------------------
        cursor.execute(
            """
            SELECT COUNT(*) AS diabetes_risk
            FROM assessments
            WHERE prediction = 1
            """
        )

        diabetes_risk = cursor.fetchone()["diabetes_risk"]

        # -----------------------------------------------------
        # LOWER RISK
        # -----------------------------------------------------
        cursor.execute(
            """
            SELECT COUNT(*) AS lower_risk
            FROM assessments
            WHERE prediction = 0
            """
        )

        lower_risk = cursor.fetchone()["lower_risk"]

        # -----------------------------------------------------
        # TOTAL FAMILY MEMBERS
        # -----------------------------------------------------
        cursor.execute(
            """
            SELECT COUNT(*) AS total_family_members
            FROM family_members
            """
        )

        total_family_members = cursor.fetchone()["total_family_members"]

        # -----------------------------------------------------
        # TODAY'S ASSESSMENTS
        # -----------------------------------------------------
        cursor.execute(
            """
            SELECT COUNT(*) AS today_predictions
            FROM assessments
            WHERE DATE(created_at) = CURDATE()
            """
        )

        today_predictions = cursor.fetchone()["today_predictions"]

        # -----------------------------------------------------
        # AVERAGE RISK PROBABILITY
        # -----------------------------------------------------
        cursor.execute(
            """
            SELECT AVG(risk_probability) AS average_probability
            FROM assessments
            WHERE risk_probability IS NOT NULL
            """
        )

        average_probability = cursor.fetchone()["average_probability"]

        if average_probability is None:
            average_probability = 0

        # IMPORTANT:
        # Your database values are already percentage values.
        # Therefore we do NOT multiply by 100 here.
        average_probability = float(average_probability)

        # -----------------------------------------------------
        # SYSTEM OVERVIEW
        # -----------------------------------------------------
        st.markdown(
            '<div class="section-title">System Overview</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Registered Users",
                total_users
            )

        with col2:

            st.metric(
                "Total Assessments",
                total_predictions
            )

        with col3:

            st.metric(
                "Family Members",
                total_family_members
            )

        col4, col5, col6 = st.columns(3)

        with col4:

            st.metric(
                "Diabetes Risk",
                diabetes_risk
            )

        with col5:

            st.metric(
                "Lower Risk",
                lower_risk
            )

        with col6:

            st.metric(
                "Today's Assessments",
                today_predictions
            )

        st.write("")

        # -----------------------------------------------------
        # AVERAGE RISK
        # -----------------------------------------------------
        st.metric(
            "Average Risk Probability",
            f"{average_probability:.2f}%"
        )

        # -----------------------------------------------------
        # ASSESSMENT ANALYTICS
        # -----------------------------------------------------
        st.markdown(
            '<div class="section-title">Assessment Analytics</div>',
            unsafe_allow_html=True
        )

        analytics_col1, analytics_col2 = st.columns(2)

        # -----------------------------------------------------
        # RISK CHART
        # -----------------------------------------------------
        with analytics_col1:

            risk_data = {
                "Risk Level": [
                    "Diabetes Risk",
                    "Lower Risk"
                ],
                "Assessments": [
                    diabetes_risk,
                    lower_risk
                ]
            }

            risk_df = pd.DataFrame(risk_data)

            st.bar_chart(
                risk_df.set_index("Risk Level")
            )

        # -----------------------------------------------------
        # ASSESSMENT SUMMARY
        # -----------------------------------------------------
        with analytics_col2:

            st.write("### Assessment Summary")

            if total_predictions > 0:

                diabetes_percentage = (
                    diabetes_risk /
                    total_predictions
                ) * 100

                lower_percentage = (
                    lower_risk /
                    total_predictions
                ) * 100

                st.write(
                    f"**Diabetes Risk:** "
                    f"{diabetes_percentage:.2f}%"
                )

                st.progress(
                    diabetes_percentage / 100
                )

                st.write(
                    f"**Lower Risk:** "
                    f"{lower_percentage:.2f}%"
                )

                st.progress(
                    lower_percentage / 100
                )

            else:

                st.info(
                    "No assessment data available yet."
                )

        # -----------------------------------------------------
        # MANAGEMENT SECTION
        # -----------------------------------------------------
        st.markdown(
            '<div class="section-title">Management</div>',
            unsafe_allow_html=True
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "Users",
                "Assessments",
                "Family Members"
            ]
        )

        # =====================================================
        # USERS TAB
        # =====================================================
        with tab1:

            st.subheader("Registered Users")

            cursor.execute(
                """
                SELECT
                    user_id,
                    full_name,
                    email,
                    created_at
                FROM users
                ORDER BY created_at DESC
                """
            )

            users = cursor.fetchall()

            if users:

                st.dataframe(
                    users,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No registered users found."
                )

        # =====================================================
        # ASSESSMENTS TAB
        # =====================================================
        with tab2:

            st.subheader("Assessment Records")

            cursor.execute(
                """
                SELECT
                    a.assessment_id,
                    u.full_name AS user_name,
                    u.email,
                    fm.name AS family_member,
                    a.age,
                    a.gender,
                    a.bmi,
                    a.hba1c,
                    a.blood_glucose,
                    a.hypertension,
                    a.heart_disease,
                    a.smoking_history,
                    a.prediction,
                    a.risk_probability,
                    a.created_at

                FROM assessments a

                INNER JOIN users u
                    ON a.user_id = u.user_id

                LEFT JOIN family_members fm
                    ON a.member_id = fm.member_id

                ORDER BY a.created_at DESC
                """
            )

            assessments = cursor.fetchall()

            if assessments:

                for assessment in assessments:

                    # Convert prediction value
                    if assessment["prediction"] == 1:

                        assessment["prediction"] = (
                            "Diabetes Risk"
                        )

                    else:

                        assessment["prediction"] = (
                            "Lower Risk"
                        )

                    # Convert risk probability
                    if assessment["risk_probability"] is not None:

                        assessment["risk_probability"] = (
                            f"{float(assessment['risk_probability']):.2f}%"
                        )

                st.dataframe(
                    assessments,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No assessment records found."
                )

        # =====================================================
        # FAMILY MEMBERS TAB
        # =====================================================
        with tab3:

            st.subheader("Family Members")

            cursor.execute(
                """
                SELECT
                    fm.member_id,
                    fm.name AS family_member,
                    u.full_name AS account_owner,
                    u.email,
                    fm.created_at

                FROM family_members fm

                INNER JOIN users u
                    ON fm.user_id = u.user_id

                ORDER BY fm.created_at DESC
                """
            )

            family_members = cursor.fetchall()

            if family_members:

                st.dataframe(
                    family_members,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No family members found."
                )

    except Exception as e:

        st.error(
            f"Admin dashboard error: {e}"
        )

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()

    # ---------------------------------------------------------
    # ADMIN LOGOUT
    # ---------------------------------------------------------
    st.write("")
    st.write("")

    if st.button(
        "Logout",
        use_container_width=True,
        key="admin_logout_button"
    ):

        st.session_state.admin_logged_in = False
        st.session_state.admin_id = None
        st.session_state.admin_name = None
        st.session_state.admin_email = None
        st.session_state.page = "landing"

        st.rerun()
# =========================================================
# Profile PAGE
# =========================================================
def profile_page():

    st.title("Profile")
    st.caption("Manage your account and personal information.")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            user_id,
            full_name,
            email,
            profile_photo,
            created_at
        FROM users
        WHERE user_id = %s
    """, (st.session_state.user_id,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        st.error("Profile could not be loaded.")
        return

    import os
    import base64
    from io import BytesIO

    def image_to_base64(image):

        image = ImageOps.exif_transpose(image)

        if image.mode != "RGB":
            image = image.convert("RGB")

        buffer = BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=100,
            subsampling=0
        )

        return base64.b64encode(
            buffer.getvalue()
        ).decode()

    # -----------------------------
    # Profile Header
    # -----------------------------

    profile_image = None

    if user["profile_photo"]:

        if os.path.exists(user["profile_photo"]):

            try:
                saved_image = Image.open(
                    user["profile_photo"]
                )

                profile_image = image_to_base64(
                    saved_image
                )

            except Exception:
                profile_image = None

    photo_html = ""

    if profile_image:

        photo_html = f"""
        <img
            src="data:image/jpeg;base64,{profile_image}"
            style="
                width:170px;
                height:170px;
                object-fit:cover;
                border-radius:50%;
                border:4px solid #d4af37;
                display:block;
            "
        >
        """

    else:

        photo_html = """
        <div style="
            width:170px;
            height:170px;
            border-radius:50%;
            border:4px solid #d4af37;
            background:#16213e;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:60px;
        ">
            👤
        </div>
        """

    profile_col1, profile_col2 = st.columns(
        [1, 2.5],
        vertical_alignment="center"
    )

    with profile_col1:

        if profile_image:

            st.html(
                f"""
                <div style="
                    display:flex;
                    justify-content:center;
                    align-items:center;
                ">
                    <img
                        src="data:image/jpeg;base64,{profile_image}"
                        style="
                            width:170px;
                            height:170px;
                            object-fit:cover;
                            border-radius:50%;
                            border:4px solid #d4af37;
                        "
                    >
                </div>
                """
            )

        else:

            st.html(
                """
                <div style="
                    width:170px;
                    height:170px;
                    border-radius:50%;
                    border:4px solid #d4af37;
                    background:#16213e;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:60px;
                    margin:auto;
                ">
                    👤
                </div>
                """
            )

    with profile_col2:

        st.html(
            f"""
            <div style="
                padding:10px 0 5px 0;
            ">

                <div style="
                    font-size:30px;
                    font-weight:700;
                    color:white;
                    margin-bottom:8px;
                ">
                    {user["full_name"]}
                </div>

                <div style="
                    font-size:16px;
                    color:#b8c0d9;
                    margin-bottom:8px;
                ">
                    {user["email"]}
                </div>

                <div style="
                    font-size:14px;
                    color:#8f98b3;
                ">
                    Member since
                    {user["created_at"].strftime("%d %B %Y")}
                </div>

            </div>
            """
        )

        st.write("")

        new_photo = st.file_uploader(
            "Change Photo",
            type=["jpg", "jpeg", "png"],
            key="profile_photo_upload"
        )

    # -----------------------------
# New Photo Preview
# -----------------------------

    if new_photo is not None:

        preview_image = Image.open(new_photo)

        preview_image = ImageOps.exif_transpose(
            preview_image
        )

        preview_base64 = image_to_base64(
            preview_image
        )

        st.html(
            f"""
            <div style="
                display:flex;
                align-items:center;
                gap:20px;
                margin-top:10px;
                padding:15px 20px;
                background:rgba(22,33,62,0.65);
                border:1px solid rgba(212,175,55,0.35);
                border-radius:15px;
            ">

                <img
                    src="data:image/jpeg;base64,{preview_base64}"
                    style="
                        width:80px;
                        height:80px;
                        object-fit:cover;
                        border-radius:50%;
                        border:2px solid #d4af37;
                    "
                >

                <div>
                    <div style="
                        color:white;
                        font-size:16px;
                        font-weight:600;
                    ">
                        New profile photo selected
                    </div>

                    <div style="
                        color:#9fa8c0;
                        font-size:13px;
                        margin-top:4px;
                    ">
                        Your photo will be saved when you click
                        Save Changes.
                    </div>
                </div>

            </div>
            """
        )
    # -----------------------------
    # Personal Information
    # -----------------------------

    st.subheader("Personal Information")

    new_name = st.text_input(
        "Full Name",
        value=user["full_name"],
        key="profile_full_name"
    )

    st.text_input(
        "Email",
        value=user["email"],
        disabled=True,
        key="profile_email"
    )

    st.write("")

    # -----------------------------
    # Save Changes
    # -----------------------------

    if st.button(
        "Save Changes",
        type="primary",
        use_container_width=True
    ):

        new_name = new_name.strip()

        if not new_name:
            st.error("Full name cannot be empty.")
            return

        profile_photo_path = user["profile_photo"]

        if new_photo is not None:

            upload_folder = os.path.join(
                "static",
                "uploads",
                "profile"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            file_path = os.path.join(
                upload_folder,
                f"user_{st.session_state.user_id}.jpg"
            )

            image = Image.open(new_photo)

            image = ImageOps.exif_transpose(
                image
            )

            if image.mode != "RGB":
                image = image.convert("RGB")

            image.save(
                file_path,
                "JPEG",
                quality=100,
                subsampling=0
            )

            profile_photo_path = file_path.replace(
                "\\",
                "/"
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET
                full_name = %s,
                profile_photo = %s
            WHERE user_id = %s
            """,
            (
                new_name,
                profile_photo_path,
                st.session_state.user_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        st.session_state.user_name = new_name

        st.success("Profile updated successfully.")

        st.rerun()

    st.divider()

    # -----------------------------
    # Account Information
    # -----------------------------

    st.subheader("Account Information")

    st.info(
        "Your health assessments, family assessment records, "
        "progress data, reminders and reports are linked to this account."
    )
# =========================================================
# DASHBOARD HOME
# =========================================================

def dashboard_home():

    show_dashboard_reminders()


    st.markdown(
        f"# Welcome, {st.session_state.get('user_name', 'User')}"
    )

    st.caption(
        "Your personal space to assess, understand and track your health."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.markdown("### 🩺")
            st.markdown("**Assessment**")
            st.caption(
                "Create a new health assessment."
            )

    with col2:

        with st.container(border=True):

            st.markdown("### 👤")
            st.markdown("**My Assessment**")
            st.caption(
                "View your previous assessments."
            )

    with col3:

        with st.container(border=True):

            st.markdown("### 👨‍👩‍👧")
            st.markdown("**Family Members**")
            st.caption(
                "View assessments for your family."
            )

    st.write("")

    col4, col5, col6 = st.columns(3)

    with col4:

        with st.container(border=True):

            st.markdown("### 📊")
            st.markdown("**Analytics**")
            st.caption(
                "Understand your health data."
            )

    with col5:

        with st.container(border=True):

            st.markdown("### 📈")
            st.markdown("**Progress**")
            st.caption(
                "Track health measurements over time."
            )

    with col6:

        with st.container(border=True):

            st.markdown("### 📚")
            st.markdown("**Health Knowledge**")
            st.caption(
                "Learn about diabetes and healthy habits."
            )


# =========================================================
# DASHBOARD PAGE
# =========================================================

def dashboard_page():

    dashboard_sidebar()

    if st.session_state.dashboard_page == "assessment":

        assessment_page()
        return

    if st.session_state.dashboard_page == "my_assessment":

        my_assessment_page()
        return

    if st.session_state.dashboard_page == "family":

        family_members_page()
        return

    if st.session_state.dashboard_page == "family_history":

        family_history_page()
        return

    if st.session_state.dashboard_page == "analytics":

        analytics_page()
        return


    if st.session_state.dashboard_page == "progress":

        progress_page()
        return

    if st.session_state.dashboard_page == "reminders":

        reminders_page()
        return

    if st.session_state.dashboard_page == "knowledge":

        health_knowledge_page()
        return

    if st.session_state.dashboard_page == "reports":
        reports_page()
        return

    if st.session_state.dashboard_page == "profile":
        profile_page()
        return
    
    dashboard_home()

# =========================================================
# ASSESSMENT PAGE
# =========================================================

def assessment_page():

    st.markdown("# 🩺 Assessment")

    st.caption(
        "Enter the person's health information to receive "
        "a machine-learning-based diabetes risk assessment."
    )

    st.divider()


    # =====================================================
    # PERSON INFORMATION
    # =====================================================

    with st.container(border=True):

        st.markdown("### Person Information")

        person_name = st.text_input(
            "Name",
            value=st.session_state.user_name,
            placeholder="Enter the person's name"
        )

    st.write("")

    # =====================================================
    # HEALTH INFORMATION
    # =====================================================

    with st.container(border=True):

        st.markdown("### Personal & Health Information")

        col1, col2 = st.columns(2)

        with col1:

            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=25
            )

            gender = st.selectbox(
                "Gender",
                [
                    "Select",
                    "Female",
                    "Male"
                ]
            )

            bmi = st.number_input(
                "BMI",
                min_value=1.0,
                max_value=80.0,
                value=25.0,
                step=0.1
            )

            hba1c = st.number_input(
                "HbA1c Level (%)",
                min_value=1.0,
                max_value=20.0,
                value=5.5,
                step=0.1
            )

        with col2:

            glucose = st.number_input(
                "Blood Glucose Level (mg/dL)",
                min_value=1,
                max_value=500,
                value=100
            )

            hypertension = st.selectbox(
                "Hypertension",
                [
                    "No",
                    "Yes"
                ]
            )

            heart_disease = st.selectbox(
                "Heart Disease",
                [
                    "No",
                    "Yes"
                ]
            )

            smoking_history = st.selectbox(
                "Smoking History",
                [
                    "Never",
                    "No Info",
                    "Current",
                    "Former",
                    "Ever",
                    "Not Current"
                ]
            )


    st.write("")

    # =====================================================
    # ASSESS BUTTON
    # =====================================================

    if st.button(
        "🔮 Assess Diabetes Risk",
        use_container_width=True
    ):

        # =================================================
        # VALIDATION
        # =================================================

        person_name = person_name.strip()

        if not person_name:

            st.warning(
                "Please enter the person's name."
            )

            return

        if gender == "Select":

            st.warning(
                "Please select the person's gender."
            )

            return


        # =================================================
        # IDENTIFY PERSON
        # =================================================

        member_id = None

        logged_in_name = (
            st.session_state.user_name.strip()
        )


        # =================================================
        # PERSONAL ASSESSMENT
        # =================================================

        if person_name.lower() == logged_in_name.lower():

            member_id = None


        # =================================================
        # FAMILY MEMBER ASSESSMENT
        # =================================================

        else:

            db = None
            cursor = None

            try:

                db = get_db_connection()

                cursor = db.cursor(
                    dictionary=True
                )

                cursor.execute(
                    """
                    SELECT member_id
                    FROM family_members
                    WHERE user_id = %s
                    AND LOWER(name) = LOWER(%s)
                    LIMIT 1
                    """,
                    (
                        st.session_state.user_id,
                        person_name
                    )
                )

                existing_member = cursor.fetchone()


                if existing_member:

                    member_id = (
                        existing_member["member_id"]
                    )


                else:

                    cursor.execute(
                        """
                        INSERT INTO family_members
                        (
                            user_id,
                            name
                        )
                        VALUES
                        (
                            %s,
                            %s
                        )
                        """,
                        (
                            st.session_state.user_id,
                            person_name
                        )
                    )

                    member_id = cursor.lastrowid

                    db.commit()


            except Exception as e:

                st.error(
                    f"Could not identify the person: {e}"
                )

                return

            finally:

                if cursor is not None:
                    cursor.close()

                if db is not None:
                    db.close()


        # =================================================
        # ENCODING
        # =================================================

        gender_value = (
            1
            if gender == "Male"
            else 0
        )

        hypertension_value = (
            1
            if hypertension == "Yes"
            else 0
        )

        heart_disease_value = (
            1
            if heart_disease == "Yes"
            else 0
        )


        smoking_history_map = {

            "Never": 0,
            "No Info": 1,
            "Current": 2,
            "Former": 3,
            "Ever": 4,
            "Not Current": 5

        }

        smoking_value = (
            smoking_history_map[
                smoking_history
            ]
        )


        # =================================================
        # MODEL INPUT
        # =================================================

        data = np.array(
            [[
                gender_value,
                age,
                hypertension_value,
                heart_disease_value,
                smoking_value,
                bmi,
                hba1c,
                glucose
            ]]
        )


        # =================================================
        # PREDICTION
        # =================================================

        try:

            prediction = model.predict(data)

            probability = model.predict_proba(data)

            class_index = list(
                model.classes_
            ).index(1)

            risk = (
                probability[0][class_index]
                * 100
            )

        except Exception as e:

            st.error(
                f"Prediction error: {e}"
            )

            return


        # =================================================
        # SAVE ASSESSMENT
        # =================================================

        db = None
        cursor = None

        try:

            db = get_db_connection()

            cursor = db.cursor()

            cursor.execute(
                """
                INSERT INTO assessments
                (
                    user_id,
                    member_id,
                    age,
                    gender,
                    bmi,
                    hba1c,
                    blood_glucose,
                    hypertension,
                    heart_disease,
                    smoking_history,
                    prediction,
                    risk_probability
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    st.session_state.user_id,
                    member_id,
                    age,
                    gender,
                    bmi,
                    hba1c,
                    glucose,
                    hypertension_value,
                    heart_disease_value,
                    smoking_history,
                    int(prediction[0]),
                    risk
                )
            )

            db.commit()

        except Exception as e:

            st.error(
                f"Could not save assessment: {e}"
            )

            return

        finally:

            if cursor is not None:
                cursor.close()

            if db is not None:
                db.close()


        # =================================================
        # RESULT
        # =================================================

        st.divider()

        st.markdown(
            f"## Assessment Result — {person_name}"
        )

        result_col1, result_col2 = st.columns(2)

        with result_col1:

            st.metric(
                "Estimated Diabetes Risk",
                f"{risk:.1f}%"
            )

        with result_col2:

            if risk < 30:

                st.success(
                    "Lower estimated risk"
                )

            elif risk < 70:

                st.warning(
                    "Elevated estimated risk"
                )

            else:

                st.error(
                    "Higher estimated risk"
                )


        st.info(
            "This is a machine-learning-based risk assessment, "
            "not a medical diagnosis. If you are concerned about "
            "your health or measurements, consult a qualified "
            "healthcare professional."
        )


# =========================================================
# MY ASSESSMENT PAGE
# =========================================================

def my_assessment_page():

    st.title("👤 My Assessment")

    st.caption(
        "Your personal health assessment history."
    )

    if st.button("← Back to Dashboard"):

        st.session_state.dashboard_page = "home"
        st.rerun()

    st.divider()

    db = None
    cursor = None

    try:

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                assessment_id,
                age,
                gender,
                bmi,
                hba1c,
                blood_glucose,
                hypertension,
                heart_disease,
                smoking_history,
                prediction,
                risk_probability,
                created_at
            FROM assessments
            WHERE user_id = %s
            AND member_id IS NULL
            ORDER BY created_at DESC
            """,
            (
                st.session_state.user_id,
            )
        )

        history = cursor.fetchall()

        if not history:

            st.info(
                "You don't have any personal assessments yet."
            )

            return


        for assessment in history:

            date_text = (
                assessment["created_at"]
                .strftime(
                    "%d %b %Y, %I:%M %p"
                )
            )

            risk = float(
                assessment["risk_probability"]
            )

            if risk < 30:

                risk_text = "Lower estimated risk"

            elif risk < 70:

                risk_text = "Elevated estimated risk"

            else:

                risk_text = "Higher estimated risk"


            with st.container(border=True):

                st.markdown(
                    f"### Assessment — {date_text}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"**Age:** {assessment['age']}"
                    )

                    st.write(
                        f"**Gender:** {assessment['gender']}"
                    )

                    st.write(
                        f"**BMI:** {assessment['bmi']}"
                    )

                with col2:

                    st.write(
                        f"**HbA1c:** {assessment['hba1c']}"
                    )

                    st.write(
                        f"**Blood Glucose:** "
                        f"{assessment['blood_glucose']}"
                    )

                    st.write(
                        f"**Hypertension:** "
                        f"{'Yes' if assessment['hypertension'] else 'No'}"
                    )

                with col3:

                    st.write(
                        f"**Heart Disease:** "
                        f"{'Yes' if assessment['heart_disease'] else 'No'}"
                    )

                    st.write(
                        f"**Smoking History:** "
                        f"{assessment['smoking_history']}"
                    )

                    st.write(
                        f"**Result:** {risk_text}"
                    )

                st.metric(
                    "Estimated Risk Probability",
                    f"{risk:.1f}%"
                )


    except Exception as e:

        st.error(
            f"Could not load your assessment history: {e}"
        )

    finally:

        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()


# =========================================================
# FAMILY MEMBERS ASSESSMENT PAGE
# =========================================================

def family_members_page():

    st.title("👨‍👩‍👧 Family Members Assessment")

    st.caption(
        "People whose health information you are tracking."
    )

    if st.button("← Back to Dashboard"):

        st.session_state.dashboard_page = "home"
        st.rerun()

    st.divider()

    db = None
    cursor = None

    try:

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                member_id,
                name
            FROM family_members
            WHERE user_id = %s
            ORDER BY created_at ASC
            """,
            (
                st.session_state.user_id,
            )
        )

        members = cursor.fetchall()


        if not members:

            st.info(
                "No family members have been assessed yet."
            )

            return


        for member in members:

            with st.container(border=True):

                col1, col2 = st.columns(
                    [3, 1]
                )

                with col1:

                    st.markdown(
                        f"### 👤 {member['name']}"
                    )

                    st.caption(
                        "View health assessment history"
                    )

                with col2:

                    if st.button(
                        "View History →",
                        key=(
                            f"history_"
                            f"{member['member_id']}"
                        )
                    ):

                        st.session_state.selected_member_id = (
                            member["member_id"]
                        )

                        st.session_state.selected_member_name = (
                            member["name"]
                        )

                        st.session_state.dashboard_page = (
                            "family_history"
                        )

                        st.rerun()


    except Exception as e:

        st.error(
            f"Could not load family members: {e}"
        )

    finally:

        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()


# =========================================================
# FAMILY HISTORY PAGE
# =========================================================

def family_history_page():

    member_id = (
        st.session_state.get(
            "selected_member_id"
        )
    )

    member_name = (
        st.session_state.get(
            "selected_member_name",
            "Family Member"
        )
    )


    if st.button("← Back to Family Members"):

        st.session_state.dashboard_page = "family"
        st.rerun()


    if not member_id:

        st.warning(
            "Please select a family member first."
        )

        return


    st.title(
        f"👤 {member_name}"
    )

    st.caption(
        "Health assessment history"
    )

    st.divider()

    db = None
    cursor = None

    try:

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                assessment_id,
                age,
                gender,
                bmi,
                hba1c,
                blood_glucose,
                hypertension,
                heart_disease,
                smoking_history,
                prediction,
                risk_probability,
                created_at
            FROM assessments
            WHERE user_id = %s
            AND member_id = %s
            ORDER BY created_at DESC
            """,
            (
                st.session_state.user_id,
                member_id
            )
        )

        history = cursor.fetchall()


        if not history:

            st.info(
                "No health assessment history found."
            )

            return


        for assessment in history:

            date_text = (
                assessment["created_at"]
                .strftime(
                    "%d %b %Y, %I:%M %p"
                )
            )

            risk = float(
                assessment["risk_probability"]
            )

            if risk < 30:

                risk_text = (
                    "Lower estimated risk"
                )

            elif risk < 70:

                risk_text = (
                    "Elevated estimated risk"
                )

            else:

                risk_text = (
                    "Higher estimated risk"
                )


            with st.container(border=True):

                st.markdown(
                    f"### Assessment — {date_text}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"**Age:** {assessment['age']}"
                    )

                    st.write(
                        f"**Gender:** {assessment['gender']}"
                    )

                    st.write(
                        f"**BMI:** {assessment['bmi']}"
                    )

                with col2:

                    st.write(
                        f"**HbA1c:** "
                        f"{assessment['hba1c']}"
                    )

                    st.write(
                        f"**Blood Glucose:** "
                        f"{assessment['blood_glucose']}"
                    )

                    st.write(
                        f"**Hypertension:** "
                        f"{'Yes' if assessment['hypertension'] else 'No'}"
                    )

                with col3:

                    st.write(
                        f"**Heart Disease:** "
                        f"{'Yes' if assessment['heart_disease'] else 'No'}"
                    )

                    st.write(
                        f"**Smoking History:** "
                        f"{assessment['smoking_history']}"
                    )

                    st.write(
                        f"**Result:** {risk_text}"
                    )

                st.metric(
                    "Estimated Risk Probability",
                    f"{risk:.1f}%"
                )


    except Exception as e:

        st.error(
            f"Could not load health history: {e}"
        )

    finally:

        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()

# =========================================================
# ANALYTICS
# =========================================================

def style_analytics_chart(fig, height=450):

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    return fig


# =========================================================
# GET PERSONAL ANALYTICS DATA
# =========================================================

def get_personal_analytics_data():

    db = None
    cursor = None

    try:

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                assessment_id,
                age,
                gender,
                bmi,
                hba1c,
                blood_glucose,
                hypertension,
                heart_disease,
                smoking_history,
                prediction,
                risk_probability,
                created_at
            FROM assessments
            WHERE user_id = %s
            AND member_id IS NULL
            ORDER BY created_at ASC
            """,
            (
                st.session_state.user_id,
            )
        )

        records = cursor.fetchall()

        return pd.DataFrame(records)

    except Exception as e:

        st.error(
            f"Could not load personal analytics data: {e}"
        )

        return pd.DataFrame()

    finally:

        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()


# =========================================================
# GET FAMILY ANALYTICS DATA
# =========================================================

def get_family_analytics_data():

    db = None
    cursor = None

    try:

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                a.assessment_id,
                fm.name AS member_name,
                a.age,
                a.gender,
                a.bmi,
                a.hba1c,
                a.blood_glucose,
                a.hypertension,
                a.heart_disease,
                a.smoking_history,
                a.prediction,
                a.risk_probability,
                a.created_at
            FROM assessments a

            INNER JOIN family_members fm
                ON a.member_id = fm.member_id

            WHERE a.user_id = %s
            AND a.member_id IS NOT NULL

            ORDER BY a.created_at ASC
            """,
            (
                st.session_state.user_id,
            )
        )

        records = cursor.fetchall()

        return pd.DataFrame(records)

    except Exception as e:

        st.error(
            f"Could not load family analytics data: {e}"
        )

        return pd.DataFrame()

    finally:

        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()


# =========================================================
# PERSONAL ANALYTICS
# =========================================================

def personal_analytics():

    st.markdown("## 👤 Personal Analytics")

    st.caption(
        "Track your saved assessment results and health measurements over time."
    )

    df = get_personal_analytics_data()

    if df.empty:

        st.info(
            "You need at least one personal assessment "
            "before personal analytics can be displayed."
        )

        return


    # =====================================================
    # PREPARE DATA
    # =====================================================

    df["created_at"] = pd.to_datetime(
        df["created_at"]
    )

    df["prediction_label"] = df["prediction"].map(
        {
            0: "Non-Diabetic",
            1: "Diabetic"
        }
    )


    # =====================================================
    # OVERVIEW
    # =====================================================

    st.markdown("### 📌 Overview")

    total = len(df)

    diabetic = int(
        (df["prediction"] == 1).sum()
    )

    non_diabetic = int(
        (df["prediction"] == 0).sum()
    )

    avg_bmi = df["bmi"].mean()

    avg_glucose = df["blood_glucose"].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Total Assessments",
            total
        )

    with col2:

        st.metric(
            "Diabetic Predictions",
            diabetic
        )

    with col3:

        st.metric(
            "Non-Diabetic",
            non_diabetic
        )

    with col4:

        st.metric(
            "Average BMI",
            f"{avg_bmi:.1f}"
        )

    with col5:

        st.metric(
            "Average Glucose",
            f"{avg_glucose:.1f}"
        )


    st.divider()


    # =====================================================
    # RISK OVER TIME
    # =====================================================

    st.markdown("### 📈 Risk Over Time")

    fig = px.line(
        df,
        x="created_at",
        y="risk_probability",
        markers=True,
        labels={
            "created_at": "Assessment Date",
            "risk_probability": "Estimated Risk (%)"
        }
    )

    fig.update_traces(
        line_width=3,
        marker_size=8
    )

    fig.update_yaxes(
        range=[0, 100]
    )

    fig = style_analytics_chart(
        fig,
        450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # BMI TREND
    # =====================================================

    st.markdown("### ⚖️ BMI Trend")

    fig = px.line(
        df,
        x="created_at",
        y="bmi",
        markers=True,
        labels={
            "created_at": "Assessment Date",
            "bmi": "BMI"
        }
    )

    fig.update_traces(
        line_width=3,
        marker_size=8
    )

    fig = style_analytics_chart(
        fig,
        400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # BLOOD GLUCOSE TREND
    # =====================================================

    st.markdown("### 🩸 Blood Glucose Trend")

    fig = px.line(
        df,
        x="created_at",
        y="blood_glucose",
        markers=True,
        labels={
            "created_at": "Assessment Date",
            "blood_glucose": "Blood Glucose (mg/dL)"
        }
    )

    fig.update_traces(
        line_width=3,
        marker_size=8
    )

    fig = style_analytics_chart(
        fig,
        400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # HbA1c TREND
    # =====================================================

    st.markdown("### 💉 HbA1c Trend")

    fig = px.line(
        df,
        x="created_at",
        y="hba1c",
        markers=True,
        labels={
            "created_at": "Assessment Date",
            "hba1c": "HbA1c (%)"
        }
    )

    fig.update_traces(
        line_width=3,
        marker_size=8
    )

    fig = style_analytics_chart(
        fig,
        400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # RESULT DISTRIBUTION
    # =====================================================

    st.markdown(
        "### 🩺 Assessment Result Distribution"
    )

    result_count = (
        df["prediction_label"]
        .value_counts()
    )

    fig = px.pie(
        names=result_count.index,
        values=result_count.values,
        hole=0.45
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    fig = style_analytics_chart(
        fig,
        400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # HEALTH FACTORS
    # =====================================================

    st.markdown("### ❤️ Health Factors")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### 🩺 Hypertension")

        hypertension_count = (
            df["hypertension"]
            .map(
                {
                    0: "No Hypertension",
                    1: "Hypertension"
                }
            )
            .value_counts()
        )

        fig = px.bar(
            x=hypertension_count.index,
            y=hypertension_count.values,
            labels={
                "x": "Hypertension",
                "y": "Assessments"
            },
            text=hypertension_count.values
        )

        fig.update_traces(
            textposition="outside"
        )

        fig = style_analytics_chart(
            fig,
            400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.markdown("#### ❤️ Heart Disease")

        heart_count = (
            df["heart_disease"]
            .map(
                {
                    0: "No Heart Disease",
                    1: "Heart Disease"
                }
            )
            .value_counts()
        )

        fig = px.bar(
            x=heart_count.index,
            y=heart_count.values,
            labels={
                "x": "Heart Disease",
                "y": "Assessments"
            },
            text=heart_count.values
        )

        fig.update_traces(
            textposition="outside"
        )

        fig = style_analytics_chart(
            fig,
            400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# FAMILY ANALYTICS
# =========================================================

def family_analytics():

    st.markdown("## 👨‍👩‍👧 Family Analytics")

    st.caption(
        "Track assessment history and health trends for your family members."
    )

    df = get_family_analytics_data()

    if df.empty:

        st.info(
            "No family member assessments are available yet."
        )

        return


    # =====================================================
    # PREPARE DATA
    # =====================================================

    df["created_at"] = pd.to_datetime(
        df["created_at"]
    )


    # =====================================================
    # OVERVIEW
    # =====================================================

    total = len(df)

    members = df["member_name"].nunique()

    diabetic = int(
        (df["prediction"] == 1).sum()
    )

    avg_bmi = df["bmi"].mean()

    avg_glucose = df["blood_glucose"].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Total Assessments",
            total
        )

    with col2:

        st.metric(
            "Family Members",
            members
        )

    with col3:

        st.metric(
            "Diabetic Predictions",
            diabetic
        )

    with col4:

        st.metric(
            "Average BMI",
            f"{avg_bmi:.1f}"
        )

    with col5:

        st.metric(
            "Average Glucose",
            f"{avg_glucose:.1f}"
        )


    st.divider()


    # =====================================================
    # MEMBER SELECTION
    # =====================================================

    st.markdown("### 👥 Select Family Member")

    member_names = sorted(
        df["member_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_member = st.selectbox(
        "Family Member",
        member_names
    )

    member_df = df[
        df["member_name"] == selected_member
    ].copy()


    # =====================================================
    # SELECTED MEMBER SUMMARY
    # =====================================================

    st.markdown(
        f"### 📊 {selected_member}'s Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Assessments",
            len(member_df)
        )

    with col2:

        st.metric(
            "Average BMI",
            f"{member_df['bmi'].mean():.1f}"
        )

    with col3:

        st.metric(
            "Average Glucose",
            f"{member_df['blood_glucose'].mean():.1f}"
        )

    with col4:

        st.metric(
            "Average HbA1c",
            f"{member_df['hba1c'].mean():.2f}%"
        )


    st.divider()


    # =====================================================
    # RISK TREND
    # =====================================================

    st.markdown("### 📈 Risk Trend")

    fig = px.line(
        member_df,
        x="created_at",
        y="risk_probability",
        markers=True,
        labels={
            "created_at": "Assessment Date",
            "risk_probability": "Estimated Risk (%)"
        }
    )

    fig.update_traces(
        line_width=3,
        marker_size=8
    )

    fig.update_yaxes(
        range=[0, 100]
    )

    fig = style_analytics_chart(
        fig,
        450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # BMI AND GLUCOSE
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ⚖️ BMI Trend")

        fig = px.line(
            member_df,
            x="created_at",
            y="bmi",
            markers=True,
            labels={
                "created_at": "Assessment Date",
                "bmi": "BMI"
            }
        )

        fig.update_traces(
            line_width=3,
            marker_size=8
        )

        fig = style_analytics_chart(
            fig,
            400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.markdown("### 🩸 Glucose Trend")

        fig = px.line(
            member_df,
            x="created_at",
            y="blood_glucose",
            markers=True,
            labels={
                "created_at": "Assessment Date",
                "blood_glucose": "Blood Glucose (mg/dL)"
            }
        )

        fig.update_traces(
            line_width=3,
            marker_size=8
        )

        fig = style_analytics_chart(
            fig,
            400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # =====================================================
    # HbA1c
    # =====================================================

    st.markdown("### 💉 HbA1c Trend")

    fig = px.line(
        member_df,
        x="created_at",
        y="hba1c",
        markers=True,
        labels={
            "created_at": "Assessment Date",
            "hba1c": "HbA1c (%)"
        }
    )

    fig.update_traces(
        line_width=3,
        marker_size=8
    )

    fig = style_analytics_chart(
        fig,
        400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # FAMILY MEMBER COMPARISON
    # =====================================================

    st.markdown("### 👥 Family Member Comparison")

    comparison = (
        df.groupby("member_name")
        .agg(
            Assessments=("assessment_id", "count"),
            Average_Risk=("risk_probability", "mean"),
            Average_BMI=("bmi", "mean"),
            Average_Glucose=("blood_glucose", "mean")
        )
        .reset_index()
    )

    comparison["Average_Risk"] = (
        comparison["Average_Risk"].round(1)
    )

    fig = px.bar(
        comparison,
        x="member_name",
        y="Average_Risk",
        text="Average_Risk",
        labels={
            "member_name": "Family Member",
            "Average_Risk": "Average Estimated Risk (%)"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_yaxes(
        range=[0, 100]
    )

    fig = style_analytics_chart(
        fig,
        450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# DATASET ANALYTICS
# =========================================================

def dataset_analytics():

    st.markdown("## 🌍 Dataset Analytics")

    st.caption(
        "Explore the original dataset used by the machine-learning model."
    )

    if dataset is None:

        st.error(
            "Diabetic_Prediction.csv was not found."
        )

        st.info(
            "Place Diabetic_Prediction.csv in the same folder "
            "as streamlit_app.py."
        )

        return


    df = dataset.copy()


    # =====================================================
    # OVERVIEW
    # =====================================================

    st.markdown("### 📌 Dataset Overview")

    total_records = len(df)

    total_diabetic = int(
        (df["diabetes"] == 1).sum()
    )

    total_non_diabetic = int(
        (df["diabetes"] == 0).sum()
    )

    total_female = int(
        (df["gender"] == 0).sum()
    )

    total_male = int(
        (df["gender"] == 1).sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👥 Total Records",
            total_records
        )

    with col2:

        st.metric(
            "🩺 Diabetic",
            total_diabetic
        )

    with col3:

        st.metric(
            "👩 Female",
            total_female
        )

    with col4:

        st.metric(
            "👨 Male",
            total_male
        )


    st.divider()


    # =====================================================
    # GENDER DISTRIBUTION
    # =====================================================

    st.markdown("### 📊 Gender Distribution")

    gender_count = (
        df["gender"]
        .replace(
            {
                0: "Female",
                1: "Male"
            }
        )
        .value_counts()
    )

    fig = px.bar(
        x=gender_count.index,
        y=gender_count.values,
        labels={
            "x": "Gender",
            "y": "Number of Patients"
        },
        text=gender_count.values
    )

    fig.update_traces(
        textposition="outside"
    )

    fig = style_analytics_chart(
        fig,
        450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # DIABETES DISTRIBUTION
    # =====================================================

    st.markdown("### 🩺 Diabetes Distribution")

    diabetes_count = (
        df["diabetes"]
        .replace(
            {
                0: "Non-Diabetic",
                1: "Diabetic"
            }
        )
        .value_counts()
    )

    fig = px.pie(
        names=diabetes_count.index,
        values=diabetes_count.values,
        hole=0.45
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    fig = style_analytics_chart(
        fig,
        450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # BMI DISTRIBUTION
    # =====================================================

    st.markdown("### ⚖️ BMI Distribution")

    fig = px.histogram(
        df,
        x="bmi",
        nbins=30
    )

    fig.update_layout(
        xaxis_title="BMI",
        yaxis_title="Number of Patients"
    )

    fig = style_analytics_chart(
        fig,
        450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    avg_bmi = df["bmi"].mean()

    min_bmi = df["bmi"].min()

    max_bmi = df["bmi"].max()

    st.write(
        f"**Average BMI:** {avg_bmi:.1f}  |  "
        f"**Minimum:** {min_bmi:.1f}  |  "
        f"**Maximum:** {max_bmi:.1f}"
    )


    # =====================================================
    # SMOKING HISTORY
    # =====================================================

    st.markdown(
        "### 🚬 Smoking History Distribution"
    )

    smoking_count = (
        df["smoking_history"]
        .replace(
            {
                0: "No Info",
                1: "Current",
                2: "Ever",
                3: "Former",
                4: "Never",
                5: "Not Current"
            }
        )
        .value_counts()
    )

    fig = px.bar(
        x=smoking_count.index,
        y=smoking_count.values,
        text=smoking_count.values,
        labels={
            "x": "Smoking History",
            "y": "Number of Patients"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    fig = style_analytics_chart(
        fig,
        500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # BLOOD GLUCOSE
    # =====================================================

    st.markdown(
        "### 🩸 Blood Glucose Level Distribution"
    )

    fig = px.histogram(
        df,
        x="blood_glucose_level",
        nbins=20
    )

    fig.update_layout(
        xaxis_title="Blood Glucose Level (mg/dL)",
        yaxis_title="Number of Patients"
    )

    fig = style_analytics_chart(
        fig,
        500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    avg_glucose = (
        df["blood_glucose_level"].mean()
    )

    min_glucose = (
        df["blood_glucose_level"].min()
    )

    max_glucose = (
        df["blood_glucose_level"].max()
    )

    st.write(
        f"**Average:** {avg_glucose:.1f} mg/dL  |  "
        f"**Minimum:** {min_glucose} mg/dL  |  "
        f"**Maximum:** {max_glucose} mg/dL"
    )


    # =====================================================
    # HbA1c
    # =====================================================

    st.markdown(
        "### 💉 HbA1c Level Distribution"
    )

    fig = px.histogram(
        df,
        x="HbA1c_level",
        nbins=20
    )

    fig.update_layout(
        xaxis_title="HbA1c Level (%)",
        yaxis_title="Number of Patients"
    )

    fig = style_analytics_chart(
        fig,
        500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    avg_hba1c = (
        df["HbA1c_level"].mean()
    )

    min_hba1c = (
        df["HbA1c_level"].min()
    )

    max_hba1c = (
        df["HbA1c_level"].max()
    )

    st.write(
        f"**Average HbA1c:** {avg_hba1c:.2f}%  |  "
        f"**Minimum:** {min_hba1c}%  |  "
        f"**Maximum:** {max_hba1c}%"
    )


    # =====================================================
    # HEART DISEASE VS DIABETES
    # =====================================================

    st.markdown(
        "### ❤️ Heart Disease vs Diabetes"
    )

    heart_df = (
        df.groupby(
            [
                "heart_disease",
                "diabetes"
            ]
        )
        .size()
        .reset_index(
            name="Count"
        )
    )

    heart_df["heart_disease"] = (
        heart_df["heart_disease"]
        .replace(
            {
                0: "No Heart Disease",
                1: "Heart Disease"
            }
        )
    )

    heart_df["diabetes"] = (
        heart_df["diabetes"]
        .replace(
            {
                0: "Non-Diabetic",
                1: "Diabetic"
            }
        )
    )

    fig = px.bar(
        heart_df,
        x="heart_disease",
        y="Count",
        color="diabetes",
        barmode="group",
        text="Count"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Heart Disease",
        yaxis_title="Patients"
    )

    fig = style_analytics_chart(
        fig,
        500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # HYPERTENSION VS DIABETES
    # =====================================================

    st.markdown(
        "### 🩺 Hypertension vs Diabetes"
    )

    hyper_df = (
        df.groupby(
            [
                "hypertension",
                "diabetes"
            ]
        )
        .size()
        .reset_index(
            name="Count"
        )
    )

    hyper_df["hypertension"] = (
        hyper_df["hypertension"]
        .replace(
            {
                0: "No Hypertension",
                1: "Hypertension"
            }
        )
    )

    hyper_df["diabetes"] = (
        hyper_df["diabetes"]
        .replace(
            {
                0: "Non-Diabetic",
                1: "Diabetic"
            }
        )
    )

    fig = px.bar(
        hyper_df,
        x="hypertension",
        y="Count",
        color="diabetes",
        barmode="group",
        text="Count"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Hypertension",
        yaxis_title="Number of Patients"
    )

    fig = style_analytics_chart(
        fig,
        500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # CORRELATION HEATMAP
    # =====================================================

    st.markdown("### 🔥 Correlation Heatmap")

    corr = (
        df
        .drop(
            columns=["Unnamed: 0"],
            errors="ignore"
        )
        .corr(
            numeric_only=True
        )
    )

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="Blues",
        aspect="auto"
    )

    fig = style_analytics_chart(
        fig,
        600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # KEY FINDINGS
    # =====================================================

    st.markdown("### 🎯 Key Findings")

    st.markdown(
        f"""
        **Dataset Size:** {total_records:,} records

        **Diabetic Records:** {total_diabetic:,}

        **Non-Diabetic Records:** {total_non_diabetic:,}

        **Female Records:** {total_female:,}

        **Male Records:** {total_male:,}

        **Average BMI:** {avg_bmi:.1f}

        **Average Blood Glucose:** {avg_glucose:.1f} mg/dL

        **Average HbA1c:** {avg_hba1c:.2f}%
        """
    )

    st.info(
        "The dataset contains multiple health-related "
        "features including age, BMI, HbA1c, blood glucose, "
        "hypertension, heart disease and smoking history. "
        "These features are used as inputs for the machine-learning model."
    )


# =========================================================
# ANALYTICS PAGE
# =========================================================

def analytics_page():

    st.title("📊 Analytics")

    st.caption(
        "Explore your personal health data, family assessment "
        "data and the original machine-learning dataset."
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        [
            "👤 Personal",
            "👨‍👩‍👧 Family",
            "🌍 Dataset"
        ]
    )

    with tab1:

        personal_analytics()

    with tab2:

        family_analytics()

    with tab3:

        dataset_analytics()
# =========================================================
# PROGRESS PAGE
# =========================================================

def progress_page():

    st.title("📈 Progress")

    st.caption(
        "Track changes in your health measurements across your saved assessments."
    )

    # =====================================================
    # LOAD PERSONAL ASSESSMENTS
    # =====================================================

    db = None
    cursor = None

    try:

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                assessment_id,
                bmi,
                hba1c,
                blood_glucose,
                prediction,
                risk_probability,
                created_at
            FROM assessments
            WHERE user_id = %s
            AND member_id IS NULL
            ORDER BY created_at ASC
            """,
            (
                st.session_state.user_id,
            )
        )

        records = cursor.fetchall()

        df = pd.DataFrame(records)

    except Exception as e:

        st.error(
            f"Could not load progress data: {e}"
        )

        return

    finally:

        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()


    # =====================================================
    # NO DATA
    # =====================================================

    if df.empty:

        st.info(
            "Complete your first personal assessment "
            "to start tracking your progress."
        )

        return


    # =====================================================
    # PREPARE DATA
    # =====================================================

    df["created_at"] = pd.to_datetime(
        df["created_at"]
    )

    df = df.sort_values(
        "created_at"
    ).reset_index(
        drop=True
    )


    # =====================================================
    # CURRENT AND PREVIOUS VALUES
    # =====================================================

    current = df.iloc[-1]

    if len(df) > 1:

        previous = df.iloc[-2]

    else:

        previous = None


    current_risk = float(
        current["risk_probability"]
    )

    current_bmi = float(
        current["bmi"]
    )

    current_glucose = float(
        current["blood_glucose"]
    )

    current_hba1c = float(
        current["hba1c"]
    )


    # =====================================================
    # CHANGES
    # =====================================================

    if previous is not None:

        previous_risk = float(
            previous["risk_probability"]
        )

        previous_bmi = float(
            previous["bmi"]
        )

        previous_glucose = float(
            previous["blood_glucose"]
        )

        previous_hba1c = float(
            previous["hba1c"]
        )

        risk_change = (
            current_risk - previous_risk
        )

        bmi_change = (
            current_bmi - previous_bmi
        )

        glucose_change = (
            current_glucose - previous_glucose
        )

        hba1c_change = (
            current_hba1c - previous_hba1c
        )

    else:

        previous_risk = None
        previous_bmi = None
        previous_glucose = None
        previous_hba1c = None

        risk_change = None
        bmi_change = None
        glucose_change = None
        hba1c_change = None


    # =====================================================
    # CURRENT STATUS
    # =====================================================

    st.markdown("### 📌 Current Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Current Risk",
            f"{current_risk:.1f}%"
        )

    with col2:

        st.metric(
            "Current BMI",
            f"{current_bmi:.1f}"
        )

    with col3:

        st.metric(
            "Blood Glucose",
            f"{current_glucose:.0f} mg/dL"
        )

    with col4:

        st.metric(
            "HbA1c",
            f"{current_hba1c:.2f}%"
        )


    st.divider()


    # =====================================================
    # CHANGES FROM PREVIOUS ASSESSMENT
    # =====================================================

    st.markdown(
        "### 🔄 Change From Previous Assessment"
    )

    if previous is None:

        st.info(
            "This is your first assessment. "
            "Complete another assessment later to see how your measurements change."
        )

    else:

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Risk Change",
                f"{risk_change:+.1f}%",
                delta=f"{risk_change:+.1f}%"
            )

        with col2:

            st.metric(
                "BMI Change",
                f"{bmi_change:+.1f}",
                delta=f"{bmi_change:+.1f}"
            )

        with col3:

            st.metric(
                "Glucose Change",
                f"{glucose_change:+.0f} mg/dL",
                delta=f"{glucose_change:+.0f} mg/dL"
            )

        with col4:

            st.metric(
                "HbA1c Change",
                f"{hba1c_change:+.2f}%",
                delta=f"{hba1c_change:+.2f}%"
            )


    st.divider()


    # =====================================================
    # RISK PROGRESS
    # =====================================================

    st.markdown("### 📈 Risk Progress")

    fig = px.line(
        df,
        x="created_at",
        y="risk_probability",
        markers=True,
        labels={
            "created_at": "Assessment Date",
            "risk_probability": "Estimated Risk (%)"
        }
    )

    fig.update_traces(
        line_width=3,
        marker_size=9
    )

    fig.update_yaxes(
        range=[0, 100]
    )

    fig.update_layout(
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # BMI PROGRESS
    # =====================================================

    st.markdown("### ⚖️ BMI Progress")

    fig = px.line(
        df,
        x="created_at",
        y="bmi",
        markers=True,
        labels={
            "created_at": "Assessment Date",
            "bmi": "BMI"
        }
    )

    fig.update_traces(
        line_width=3,
        marker_size=9
    )

    fig.update_layout(
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # BLOOD GLUCOSE PROGRESS
    # =====================================================

    st.markdown("### 🩸 Blood Glucose Progress")

    fig = px.line(
        df,
        x="created_at",
        y="blood_glucose",
        markers=True,
        labels={
            "created_at": "Assessment Date",
            "blood_glucose": "Blood Glucose (mg/dL)"
        }
    )

    fig.update_traces(
        line_width=3,
        marker_size=9
    )

    fig.update_layout(
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # HbA1c PROGRESS
    # =====================================================

    st.markdown("### 💉 HbA1c Progress")

    fig = px.line(
        df,
        x="created_at",
        y="hba1c",
        markers=True,
        labels={
            "created_at": "Assessment Date",
            "hba1c": "HbA1c (%)"
        }
    )

    fig.update_traces(
        line_width=3,
        marker_size=9
    )

    fig.update_layout(
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # ASSESSMENT HISTORY
    # =====================================================

    st.markdown("### 📋 Assessment History")

    history = df[
        [
            "created_at",
            "bmi",
            "hba1c",
            "blood_glucose",
            "risk_probability",
            "prediction"
        ]
    ].copy()

    history["created_at"] = (
        history["created_at"]
        .dt.strftime("%d %b %Y")
    )

    history["prediction"] = (
        history["prediction"]
        .map(
            {
                0: "Non-Diabetic",
                1: "Diabetic"
            }
        )
    )

    history = history.rename(
        columns={
            "created_at": "Date",
            "bmi": "BMI",
            "hba1c": "HbA1c (%)",
            "blood_glucose": "Blood Glucose",
            "risk_probability": "Estimated Risk (%)",
            "prediction": "Prediction"
        }
    )

    history["BMI"] = history["BMI"].round(1)

    history["HbA1c (%)"] = (
        history["HbA1c (%)"].round(2)
    )

    history["Estimated Risk (%)"] = (
        history["Estimated Risk (%)"].round(1)
    )

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # PROGRESS SUMMARY
    # =====================================================

    st.markdown("### 📝 Progress Summary")

    if previous is None:

        st.info(
            "Your progress history will become more meaningful "
            "as you complete additional assessments over time."
        )

    else:

        latest_date = current["created_at"]

        previous_date = previous["created_at"]

        st.write(
            f"Your latest assessment was recorded on "
            f"**{latest_date.strftime('%d %B %Y')}**."
        )

        st.write(
            f"Compared with your previous assessment on "
            f"**{previous_date.strftime('%d %B %Y')}**, "
            f"your estimated risk changed by "
            f"**{risk_change:+.1f} percentage points**."
        )

        st.write(
            f"Your BMI changed by **{bmi_change:+.1f}**, "
            f"blood glucose changed by "
            f"**{glucose_change:+.0f} mg/dL**, "
            f"and HbA1c changed by "
            f"**{hba1c_change:+.2f} percentage points**."
        )

        st.caption(
            "Progress values describe changes between your saved "
            "assessments. They are not a medical diagnosis."
        )
# =========================================================
# REMINDERS PAGE
# =========================================================

def reminders_page():

    st.title("🔔 Reminders")

    st.caption(
        "Create and manage your personal health reminders."
    )

    st.divider()

    # =====================================================
    # CREATE NEW REMINDER
    # =====================================================

    st.markdown("### ➕ Create New Reminder")

    with st.form("reminder_form"):

        title = st.text_input(
            "Reminder Title",
            placeholder="Example: Take morning medicine"
        )

        reminder_type = st.selectbox(
            "Reminder Type",
            [
                "Medication",
                "Health Checkup",
                "Blood Test",
                "Assessment",
                "Water",
                "Exercise",
                "Custom"
            ]
        )

        col1, col2 = st.columns(2)

        with col1:

            reminder_date = st.date_input(
                "Date"
            )

        with col2:

            reminder_time = st.time_input(
                "Time"
            )

        notes = st.text_area(
            "Notes",
            placeholder="Add any additional information..."
        )

        submitted = st.form_submit_button(
            "➕ Add Reminder",
            use_container_width=True
        )

    # =====================================================
    # SAVE REMINDER
    # =====================================================

    if submitted:

        if not title.strip():

            st.error(
                "Please enter a reminder title."
            )

        else:

            db = None
            cursor = None

            try:

                db = get_db_connection()

                cursor = db.cursor()

                cursor.execute(
                    """
                    INSERT INTO reminders
                    (
                        user_id,
                        title,
                        reminder_type,
                        reminder_date,
                        reminder_time,
                        notes
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        st.session_state.user_id,
                        title.strip(),
                        reminder_type,
                        reminder_date,
                        reminder_time,
                        notes.strip()
                    )
                )

                db.commit()

                st.success(
                    "Reminder added successfully."
                )

                st.rerun()

            except Exception as e:

                if db:
                    db.rollback()

                st.error(
                    f"Could not save reminder: {e}"
                )

            finally:

                if cursor:
                    cursor.close()

                if db:
                    db.close()

    st.divider()

    # =====================================================
    # LOAD REMINDERS
    # =====================================================

    db = None
    cursor = None

    try:

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                reminder_id,
                title,
                reminder_type,
                reminder_date,
                reminder_time,
                notes,
                is_completed
            FROM reminders
            WHERE user_id = %s
            ORDER BY
                reminder_date ASC,
                reminder_time ASC
            """,
            (
                st.session_state.user_id,
            )
        )

        reminders = cursor.fetchall()

    except Exception as e:

        st.error(
            f"Could not load reminders: {e}"
        )

        reminders = []

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()

    # =====================================================
    # REMINDER LIST
    # =====================================================

    st.markdown("### 📋 Your Reminders")

    if not reminders:

        st.info(
            "You don't have any reminders yet. "
            "Create your first reminder above."
        )

        return

    for reminder in reminders:

        reminder_id = reminder["reminder_id"]

        title = reminder["title"]

        reminder_type = reminder["reminder_type"]

        reminder_date = reminder["reminder_date"]

        reminder_time = reminder["reminder_time"]

        notes = reminder["notes"]

        is_completed = reminder["is_completed"]

        if is_completed:

            status = "✅ Completed"

        else:

            status = "⏳ Pending"

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [4, 2, 1]
            )

            with col1:

                st.markdown(
                    f"### {title}"
                )

                st.write(
                    f"**Type:** {reminder_type}"
                )

                if hasattr(reminder_time, "seconds"):

                    total_seconds = reminder_time.seconds

    

                if notes:

                    st.write(
                        f"📝 {notes}"
                    )

            with col2:

                st.write(status)

            with col3:

                if not is_completed:

                    if st.button(
                        "✓ Done",
                        key=f"complete_{reminder_id}",
                        use_container_width=True
                    ):

                        db = get_db_connection()

                        cursor = db.cursor()

                        cursor.execute(
                            """
                            UPDATE reminders
                            SET is_completed = 1
                            WHERE reminder_id = %s
                            AND user_id = %s
                            """,
                            (
                                reminder_id,
                                st.session_state.user_id
                            )
                        )

                        db.commit()

                        cursor.close()

                        db.close()

                        st.rerun()

                else:

                    if st.button(
                        "↩ Undo",
                        key=f"undo_{reminder_id}",
                        use_container_width=True
                    ):

                        db = get_db_connection()

                        cursor = db.cursor()

                        cursor.execute(
                            """
                            UPDATE reminders
                            SET is_completed = 0
                            WHERE reminder_id = %s
                            AND user_id = %s
                            """,
                            (
                                reminder_id,
                                st.session_state.user_id
                            )
                        )

                        db.commit()

                        cursor.close()

                        db.close()

                        st.rerun()
# =========================================================
# DASHBOARD REMINDER ALERTS
# =========================================================

def show_dashboard_reminders():

    db = None
    cursor = None

    try:

        db = get_db_connection()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                reminder_id,
                title,
                reminder_type,
                reminder_date,
                reminder_time,
                notes,
                is_completed
            FROM reminders
            WHERE user_id = %s
            AND is_completed = 0
            AND reminder_date >= CURDATE()
            ORDER BY reminder_date ASC, reminder_time ASC
            """,
            (
                st.session_state.user_id,
            )
        )

        reminders = cursor.fetchall()

    except Exception as e:

        st.error(
            f"Could not load reminders: {e}"
        )

        return

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()

    if not reminders:
        return

    now = datetime.now()

    due_reminders = []
    upcoming_reminders = []

    for reminder in reminders:

        reminder_date = reminder["reminder_date"]
        reminder_time = reminder["reminder_time"]

        # MySQL TIME comes as timedelta
        if hasattr(reminder_time, "seconds"):

            total_seconds = reminder_time.seconds

            hours = total_seconds // 3600

            minutes = (
                total_seconds % 3600
            ) // 60

            seconds = (
                total_seconds % 60
            )

            reminder_datetime = datetime.combine(
                reminder_date,
                time(
                    hours,
                    minutes,
                    seconds
                )
            )

        else:

            reminder_datetime = datetime.combine(
                reminder_date,
                reminder_time
            )

        if reminder_datetime <= now:

            due_reminders.append(
                reminder
            )

        else:

            upcoming_reminders.append(
                reminder
            )

    # =====================================================
    # DUE REMINDERS
    # =====================================================

    if due_reminders:

        st.error(
            f"🔴 You have {len(due_reminders)} "
            f"reminder(s) due."
        )

        for reminder in due_reminders:

            reminder_id = reminder["reminder_id"]

            reminder_time = reminder["reminder_time"]

            total_seconds = reminder_time.seconds

            hours = total_seconds // 3600

            minutes = (
                total_seconds % 3600
            ) // 60

            if hours == 0:

                display_hour = 12
                period = "AM"

            elif hours < 12:

                display_hour = hours
                period = "AM"

            elif hours == 12:

                display_hour = 12
                period = "PM"

            else:

                display_hour = hours - 12
                period = "PM"

            display_time = (
                f"{display_hour:02d}:"
                f"{minutes:02d} "
                f"{period}"
            )

            with st.container(border=True):

                col1, col2 = st.columns(
                    [5, 1]
                )

                with col1:

                    st.markdown(
                        f"### 🔴 {reminder['title']}"
                    )

                    st.write(
                        f"**Type:** "
                        f"{reminder['reminder_type']}"
                    )

                    st.write(
                        f"Scheduled for "
                        f"**{display_time}**"
                    )

                    if reminder["notes"]:

                        st.caption(
                            reminder["notes"]
                        )

                with col2:

                    if st.button(
                        "✓ Done",
                        key=f"dashboard_done_{reminder_id}",
                        use_container_width=True
                    ):

                        db = get_db_connection()

                        cursor = db.cursor()

                        cursor.execute(
                            """
                            UPDATE reminders
                            SET is_completed = 1
                            WHERE reminder_id = %s
                            AND user_id = %s
                            """,
                            (
                                reminder_id,
                                st.session_state.user_id
                            )
                        )

                        db.commit()

                        cursor.close()

                        db.close()

                        st.rerun()

    # =====================================================
    # UPCOMING REMINDERS
    # =====================================================

    if upcoming_reminders:

        st.markdown(
            "### 🔔 Upcoming Reminders"
        )

        for reminder in upcoming_reminders[:5]:

            reminder_time = reminder["reminder_time"]

            total_seconds = reminder_time.seconds

            hours = total_seconds // 3600

            minutes = (
                total_seconds % 3600
            ) // 60

            if hours == 0:

                display_hour = 12
                period = "AM"

            elif hours < 12:

                display_hour = hours
                period = "AM"

            elif hours == 12:

                display_hour = 12
                period = "PM"

            else:

                display_hour = hours - 12
                period = "PM"

            display_time = (
                f"{display_hour:02d}:"
                f"{minutes:02d} "
                f"{period}"
            )

            st.info(
                f"🔔 **{reminder['title']}**  \n"
                f"📅 {reminder['reminder_date'].strftime('%d %b %Y')}  "
                f"🕒 {display_time}"
            )
# =========================================================
# HEALTH KNOWLEDGE PAGE
# =========================================================

def health_knowledge_page():

    st.title("📚 Health Knowledge")

    st.caption(
        "Learn about important health measurements, diabetes-related "
        "topics and healthy lifestyle habits."
    )

    st.divider()

    knowledge = {
        "🩸 Blood Glucose": {
            "category": "Health Measurements",
            "description": "Learn what blood glucose means and why it is monitored.",
            "content": """
Blood glucose is the amount of glucose present in your blood.

Glucose is an important source of energy for the body. The body normally
regulates blood glucose using hormones such as insulin.

Blood glucose measurements can vary depending on factors such as meals,
physical activity, medications and overall health.

Regular monitoring may help people and healthcare professionals understand
changes over time.
"""
        },

        "💉 HbA1c": {
            "category": "Health Measurements",
            "description": "Understand HbA1c and what it tells you about blood glucose.",
            "content": """
HbA1c is a blood test that reflects average blood glucose levels over
approximately the previous two to three months.

Unlike a single blood glucose measurement, HbA1c provides a longer-term
view of glucose levels.

Healthcare professionals may use HbA1c along with other information when
assessing glucose control.
"""
        },

        "⚖️ BMI": {
            "category": "Health Measurements",
            "description": "Learn what Body Mass Index means.",
            "content": """
Body Mass Index (BMI) is a measurement calculated using a person's weight
and height.

BMI can be useful for population-level health assessment, but it does not
directly measure body fat and does not provide a complete picture of an
individual's health.

Healthcare professionals may consider BMI together with other health
information.
"""
        },

        "❤️ Heart Health": {
            "category": "Health & Lifestyle",
            "description": "Learn about factors that can affect cardiovascular health.",
            "content": """
Heart health can be influenced by many factors, including physical
activity, nutrition, blood pressure, smoking, sleep and other health
conditions.

Regular physical activity, balanced nutrition, avoiding tobacco and
following appropriate medical advice can support overall cardiovascular
health.

People with existing health conditions should discuss appropriate lifestyle
changes with a healthcare professional.
"""
        },

        "🚬 Smoking": {
            "category": "Health & Lifestyle",
            "description": "Understand why smoking history is considered in health assessment.",
            "content": """
Smoking can affect many parts of the body and is associated with several
long-term health risks.

Smoking history is therefore often considered when evaluating overall
health risk.

If you smoke and want to quit, healthcare professionals and smoking
cessation programs can provide support and guidance.
"""
        },

        "🏃 Physical Activity": {
            "category": "Healthy Lifestyle",
            "description": "Learn why regular physical activity matters.",
            "content": """
Regular physical activity can support cardiovascular fitness, muscle
strength and overall wellbeing.

The appropriate amount and type of activity can vary between individuals.

People with medical conditions or specific health concerns should discuss
suitable activities with a healthcare professional.
"""
        },

        "🥗 Healthy Eating": {
            "category": "Healthy Lifestyle",
            "description": "Learn about balanced nutrition and healthy food habits.",
            "content": """
A balanced eating pattern can include vegetables, fruits, whole grains,
appropriate protein sources and other nutrient-rich foods.

Healthy eating is not simply about removing one particular food. Overall
dietary patterns, portion sizes and individual nutritional needs are important.

People with diabetes or other medical conditions may have specific dietary
requirements and should follow advice from their healthcare professional.
"""
        },

        "😴 Sleep & Health": {
            "category": "Healthy Lifestyle",
            "description": "Understand the connection between sleep and overall health.",
            "content": """
Sleep is an important part of overall health and wellbeing.

Consistent sleep routines and good sleep habits can support physical
and mental wellbeing.

Persistent sleep problems should be discussed with a healthcare professional,
especially when they affect daily activities or overall health.
"""
        }
    }

    # ---------------------------------------------------------
    # SHOW SELECTED TOPIC FIRST
    # ---------------------------------------------------------

    selected_topic = st.session_state.get("selected_health_topic")

    if selected_topic in knowledge:

        details = knowledge[selected_topic]

        st.markdown(f"## {selected_topic}")
        st.caption(details["category"])

        st.markdown(
            f"""
            <div style="
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 16px;
                padding: 25px;
                margin-bottom: 20px;
            ">
                {details["content"].replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "This information is for educational purposes and "
            "does not replace professional medical advice."
        )

        if st.button(
            "← Back to Topics",
            use_container_width=True
        ):
            st.session_state["selected_health_topic"] = None
            st.rerun()

        st.divider()

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------

    search = st.text_input(
        "🔎 Search Health Topics",
        placeholder="Search glucose, HbA1c, BMI, exercise..."
    )

    filtered_topics = []

    for topic, details in knowledge.items():

        search_text = (
            topic.lower()
            + " "
            + details["category"].lower()
            + " "
            + details["description"].lower()
            + " "
            + details["content"].lower()
        )

        if search.strip().lower() in search_text:
            filtered_topics.append((topic, details))

    st.markdown("### 📖 Explore Topics")

    if not filtered_topics:
        st.warning("No health topic found. Try another search.")
        return

    # ---------------------------------------------------------
    # TOPIC CARDS
    # ---------------------------------------------------------

    columns = st.columns(2)

    for index, (topic, details) in enumerate(filtered_topics):

        with columns[index % 2]:

            with st.container(border=True):

                st.markdown(f"### {topic}")

                st.caption(details["category"])

                st.write(details["description"])

                button_text = (
                    "Viewing"
                    if selected_topic == topic
                    else "Read More"
                )

                if st.button(
                    button_text,
                    key=f"knowledge_{index}",
                    use_container_width=True,
                    disabled=(selected_topic == topic)
                ):
                    st.session_state["selected_health_topic"] = topic
                    st.rerun()

# =========================================================
# PROFESSIONAL HEALTH REPORT PDF
# =========================================================

def generate_health_report(assessment):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=14 * mm,
        leftMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=23,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111111")
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#555555")
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1F2937"),
        spaceBefore=5,
        spaceAfter=5
    )

    normal_style = ParagraphStyle(
        "NormalReport",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#222222")
    )

    small_style = ParagraphStyle(
        "SmallReport",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#666666")
    )

    value_style = ParagraphStyle(
        "Value",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#111111")
    )

    story = []

    previous = assessment.get("previous")

    # =====================================================
    # HEADER
    # =====================================================

    header_table = Table(
        [
            [
                Paragraph(
                    "<b>DIABETESHEALTH</b><br/>"
                    "<font size='7'>PERSONAL HEALTH SUPPORT PLATFORM</font>",
                    ParagraphStyle(
                        "Brand",
                        parent=styles["Normal"],
                        fontName="Helvetica-Bold",
                        fontSize=15,
                        leading=18,
                        textColor=colors.HexColor("#111111")
                    )
                ),
                Paragraph(
                    "<b>HEALTH ASSESSMENT REPORT</b><br/>"
                    f"<font size='7'>Report ID: DH-{assessment['assessment_id']:06d}</font>",
                    ParagraphStyle(
                        "HeaderRight",
                        parent=styles["Normal"],
                        fontName="Helvetica",
                        fontSize=9,
                        leading=12,
                        alignment=TA_RIGHT,
                        textColor=colors.HexColor("#333333")
                    )
                )
            ]
        ],
        colWidths=[95 * mm, 83 * mm]
    )

    header_table.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LINEBELOW", (0, 0), (-1, 0), 1.2, colors.HexColor("#222222")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(header_table)
    story.append(Spacer(1, 4 * mm))

    # =====================================================
    # REPORT DATE
    # =====================================================

    report_info = Table(
        [
            [
                Paragraph(
                    "<b>Assessment Date</b><br/>"
                    f"{assessment['created_at'].strftime('%d %B %Y')}",
                    normal_style
                ),
                Paragraph(
                    "<b>Assessment Time</b><br/>"
                    f"{assessment['created_at'].strftime('%I:%M %p')}",
                    normal_style
                ),
                Paragraph(
                    "<b>Report Type</b><br/>"
                    "Diabetes Risk Assessment",
                    normal_style
                )
            ]
        ],
        colWidths=[59 * mm, 59 * mm, 60 * mm]
    )

    report_info.setStyle(
        TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#AAAAAA")),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7F7F7")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ])
    )

    story.append(report_info)

    # =====================================================
    # PATIENT INFORMATION
    # =====================================================

    story.append(
        Paragraph(
            "PATIENT INFORMATION",
            section_style
        )
    )

    patient_table = Table(
        [
            [
                Paragraph("<b>Patient Name</b>", normal_style),
                Paragraph(
                    str(assessment["patient_name"]),
                    value_style
                ),
                Paragraph("<b>Age</b>", normal_style),
                Paragraph(
                    f"{assessment['age']} Years",
                    value_style
                )
            ],
            [
                Paragraph("<b>Gender</b>", normal_style),
                Paragraph(
                    str(assessment["gender"]),
                    value_style
                ),
                Paragraph("<b>Assessment ID</b>", normal_style),
                Paragraph(
                    f"DH-{assessment['assessment_id']:06d}",
                    value_style
                )
            ]
        ],
        colWidths=[31 * mm, 59 * mm, 31 * mm, 57 * mm]
    )

    patient_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#AAAAAA")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3F3F3")),
            ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#F3F3F3")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(patient_table)

    # =====================================================
    # INVESTIGATION RESULTS
    # =====================================================

    story.append(
        Paragraph(
            "INVESTIGATION RESULTS",
            section_style
        )
    )

    if previous:

        previous_glucose = f"{previous['blood_glucose']} mg/dL"
        previous_hba1c = f"{previous['hba1c']}%"
        previous_bmi = f"{previous['bmi']}"

        def change_text(current, old):

            difference = float(current) - float(old)

            if difference > 0:
                return f"↑ {difference:.2f}"

            if difference < 0:
                return f"↓ {abs(difference):.2f}"

            return "—"

        glucose_change = change_text(
            assessment["blood_glucose"],
            previous["blood_glucose"]
        )

        hba1c_change = change_text(
            assessment["hba1c"],
            previous["hba1c"]
        )

        bmi_change = change_text(
            assessment["bmi"],
            previous["bmi"]
        )

        investigation_data = [
            [
                Paragraph("<b>Parameter</b>", normal_style),
                Paragraph("<b>Current</b>", normal_style),
                Paragraph("<b>Previous</b>", normal_style),
                Paragraph("<b>Change</b>", normal_style),
                Paragraph("<b>Unit</b>", normal_style)
            ],
            [
                "Blood Glucose",
                str(assessment["blood_glucose"]),
                str(previous["blood_glucose"]),
                glucose_change,
                "mg/dL"
            ],
            [
                "HbA1c",
                str(assessment["hba1c"]),
                str(previous["hba1c"]),
                hba1c_change,
                "%"
            ],
            [
                "Body Mass Index",
                str(assessment["bmi"]),
                str(previous["bmi"]),
                bmi_change,
                "kg/m²"
            ]
        ]

    else:

        investigation_data = [
            [
                Paragraph("<b>Parameter</b>", normal_style),
                Paragraph("<b>Current</b>", normal_style),
                Paragraph("<b>Unit</b>", normal_style),
                Paragraph("<b>Previous</b>", normal_style)
            ],
            [
                "Blood Glucose",
                str(assessment["blood_glucose"]),
                "mg/dL",
                "Not available"
            ],
            [
                "HbA1c",
                str(assessment["hba1c"]),
                "%",
                "Not available"
            ],
            [
                "Body Mass Index",
                str(assessment["bmi"]),
                "kg/m²",
                "Not available"
            ]
        ]

    investigation_table = Table(
        investigation_data,
        colWidths=[
            52 * mm,
            31 * mm,
            31 * mm,
            31 * mm,
            33 * mm
        ]
        if previous
        else [
            60 * mm,
            38 * mm,
            38 * mm,
            42 * mm
        ]
    )

    investigation_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#AAAAAA")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDEDED")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(investigation_table)

    # =====================================================
    # ADDITIONAL HEALTH FACTORS
    # =====================================================

    story.append(
        Paragraph(
            "ADDITIONAL HEALTH FACTORS",
            section_style
        )
    )

    hypertension = (
        "Present"
        if assessment["hypertension"]
        else "Not recorded"
    )

    heart_disease = (
        "Present"
        if assessment["heart_disease"]
        else "Not recorded"
    )

    factors_table = Table(
        [
            [
                Paragraph("<b>Hypertension</b>", normal_style),
                hypertension,
                Paragraph("<b>Heart Disease</b>", normal_style),
                heart_disease
            ],
            [
                Paragraph("<b>Smoking History</b>", normal_style),
                assessment["smoking_history"],
                Paragraph("<b>Model Result</b>", normal_style),
                (
                    "Higher estimated risk"
                    if assessment["prediction"] == 1
                    else "Lower estimated risk"
                )
            ]
        ],
        colWidths=[35 * mm, 54 * mm, 35 * mm, 54 * mm]
    )

    factors_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#AAAAAA")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3F3F3")),
            ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#F3F3F3")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(factors_table)

    # =====================================================
    # RISK ASSESSMENT
    # =====================================================

    story.append(
        Paragraph(
            "MACHINE-LEARNING RISK ASSESSMENT",
            section_style
        )
    )

    risk = (
        float(assessment["risk_probability"])
        if assessment["risk_probability"] is not None
        else 0
    )

    risk_display = f"{risk:.1f}%"

    risk_result = Table(
        [
            [
                Paragraph(
                    "<b>Estimated Diabetes Risk</b>",
                    normal_style
                ),
                Paragraph(
                    f"<b>{risk_display}</b>",
                    ParagraphStyle(
                        "RiskValue",
                        parent=styles["Normal"],
                        fontName="Helvetica-Bold",
                        fontSize=18,
                        alignment=TA_CENTER,
                        textColor=colors.HexColor("#111111")
                    )
                )
            ]
        ],
        colWidths=[89 * mm, 89 * mm]
    )

    risk_result.setStyle(
        TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#777777")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7F7F7")),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    )

    story.append(risk_result)

    story.append(Spacer(1, 3 * mm))

    # Risk scale

    risk_scale = Table(
        [
            [
                "LOW",
                "MODERATE",
                "HIGH"
            ],
            [
                "0–33%",
                "34–66%",
                "67–100%"
            ]
        ],
        colWidths=[59 * mm, 59 * mm, 60 * mm]
    )

    risk_scale.setStyle(
        TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#AAAAAA")),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
    )

    story.append(risk_scale)

    # =====================================================
    # AUTOMATED SUMMARY
    # =====================================================

    story.append(
        Paragraph(
            "AUTOMATED HEALTH SUMMARY",
            section_style
        )
    )

    if previous:

        risk_change = (
            float(assessment["risk_probability"])
            - float(previous["risk_probability"])
        )

        if risk_change > 0:
            risk_sentence = (
                f"The estimated diabetes risk has increased by "
                f"{abs(risk_change):.1f} percentage points "
                f"compared with the previous assessment."
            )

        elif risk_change < 0:
            risk_sentence = (
                f"The estimated diabetes risk has decreased by "
                f"{abs(risk_change):.1f} percentage points "
                f"compared with the previous assessment."
            )

        else:
            risk_sentence = (
                "The estimated diabetes risk is unchanged "
                "compared with the previous assessment."
            )

        summary = (
            f"The latest assessment for <b>{assessment['patient_name']}</b> "
            f"was recorded on "
            f"{assessment['created_at'].strftime('%d %B %Y')}. "
            f"The current estimated diabetes risk is "
            f"<b>{risk_display}</b>. {risk_sentence}"
        )

    else:

        summary = (
            f"The latest assessment for "
            f"<b>{assessment['patient_name']}</b> was recorded on "
            f"{assessment['created_at'].strftime('%d %B %Y')}. "
            f"The estimated diabetes risk from the machine-learning "
            f"model is <b>{risk_display}</b>. "
            f"This is the first recorded assessment available for "
            f"comparison."
        )

    summary_table = Table(
        [
            [
                Paragraph(
                    summary,
                    normal_style
                )
            ]
        ],
        colWidths=[178 * mm]
    )

    summary_table.setStyle(
        TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#AAAAAA")),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FAFAFA")),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ])
    )

    story.append(summary_table)

    # =====================================================
    # DISCLAIMER
    # =====================================================

    story.append(Spacer(1, 5 * mm))

    disclaimer = (
        "<b>Important:</b> This report is generated from information "
        "recorded in the DiabetesHealth application and an "
        "machine-learning risk model. The estimated result is intended "
        "for health-support and educational purposes and should not be "
        "considered a medical diagnosis."
    )

    story.append(
        Paragraph(
            disclaimer,
            small_style
        )
    )

    # =====================================================
    # FOOTER
    # =====================================================

    story.append(Spacer(1, 5 * mm))

    footer_table = Table(
        [
            [
                Paragraph(
                    "<b>DIABETESHEALTH</b><br/>"
                    "Digital Health Support Platform",
                    small_style
                ),
                Paragraph(
                    "Generated electronically<br/>"
                    f"Report DH-{assessment['assessment_id']:06d}",
                    ParagraphStyle(
                        "FooterRight",
                        parent=small_style,
                        alignment=TA_RIGHT
                    )
                )
            ]
        ],
        colWidths=[90 * mm, 88 * mm]
    )

    footer_table.setStyle(
        TableStyle([
            ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.HexColor("#777777")),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
    )

    story.append(footer_table)

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(story)

    buffer.seek(0)

    return buffer


# =========================================================
# REPORTS PAGE
# =========================================================

def reports_page():

    st.title("📄 Health Reports")

    st.caption(
        "Automatically generated health reports based on your "
        "assessment history and machine-learning results."
    )

    st.divider()

    db = None
    cursor = None

    try:

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                a.assessment_id,
                a.member_id,
                a.age,
                a.gender,
                a.bmi,
                a.hba1c,
                a.blood_glucose,
                a.hypertension,
                a.heart_disease,
                a.smoking_history,
                a.prediction,
                a.risk_probability,
                a.created_at,
                u.full_name AS user_name,
                fm.name AS family_name
            FROM assessments a
            JOIN users u
                ON a.user_id = u.user_id
            LEFT JOIN family_members fm
                ON a.member_id = fm.member_id
            WHERE a.user_id = %s
            ORDER BY a.created_at DESC
            """,
            (st.session_state.user_id,)
        )

        assessments = cursor.fetchall()

    except Exception as e:

        st.error(f"Could not load assessment history: {e}")
        return

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()

    if not assessments:

        st.info(
            "No assessment data is available yet. "
            "Complete an assessment to generate your first report."
        )

        return

    # -----------------------------------------------------
    # LATEST ASSESSMENT
    # -----------------------------------------------------

    latest = assessments[0]

    patient_name = (
        latest["family_name"]
        if latest["family_name"]
        else latest["user_name"]
    )

    # -----------------------------------------------------
    # PREVIOUS ASSESSMENT
    # -----------------------------------------------------

    previous = None

    for assessment in assessments[1:]:

        if assessment["member_id"] == latest["member_id"]:
            previous = assessment
            break

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    st.markdown("## Latest Health Report")

    st.caption(
        f"Patient: {patient_name}  •  "
        f"Assessment ID: DH-{latest['assessment_id']:06d}"
    )

    st.divider()

    # -----------------------------------------------------
    # SUMMARY METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Estimated Risk",
            f"{float(latest['risk_probability']):.1f}%"
            if latest["risk_probability"] is not None
            else "N/A"
        )

    with col2:
        st.metric(
            "BMI",
            f"{float(latest['bmi']):.1f}"
        )

    with col3:
        st.metric(
            "Blood Glucose",
            f"{latest['blood_glucose']} mg/dL"
        )

    with col4:
        st.metric(
            "HbA1c",
            f"{float(latest['hba1c']):.1f}%"
        )

    # -----------------------------------------------------
    # PATIENT INFORMATION
    # -----------------------------------------------------

    st.markdown("### Patient Information")

    patient_col1, patient_col2 = st.columns(2)

    with patient_col1:

        st.write(f"**Name:** {patient_name}")
        st.write(f"**Age:** {latest['age']} years")
        st.write(f"**Gender:** {latest['gender']}")

    with patient_col2:

        st.write(
            f"**Assessment Date:** "
            f"{latest['created_at'].strftime('%d %B %Y')}"
        )

        st.write(
            f"**Assessment Time:** "
            f"{latest['created_at'].strftime('%I:%M %p')}"
        )

        st.write(
            f"**Report ID:** DH-{latest['assessment_id']:06d}"
        )

    st.divider()

    # -----------------------------------------------------
    # CURRENT RESULTS
    # -----------------------------------------------------

    st.markdown("### Current Assessment")

    result_data = {
        "Parameter": [
            "Blood Glucose",
            "HbA1c",
            "BMI",
            "Hypertension",
            "Heart Disease",
            "Smoking History"
        ],
        "Current Result": [
            f"{latest['blood_glucose']} mg/dL",
            f"{latest['hba1c']}%",
            f"{latest['bmi']} kg/m²",
            "Yes" if latest["hypertension"] else "No",
            "Yes" if latest["heart_disease"] else "No",
            latest["smoking_history"]
        ]
    }

    st.table(result_data)

    # -----------------------------------------------------
    # CHANGE FROM PREVIOUS ASSESSMENT
    # -----------------------------------------------------

    st.markdown("### Change From Previous Assessment")

    if previous:

        def calculate_change(current, old):

            difference = float(current) - float(old)

            if difference > 0:
                return f"↑ {difference:.2f}"

            if difference < 0:
                return f"↓ {abs(difference):.2f}"

            return "No change"

        comparison_data = {
            "Parameter": [
                "Estimated Risk",
                "Blood Glucose",
                "HbA1c",
                "BMI"
            ],
            "Previous": [
                f"{float(previous['risk_probability']):.1f}%"
                if previous["risk_probability"] is not None
                else "N/A",

                f"{previous['blood_glucose']} mg/dL",

                f"{previous['hba1c']}%",

                f"{previous['bmi']}"
            ],
            "Current": [
                f"{float(latest['risk_probability']):.1f}%"
                if latest["risk_probability"] is not None
                else "N/A",

                f"{latest['blood_glucose']} mg/dL",

                f"{latest['hba1c']}%",

                f"{latest['bmi']}"
            ],
            "Change": [
                calculate_change(
                    latest["risk_probability"],
                    previous["risk_probability"]
                )
                if latest["risk_probability"] is not None
                and previous["risk_probability"] is not None
                else "N/A",

                calculate_change(
                    latest["blood_glucose"],
                    previous["blood_glucose"]
                ),

                calculate_change(
                    latest["hba1c"],
                    previous["hba1c"]
                ),

                calculate_change(
                    latest["bmi"],
                    previous["bmi"]
                )
            ]
        }

        st.table(comparison_data)

    else:

        st.info(
            "This is the first recorded assessment for this person. "
            "Future reports will compare results with this assessment."
        )

    # -----------------------------------------------------
    # RISK ASSESSMENT
    # -----------------------------------------------------

    st.markdown("### Diabetes Risk Assessment")

    if latest["risk_probability"] is not None:

        risk = float(latest["risk_probability"])

        st.progress(
            min(max(risk / 100, 0), 1)
        )

        st.markdown(
            f"**Estimated Risk: {risk:.1f}%**"
        )

        if latest["prediction"] == 1:

            st.warning(
                "The machine-learning model classified this assessment "
                "as a higher estimated diabetes-risk result."
            )

        else:

            st.success(
                "The machine-learning model classified this assessment "
                "as a lower estimated diabetes-risk result."
            )

    # -----------------------------------------------------
    # HEALTH FACTORS
    # -----------------------------------------------------

    st.markdown("### Recorded Health Factors")

    factor_col1, factor_col2 = st.columns(2)

    with factor_col1:

        st.write(
            f"**Hypertension:** "
            f"{'Present' if latest['hypertension'] else 'Not recorded'}"
        )

        st.write(
            f"**Heart Disease:** "
            f"{'Present' if latest['heart_disease'] else 'Not recorded'}"
        )

    with factor_col2:

        st.write(
            f"**Smoking History:** "
            f"{latest['smoking_history']}"
        )

        st.write(
            f"**Previous Assessment:** "
            f"{'Available' if previous else 'Not available'}"
        )

    # -----------------------------------------------------
    # REPORT SUMMARY
    # -----------------------------------------------------

    st.markdown("### Report Summary")

    if previous:

        risk_change = (
            float(latest["risk_probability"])
            - float(previous["risk_probability"])
        )

        if risk_change > 0:

            risk_summary = (
                f"The estimated risk has increased by "
                f"{abs(risk_change):.1f} percentage points "
                f"compared with the previous assessment."
            )

        elif risk_change < 0:

            risk_summary = (
                f"The estimated risk has decreased by "
                f"{abs(risk_change):.1f} percentage points "
                f"compared with the previous assessment."
            )

        else:

            risk_summary = (
                "The estimated risk is unchanged compared "
                "with the previous assessment."
            )

        st.write(
            f"Your latest assessment was recorded on "
            f"**{latest['created_at'].strftime('%d %B %Y')}**. "
            f"{risk_summary}"
        )

    else:

        st.write(
            "This is the first recorded assessment for this person. "
            "Future assessments can be compared with this result "
            "to monitor changes over time."
        )

    st.info(
        "This report provides an estimated result generated from the "
        "machine-learning model and recorded assessment information. "
        "It is intended for health-support and educational purposes."
    )

    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    st.divider()

    report_data = {
        "assessment_id": latest["assessment_id"],
        "patient_name": patient_name,
        "age": latest["age"],
        "gender": latest["gender"],
        "bmi": latest["bmi"],
        "hba1c": latest["hba1c"],
        "blood_glucose": latest["blood_glucose"],
        "hypertension": latest["hypertension"],
        "heart_disease": latest["heart_disease"],
        "smoking_history": latest["smoking_history"],
        "prediction": latest["prediction"],
        "risk_probability": latest["risk_probability"],
        "created_at": latest["created_at"],
        "previous": previous

    }

    pdf = generate_health_report(report_data)

    filename = (
        f"DiabetesHealth_Report_"
        f"{patient_name.replace(' ', '_')}_"
        f"{latest['created_at'].strftime('%Y%m%d')}.pdf"
    )

    st.download_button(
        "📥 Download Full Health Report",
        data=pdf,
        file_name=filename,
        mime="application/pdf",
        use_container_width=True
    )

# =========================================================
# PAGE ROUTER
# =========================================================

if st.session_state.page == "landing":landing_page()

elif st.session_state.page == "signup":signup_page()

elif st.session_state.page == "login":login_page()

elif st.session_state.page == "admin_login": admin_login()

elif st.session_state.page == "admin_dashboard":admin_dashboard()

elif st.session_state.page == "dashboard":dashboard_page() 