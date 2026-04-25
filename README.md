# 🎯 Smart Attendance System using Face Recognition

## 📌 Project Overview

The **Smart Attendance System using Face Recognition** is an AI-based application that automates attendance marking using real-time face detection and recognition. It eliminates manual effort, improves accuracy, and prevents proxy attendance.

---

## 🚀 Features

* 📷 Real-time face detection via webcam
* 🧠 Face recognition using ML-based encoding
* 📝 Automatic attendance marking with timestamp
* 💾 Database integration for storing records
* 🌐 Streamlit-based user interface
* ⚡ Fast, efficient, and user-friendly system

---

## 🛠️ Technologies Used

* Python
* OpenCV
* face_recognition (dlib)
* NumPy
* Pandas
* Streamlit
* SQLite (via database.py)

---

## 📂 Project Structure

```
attendance/
│── __pycache__/            # Compiled Python files
│── .venv/                  # Virtual environment
│── static/                 # Static files (images/data)
│── app.py                  # Core face recognition logic
│── streamlit_app.py        # Streamlit UI application
│── database.py             # Database handling (SQLite)
│── import face_recognition.py   # Face recognition helper script
│── import threading.py     # Threading utility
```

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/smart-attendance-system.git
cd attendance
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

### Option 1: Run Streamlit App (Recommended)

```bash
streamlit run streamlit_app.py
```

### Option 2: Run Core Application

```bash
python app.py
```

---

## 🧠 How It Works

1. The system captures face data using a webcam.
2. Face encodings are generated using the face_recognition library.
3. Encodings are compared with stored data.
4. If a match is found, attendance is recorded.
5. Data is stored in a database with timestamp.

---

## 📊 Output

* Attendance records stored in database
* Includes:

  * Name
  * Date
  * Time

---

## 🎥 Demo

(Add your demo video link here)

---

## 🔮 Future Enhancements

* Cloud deployment (AWS/Heroku)
* Mobile app integration
* Face mask detection
* Multi-user dashboard
* Export attendance reports (Excel/PDF)

---

## 🤝 Contribution

Contributions are welcome! Fork the repo and submit a pull request.

---

## 📜 License

This project is open-source under the MIT License.

---

## 👩‍💻 Author

**Heena Kousar**
M.Sc Data Science Student

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
