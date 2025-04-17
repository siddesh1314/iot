# main.py

import cv2
import time
import pytesseract
import ocr_module
import face_module
from picamera2 import Picamera2
import face_recognition
from currency_classification import CurrencyClassifier

def detect_content_type(img, currency_model, threshold=0.7):
    # Step 1: Currency detection first
    result = currency_model.classify(img)
    if result:
        label = result['label']
        confidence = result['confidence']
        print(f"Currency prediction: {label} ({confidence:.2f})")
        if confidence >= threshold:
            return "currency"

    # Step 2: Face detection
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    if len(face_locations) > 0:
        return "face"

    # Step 3: OCR/Text detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_text = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(gray_text)
    if len(text.strip()) >= 10:
        print(text)
        return "text"

    return "unknown"


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
            content_type = detect_content_type(img, currency_model)

            if content_type == "face":
                print("Detected: face")
                face_module.identify_face(img)

            elif content_type == "text":
                print("Detected: text printed above")
                #ocr_module.read_text(img)

            elif content_type == "currency":
                print("currency prediction printed above")
                
            else:
                print("unknown")

        time.sleep(5)
#Run main.py as a systemd service or cron job for auto-start