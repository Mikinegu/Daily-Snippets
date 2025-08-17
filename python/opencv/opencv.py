import cv2
import mediapipe as mp
import serial
import time

# ==== Arduino Serial Setup ====
arduino = serial.Serial(port='COM11', baudrate=9600, timeout=1)  # Change COM to your port
time.sleep(2)  # Wait for Arduino to reset

# ==== MediaPipe Setup ====
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
thumb_tip = 4

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Mirror view
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            fingers = []

            # ---- Thumb ----
            if lm[thumb_tip].x < lm[thumb_tip - 1].x:  # Simple check for right hand
                fingers.append(1)
            else:
                fingers.append(0)

            # ---- Other 4 fingers ----
            for tip in finger_tips:
                if lm[tip].y < lm[tip - 2].y:  # Tip is above knuckle
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Create LED state (only 4 LEDs: Index–Pinky)
            led_state = "".join(str(f) for f in fingers[1:])  # Skip thumb
            print("Fingers:", fingers, "→ LEDs:", led_state)

            # Send to Arduino
            arduino.write((led_state + "\n").encode())  # Send with newline

            # Draw landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
