import cv2
import numpy as np
import time
import subprocess
import pytesseract
import pyttsx3
import ocr_module
import face_module
from picamera2 import Picamera2

def detect_content_type(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Face detection
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    if len(faces) > 0:
        return "face"

    # OCR detection
    # Optional preprocessing
    gray_text = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(gray_text)
    print("Detected text:", text.strip())  # DEBUG

    if len(text.strip()) >= 2:
        return "text"
    else:
        return "currency"


if __name__ == "__main__":
    print("Smart Assistant Running...")

    # Initialize Pi camera
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
    picam2.start()

    while True:
        # Capture frame from Pi camera
        img = picam2.capture_array()

        if img is not None:
            content_type = detect_content_type(img)

            if content_type == "face":
                print("face")
                subprocess.run(["python", "face_module.py"])  # Run face recognition as standalone
            elif content_type == "text":
                print("text")
                ocr_module.read_text(img)
            else:
                print("currency")
                cv2.imwrite("captured_image.jpg", img)
                subprocess.run(["python", "currency_classification.py", "captured_image.jpg"])

        time.sleep(5)
