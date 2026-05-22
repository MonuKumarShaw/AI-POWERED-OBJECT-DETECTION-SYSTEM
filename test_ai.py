import ollama
import speech_recognition as sr
import pyttsx3

# =========================
# TEXT TO SPEECH
# =========================

engine = pyttsx3.init()

def speak(text):

    print("\nAI:", text)

    engine.say(text)

    engine.runAndWait()

# =========================
# SPEECH RECOGNITION
# =========================

recognizer = sr.Recognizer()

def listen():

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print("You:", text)

        return text.lower()

    except:

        return None

# =========================
# STARTUP
# =========================

speak("Greetings Boss. Real time AI assistant is online.")

# =========================
# MAIN LOOP
# =========================

while True:

    user_input = listen()

    if user_input is None:

        continue

    # EXIT COMMAND
    if (
        "exit" in user_input
        or "stop" in user_input
        or "bye" in user_input
    ):

        speak("Shutting down. Goodbye Boss.")

        break

    try:

        response = ollama.chat(

            model='tinyllama',

            messages=[
                {
                    'role': 'user',
                    'content': user_input
                }
            ]
        )

        ai_reply = response[
            'message'
        ]['content']

        speak(ai_reply)

    except Exception as e:

        print("Error:", e)

        speak(
            "Sorry Boss. Something went wrong."
        )