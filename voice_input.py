import speech_recognition as sr
from voice.voice_output import speak

recognizer = sr.Recognizer()

def get_voice_command():

    with sr.Microphone() as source:

        # AI prompt
        speak("Speak now.")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        try:

            # Wait 10 seconds for user
            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )

            command = recognizer.recognize_google(
                audio
            )

            command = command.lower()

            print("You said:", command)

            return command

        # No voice within 10 sec
        except sr.WaitTimeoutError:

            print("No command given.")

            speak("No command given.")

            return "no_command"

        # Voice not understood
        except sr.UnknownValueError:

            print("Could not understand.")

            speak("I could not understand.")

            return None

        # Internet issue
        except sr.RequestError:

            print("Internet connection issue.")

            speak("Internet connection issue.")

            return None