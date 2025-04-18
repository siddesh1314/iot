# emergency_module.py

def handle_emergency():
    print("🚨 Emergency action triggered!")
    # You can add logic here like sending SMS, activating camera, etc.


import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Device {index}: {name}")
