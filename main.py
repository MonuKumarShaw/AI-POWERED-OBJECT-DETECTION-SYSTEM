from detection.direction import get_direction
from detection.distance import calculate_distance
from ultralytics import YOLO
from voice.voice_input import get_voice_command
from voice.voice_output import speak

import cv2
import time
import sys
import threading

# =========================
# LOAD YOLO MODEL
# =========================

model = YOLO("yolov8n.pt")

print("Starting AI Vision Assistant...")

# Startup delay
time.sleep(2)

# Greeting
speak("Greetings Boss. AI vision assistant is ready.")

# Wait after greeting
time.sleep(2)

# =========================
# INPUT METHOD SELECTION
# =========================

print("\nChoose input method:")
print("1. Type")
print("2. Speak")

choice = input("Enter 1 or 2: ")

# TYPE INPUT
if choice == "1":

    target_object = input(
        "Type the object name: "
    ).lower()

# VOICE INPUT
elif choice == "2":

    print("Listening for command...")

    target_object = get_voice_command()

# INVALID OPTION
else:

    speak("Invalid option selected.")

    print("Invalid option.")

    time.sleep(2)

    sys.exit()

# =========================
# CHECK INPUT
# =========================

# No command
if target_object == "no_command":

    speak("No command given.")

    time.sleep(2)

    sys.exit()

# Could not understand
if target_object is None:

    speak("I could not understand.")

    time.sleep(2)

    sys.exit()

# =========================
# CLEAN COMMAND
# =========================

words_to_remove = [
    "find",
    "detect",
    "search",
    "for"
]

words = target_object.split()

filtered_words = [
    word for word in words
    if word not in words_to_remove
]

target_object = " ".join(filtered_words)

print("\nTarget Object:", target_object)

# =========================
# OPEN CAMERA
# =========================

cap = cv2.VideoCapture(0)

# Camera initialization
time.sleep(2)

# Show stable camera first
for i in range(30):

    ret, frame = cap.read()

    if ret:

        cv2.imshow(
            "AI Vision Assistant",
            frame
        )

        cv2.waitKey(1)

# =========================
# SPEAKING CONTROL
# =========================

is_speaking = False


def speak_detection(message):

    global is_speaking

    # Prevent multiple speech threads
    if is_speaking:
        return

    is_speaking = True

    speak(message)

    is_speaking = False


# =========================
# SCANNING SPEECH
# =========================

scan_message = (
    f"Scanning the area for {target_object}"
)

scan_thread = threading.Thread(
    target=speak_detection,
    args=(scan_message,),
    daemon=True
)

scan_thread.start()

# =========================
# TIMER VARIABLES
# =========================

start_time = None

# Search timeout timer
search_start_time = time.time()

# Object found flag
object_found = False

# Final values
distance = "--"
direction = "--"

# =========================
# MAIN LOOP
# =========================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # =========================
    # YOLO DETECTION
    # =========================

    results = model(
        frame,
        verbose=False
    )

    for result in results:

        boxes = result.boxes

        for box in boxes:

            cls_id = int(box.cls[0])

            label = model.names[cls_id]

            confidence = float(box.conf[0])

            # Match target object
            if confidence > 0.60 and label == target_object:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                # Object center
                x_center = (x1 + x2) // 2

                # Frame width
                frame_width = frame.shape[1]

                # Direction
                direction = get_direction(
                    x_center,
                    frame_width
                )

                # Object width
                object_width = x2 - x1

                # Distance
                distance = calculate_distance(
                    object_width
                )

                # Draw rectangle
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    3
                )

                # Display label
                cv2.putText(
                    frame,
                    f"{label} {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                # Speak only once
                if not object_found:

                    object_found = True

                    message = (
                        f"Got the {target_object} on your {direction}. "
                        f"Approximately {distance} centimeters away."
                    )

                    # Speak in background
                    speak_thread = threading.Thread(
                        target=speak_detection,
                        args=(message,),
                        daemon=True
                    )

                    speak_thread.start()

                    # Start timer
                    start_time = time.time()

    # =========================
    # SHOW WEBCAM
    # =========================

    cv2.imshow(
        "AI Vision Assistant",
        frame
    )

    # =========================
    # AUTO CLOSE IF NOT FOUND
    # =========================

    if not object_found:

        if time.time() - search_start_time >= 20:

            print("\nObject not found in 20 seconds.")

            speak("Object not found.")

            break

    # =========================
    # CLOSE AFTER DETECTION
    # =========================

    if object_found and start_time is not None:

        if time.time() - start_time >= 10:

            break

    # =========================
    # MANUAL QUIT
    # =========================

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

# =========================
# FINAL RESULT IN TERMINAL
# =========================

print("\n==============================")
print("        FINAL RESULT")
print("==============================")

print(f"Object Given        : {target_object}")
print(f"Target Object       : {target_object}")

if object_found:

    print("Object Status       : Object Detected")
    print(f"Distance From User  : {distance} cm")
    print(f"Direction From User : {direction}")

else:

    print("Object Status       : Object Not Detected")
    print("Distance From User  : --")
    print("Direction From User : --")

print("==============================")

# =========================
# CLEANUP
# =========================

cap.release()

cv2.destroyAllWindows()

print("\nAssistant stopped.")

sys.exit()