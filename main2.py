# main.py

import cv2
import time
import pytesseract
import ocr_module
import face_module
from picamera2 import Picamera2
import face_recognition
from currency_classification import CurrencyClassifier

def detect_content_type(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    if len(face_locations) > 0:
        return "face"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_text = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(gray_text)

    # More conservative check for text
    if len(text.strip()) >= 10:
        return "text"

    return "currency"

if __name__ == "__main__":
    print("Smart Assistant Running...")

    # Initialize Pi camera
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
    picam2.start()

    # Load the currency model once
    currency_model = CurrencyClassifier()

    while True:
        img = picam2.capture_array()

        if img is not None:
            content_type = detect_content_type(img)

            if content_type == "face":
                print("Detected: face")
                face_module.identify_face(img)

            elif content_type == "text":
                print("Detected: text")
                ocr_module.read_text(img)

            else:
                print("Detected: currency")
                predictions = currency_model.classify(img)
                for label in predictions:
                    print(f"{label['label']}: {label['value']:.2f}")

        time.sleep(5)
#Run main.py as a systemd service or cron job for auto-start