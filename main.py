import cv2
import mediapipe as mp
import random


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Falling object
obj_x = random.randint(100, 1180)
obj_y = 0
score = 0

# Game parameters
player_width = 150
player_height = 20
fall_speed = 10

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    player_x = w // 2

    # Process hand landmarks
    if results.multi_hand_landmarks:
        hand_landmarks_list = results.multi_hand_landmarks

        for idx, hand_landmarks in enumerate(hand_landmarks_list):
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            index_tip = hand_landmarks.landmark[8]  # Index finger tip

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            if idx == 0:
                # First hand (usually left) controls player X position
                player_x = x

            if idx == 1:
                # Second hand could control some other logic (optional)
                cv2.putText(img, "Right Hand Detected", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)

            cv2.circle(img, (x, y), 10, (0, 255, 0), -1)

    # Move falling object
    obj_y += fall_speed

    # Draw player bar
    cv2.rectangle(img, (player_x - player_width // 2, h - 50),
                  (player_x + player_width // 2, h - 50 + player_height), (255, 255, 0), -1)

    # Draw falling object
    cv2.circle(img, (obj_x, obj_y), 20, (0, 0, 255), -1)

    # Check collision
    if (h - 70 < obj_y < h - 40) and (player_x - player_width // 2 < obj_x < player_x + player_width // 2):
        score += 1
        obj_y = 0
        obj_x = random.randint(100, 1180)

    # Missed
    elif obj_y > h:
        obj_y = 0
        obj_x = random.randint(100, 1180)
        score -= 1

    # Show score
    cv2.putText(img, f"Score: {score}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    # Display window
    cv2.imshow("Catch Game - Two Hand Controlled", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()

name = "ruvindu"

print(name)
