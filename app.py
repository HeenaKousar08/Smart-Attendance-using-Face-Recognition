import cv2
import face_recognition
import numpy as np
import streamlit as st
import os
import pandas as pd
from datetime import datetime
from database import init_db, insert_attendance, get_all_records

# Initialize SQLite on startup
init_db()

KNOWN_DIR = "static/known_faces"
os.makedirs(KNOWN_DIR, exist_ok=True)

# ================= PROFESSIONAL UI STYLING ================= #
st.set_page_config(page_title="Attendance Pro", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stButton>button {
        background: linear-gradient(90deg, #2c3e50, #4ca1af);
        color: white; border-radius: 8px; height: 3em; width: 100%;
    }
    .metric-card {
        background: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #2c3e50; color: white; text-align: center;
        padding: 10px; font-size: 14px; z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# ================= CORE FUNCTIONS ================= #

def load_known_data():
    known_encodings, known_names = [], []
    for file in os.listdir(KNOWN_DIR):
        img = face_recognition.load_image_file(os.path.join(KNOWN_DIR, file))
        encoding = face_recognition.face_encodings(img)
        if encoding:
            known_encodings.append(encoding[0])
            known_names.append(os.path.splitext(file)[0])
    return known_encodings, known_names

# ================= NAVIGATION ================= #

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("Control Panel")
    choice = st.radio("Go to:", ["📊 Dashboard", "👤 Enrollment", "📂 Records"])
    st.divider()
    st.info("System: Active\nDatabase: SQLite")

if choice == "📊 Dashboard":
    st.title("🚀 Smart Attendance Dashboard")
    
    # KPI Metrics
    records = get_all_records()
    total_users = len(os.listdir(KNOWN_DIR))
    today_date = datetime.now().strftime("%Y-%m-%d")
    today_logs = len(records[records['date'] == today_date]) if not records.empty else 0

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Registered Faces", total_users)
    with c2: st.metric("Today's Attendance", today_logs)
    with c3: st.metric("System Status", "Healthy")

    st.divider()

    col_cam, col_inst = st.columns([2, 1])
    with col_cam:
        st.subheader("🎥 Recognition Engine")
        run = st.toggle("Activate Live Terminal")
        window = st.empty()
        
        if run:
            known_encodings, known_names = load_known_data()
            if not known_encodings:
                st.warning("Please enroll users first.")
            else:
                cap = cv2.VideoCapture(0)
                while run:
                    ret, frame = cap.read()
                    if not ret: break
                    
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
                    
                    face_locations = face_recognition.face_locations(small_frame)
                    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                    for face_encoding, face_loc in zip(face_encodings, face_locations):
                        matches = face_recognition.compare_faces(known_encodings, face_encoding)
                        name = "Unknown"
                        if True in matches:
                            face_dist = face_recognition.face_distance(known_encodings, face_encoding)
                            name_id = known_names[np.argmin(face_dist)]
                            # Split name and ID for database
                            try:
                                u_name, u_id = name_id.split('_')
                                name = u_name
                                if insert_attendance(u_name, u_id, datetime.now().strftime("%H:%M:%S"), today_date):
                                    st.toast(f"✅ Welcome, {u_name}!")
                            except:
                                name = name_id

                        t, r, b, l = [v*4 for v in face_loc]
                        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
                        cv2.putText(frame, name, (l, t-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
                    
                    window.image(frame, channels="BGR")
                    
                    # Keyboard stop logic
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                cap.release()
                window.empty()

    # ADDED INSTRUCTIONS SECTION
    with col_inst:
        st.markdown("""
        ### 📋 Camera Instructions
        - **To Start:** Switch the toggle to 'On'.
        - **To Stop:** Switch the toggle 'Off' or press the **'Q'** key on your keyboard.
        - Ensure your face is centered and well-lit.
        """)

elif choice == "👤 Enrollment":
    st.title("👤 Face Enrollment")
    
    # ADDED ID NUMBER FIELD
    c_in1, c_in2 = st.columns(2)
    with c_in1:
        name = st.text_input("Enter Full Name")
    with c_in2:
        u_id = st.text_input("Enter ID Number")

    if st.button("Capture Instant Sample"):
        if name and u_id:
            cap = cv2.VideoCapture(0)
            placeholder = st.empty()
            while True:
                ret, frame = cap.read()
                if not ret: break
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if face_recognition.face_locations(rgb):
                    # Saved as Name_ID.jpg
                    cv2.imwrite(f"{KNOWN_DIR}/{name}_{u_id}.jpg", frame)
                    break
                placeholder.image(frame, channels="BGR")
            cap.release()
            placeholder.empty()
            st.success(f"Successfully Enrolled {name} (ID: {u_id})!")
        else: 
            st.error("Please enter both Name and ID.")

elif choice == "📂 Records":
    st.title("📂 Attendance Logs")
    st.dataframe(get_all_records(), use_container_width=True)

# ================= PROFESSIONAL FOOTER ================= #
st.markdown(f"""
    <div class="footer">
        <p> Smart Attendance using Face Recognition | © 2026 | Heena Kousar </p>
    </div>
    """, unsafe_allow_html=True)