import pyttsx3

def speak(text):

    engine = pyttsx3.init()

    # Slower speed
    engine.setProperty('rate', 180)

    engine.say(text)

    engine.runAndWait()

    engine.stop()