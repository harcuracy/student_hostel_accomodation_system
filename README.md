# 🧠 Student Hostel Accommodation System (Face Recognition)

A **Deep Learning–powered student accommodation management system** built with **Python, Flask, and computer vision**.  
This project uses **face recognition** to verify students during hostel room allocation.

---

## 🚀 Features
- 🧑‍🎓 **Student face registration and recognition**
- 🏠 **Automated hostel room assignment**
- 🔐 **Secure student verification using Deep Learning**
- 🗃️ **Database-backed system with persistent storage**
- 🌐 **Simple web-based user interface**

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/harcuracy/student_hostel_accomodation_system.git
cd student_hostel_accomodation_system
```

### 2️⃣ Create a virtual environment
```bash
uv venv --python 3.12
```

### 3️⃣ Install dependencies
```bash
uv pip install -r requirements.txt
```

### 4️⃣ Run the application
```bash
python app.py
```

---

## 🌐 Usage
Once the server starts, open your browser and go to:
```
http://127.0.0.1:5000
```

You’ll see the **Student Hostel Accommodation System** running locally.

You can:
- Assign rooms automatically

---

## 🧠 Deep Learning Model
This system uses a **face recognition model** built with:
- **TensorFlow / Keras** for model training  
- **OpenCV** for image capture and preprocessing  
- **FaceNet / DeepFace** (depending on configuration) for feature extraction and matching

The model identifies students by comparing their facial embeddings with those stored in the database.

---

---

## 🧑‍💻 Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default)
- **Deep Learning:** TensorFlow / Keras, OpenCV, DeepFace
- **Environment Management:** uv + venv (Python 3.12)

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Author
**Harcuracy**  
📧 akandesoji4christ@gmail.com  
🔗 [GitHub Profile](https://github.com/harcuracy)
