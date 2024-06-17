import cv2
import mediapipe as mp
import serial
import time

my_serial = serial.Serial('/dev/ttyS3', baudrate=115200, timeout=1.0)
time.sleep(2.0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    ret, frame = cap.read()
    #frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = [[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark]

            extended_finger_count = sum([1 for i in range(4) if landmarks[(i+2) * 4 - 1][1] < landmarks[(i+2) * 4 - 2][1] and i * 4 not in [1]])

            x, y = int(((landmarks[9][0] + landmarks[0][0])/2) * frame.shape[1]), int(((landmarks[9][1] + landmarks[0][1])/2) * frame.shape[0])

            if extended_finger_count >= 1 and landmarks[5][2] > landmarks[6][2] and landmarks[9][2] > landmarks[10][2] and landmarks[13][2] > landmarks[14][2]:
                finger_state = "Open_palm"
                click = 0
            elif extended_finger_count == 0:
                finger_state = "Fist"
                click = 1
            else:
                finger_state = "Unknown"
                click = 3

            fingerx1 = int(hand_landmarks.landmark[4].x * 100 )
            fingerx2 = int(hand_landmarks.landmark[8].x * 100 )
            fingery1 = int(hand_landmarks.landmark[4].y * 100 )
            fingery2 = int(hand_landmarks.landmark[8].y * 100 )                
            dist = abs(fingerx1 - fingerx2)+abs(fingery1 - fingery2)
                
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            cv2.putText(frame, f"Coordinates : ({x}, {y}, {dist})", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, finger_state, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            sendData = f"!{x}@{y}#{click}${dist}^\n"
            my_serial.write( sendData.encode() )

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

