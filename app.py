import os
import cv2
import numpy as np
import pickle
import pandas as pd
from flask import Flask, render_template, jsonify, request
from keras_facenet import FaceNet
from mtcnn.mtcnn import MTCNN
from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity
from hostel_db import save_student_to_db, fetch_all_students, create_table
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# -------------------------------
# Load CSV student names
# -------------------------------
def load_student_names():
    try:
        df = pd.read_csv("students.csv")
        return dict(zip(df["matric_no"].astype(str).str.zfill(4), df["name"]))
    except Exception as e:
        print("⚠️ Could not load students.csv:", e)
        return {}

STUDENT_NAMES = load_student_names()

# -------------------------------
# Load AI Models
# -------------------------------
print("🔹 Loading models...")
embedder = FaceNet()
detector = MTCNN()
classifier = load_model("models/best_student_classifier.h5")

with open("models/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)
with open("models/student_embeddings.pkl", "rb") as f:
    student_embeddings = pickle.load(f)
print("✅ Models loaded successfully!")

create_table()

# -------------------------------
# Flask Routes
# -------------------------------
@app.route("/")
def home():
    students = fetch_all_students()  # [(name, matric_no, hall, room), ...]
    students_list = [
        {"name": s[0], "matric_no": s[1], "hall": s[2], "room": s[3]}
        for s in students
    ]
    return render_template("dashboard.html", students=students_list)

@app.route("/students")
def get_students():
    students = fetch_all_students()
    students_list = [
        {"name": s[0], "matric_no": s[1], "hall": s[2], "room": s[3]}
        for s in students
    ]
    return jsonify(students_list)

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/recognize_face", methods=["POST"])
def recognize_face():
    data = request.get_json()
    img_data = data["image"].split(",")[1]
    img_bytes = base64.b64decode(img_data)
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    frame = np.array(img)[:, :, ::-1]  # RGB → BGR for OpenCV

    threshold = 0.6
    detected_student = None

    detections = detector.detect_faces(frame)
    for det in detections:
        x, y, w, h = det["box"]
        face = frame[y:y+h, x:x+w]
        if face.size == 0:
            continue

        face = cv2.resize(face, (160, 160))
        emb = embedder.embeddings(np.expand_dims(face, axis=0))[0]
        preds = classifier.predict(np.expand_dims(emb, axis=0))[0]
        pred_idx = np.argmax(preds)
        pred_label = le.inverse_transform([pred_idx])[0]
        stored_emb = student_embeddings.get(pred_label)

        if stored_emb is None:
            continue

        sim = cosine_similarity([emb], [stored_emb])[0][0]
        if sim >= threshold:
            matric_no = str(pred_label).strip().zfill(4)  # ensure leading zeros
            name = STUDENT_NAMES.get(matric_no, matric_no)  # real name from CSV
            hall, room, new = save_student_to_db(name, matric_no)
            detected_student = {
                "name": name,
                "matric_no": matric_no,
                "hall": hall,
                "room": room,
                "new": new
            }
            break

    return jsonify(detected_student or {})

if __name__ == "__main__":
    app.run(debug=True)
