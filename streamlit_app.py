import streamlit as st
import pandas as pd
import plotly.express as px
import io
import cv2
import os
import joblib
from datetime import datetime
from database import register_user, login_user, get_all_records, insert_attendance

# ================= SETUP & THEME ================= #
st.set_page_config(page_title="Smart Attendance System", page_icon="🛡️", layout="wide")

# Modern Professional CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #2c3e50;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ================= SESSION STATE ================= #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Login"

# ================= AUTH PAGES ================= #
def auth_header(title):
    st.markdown(f"<h1 style='text-align:center; color:#2c3e50;'>{title}</h1>", unsafe_allow_html=True)

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_header("🔐 Admin Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if login_user(user, pwd):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        if st.button("New Admin? Register Here"):
            st.session_state.page = "Register"
            st.rerun()

def register_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_header("📝 Admin Registration")
        user = st.text_input("New Username")
        pwd = st.text_input("New Password", type="password")
        if st.button("Register", use_container_width=True):
            if register_user(user, pwd):
                st.success("Account created!")
                st.session_state.page = "Login"
                st.rerun()
            else:
                st.error("Username already taken")
        if st.button("Back to Login"):
            st.session_state.page = "Login"
            st.rerun()

# ================= MAIN DASHBOARD ================= #
def dashboard():
    # Sidebar
    st.sidebar.title("🛡️ Attendance Pro")
    menu = st.sidebar.radio("Navigation", ["📊 Dashboard", "➕ Add User", "📂 Reports"])
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Load Data from MongoDB
    records = get_all_records()
    df = pd.DataFrame(records) if records else pd.DataFrame(columns=['name', 'id', 'time', 'date'])

    if menu == "📊 Dashboard":
        st.title("📊 Attendance Overview")
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Users", df['name'].nunique() if not df.empty else 0)
        m2.metric("Records Found", len(df))
        m3.metric("Status", "System Active", delta="Stable")

        st.divider()

        # Dashboard Camera Integration
        col_cam, col_viz = st.columns([1, 1])
        
        with col_cam:
            st.subheader("🎥 Live Recognition Feed")
            run_engine = st.toggle("Activate Recognition Engine")
            cam_placeholder = st.empty()
            
            if run_engine:
                if not os.path.exists('static/face_recognition_model.pkl'):
                    st.warning("Model not found. Please train the model first.")
                else:
                    model = joblib.load('static/face_recognition_model.pkl')
                    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    cap = cv2.VideoCapture(0)
                    
                    while run_engine:
                        ret, frame = cap.read()
                        if not ret: break
                        
                        faces = face_detector.detectMultiScale(frame, 1.3, 5)
                        for (x, y, w, h) in faces:
                            # Preprocess and Identify
                            face_crop = cv2.resize(frame[y:y+h, x:x+w], (50, 50)).reshape(1, -1)
                            prediction = model.predict(face_crop)[0]
                            
                            # Log Attendance
                            name, uid = prediction.split('_')
                            if insert_attendance(name, uid, datetime.now().strftime("%H:%M:%S"), datetime.now().strftime("%d-%m-%Y")):
                                st.toast(f"✅ Attendance Marked: {name}")

                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
                        
                        cam_placeholder.image(frame, channels="BGR")
                    cap.release()

        with col_viz:
            st.subheader("📈 Analytics")
            if not df.empty:
                fig = px.pie(df, names='name', hole=0.4, title="Attendance Share per User")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Log some attendance to see data visualization.")

    elif menu == "➕ Add User":
        # Integrating your add_user logic here with auto-close feature
        st.title("➕ Enroll New Face")
        name = st.text_input("Name")
        userid = st.text_input("ID")
        
        if st.button("📸 Capture & Train"):
            from app import add_user # Ensure this handles the capture
            with st.spinner("Capturing faces..."):
                add_user(name, userid)
            st.success("User successfully added and model retrained.")

    elif menu == "📂 Reports":
        st.title("📂 Attendance Logs")
        if df.empty:
            st.warning("No records found in database.")
        else:
            search = st.text_input("🔍 Search by Name")
            filtered_df = df[df['name'].str.contains(search, case=False)] if search else df
            st.dataframe(filtered_df, width=1200)
            
            # Export
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV Report", csv, "report.csv", "text/csv")

# ================= ROUTING ================= #
if not st.session_state.logged_in:
    if st.session_state.page == "Login":
        login_page()
    else:
        register_page()
else:
    dashboard()