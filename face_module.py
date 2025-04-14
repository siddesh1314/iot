import face_recognition
import cv2
import numpy as np
import pickle
import pyttsx3

# Load face encodings once
print("[INFO] Loading encodings...")
with open("encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())

known_face_encodings = data["encodings"]
known_face_names = data["names"]

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def identify_face(img):
    cv_scaler = 4

    # Resize and convert
    resized_frame = cv2.resize(img, (0, 0), fx=(1 / cv_scaler), fy=(1 / cv_scaler))
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
        print(f"[INFO] Recognized: {name}")
        engine.say(name)
        engine.runAndWait()

    if not face_names:
        print("[INFO] No known face detected.")
