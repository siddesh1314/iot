# speaker.py
import pyttsx3

# Initialize the engine once
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # You can tweak this if needed

def speak(text):
    if not text:
        return
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")
