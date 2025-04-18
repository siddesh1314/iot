import speech_recognition as sr
import emergency_module



def listen_for_voice_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for voice command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Voice command recognized: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except sr.WaitTimeoutError:
        print("Listening timed out")

    return ""


command = listen_for_voice_command()
if "save me" in command:
    print("Emergency command detected! Calling emergency module...")
    emergency_module.handle_emergency()



sudo apt update
sudo apt install portaudio19-dev python3-pyaudio python3-dev
