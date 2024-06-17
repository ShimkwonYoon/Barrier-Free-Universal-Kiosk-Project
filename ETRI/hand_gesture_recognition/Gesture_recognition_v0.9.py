import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key

# 키보드 컨트롤러 초기화
keyboard = Controller()

# Mediapipe 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# OpenCV 비디오 캡처 초기화
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 이전 프레임에서 인식된 손가락 상태를 저장하는 변수
previous_finger_state = ""

# 메인 루프
while True:
    # 비디오 프레임 읽기
    ret, frame = cap.read()

    # 프레임을 RGB로 변환
    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Mediapipe를 통해 손 인식
    results = hands.process(image)

    # 손 인식 결과 확인
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # 손바닥 및 손가락 상태 확인
            landmarks = [[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark]

            # 손가락 개수 카운트
            extended_finger_count = sum([1 for i in range(4) if landmarks[(i+2) * 4][1] < landmarks[(i+2) * 4 - 1][1] and i * 4 not in [1]])
            # extended_finger_count = sum(
            #     [1 for i in range(1, 5) if landmarks[i * 4][1] < landmarks[i * 4 - 2][1] and i * 4 not in [1, 2, 3, 4]])

            # 손가락 상태 판단
            if extended_finger_count >= 2 and landmarks[5][2] > landmarks[6][2] and landmarks[9][2] > landmarks[10][2] and landmarks[13][2] > landmarks[14][2]:
            # if extended_finger_count >= 3:
                finger_state = "Open_palm"

            elif extended_finger_count == 1:
                if landmarks[8][1] < landmarks[12][1] and landmarks[8][1] < landmarks[16][1] and landmarks[8][1] < landmarks[20][1]:
                    finger_label = "Index Finger"
                    finger_landmark = landmarks[8]
                elif landmarks[12][1] < landmarks[8][1] and landmarks[12][1] < landmarks[16][1] and landmarks[12][1] < landmarks[20][1]:
                    finger_label = "Middle Finger"
                    finger_landmark = landmarks[12]
                elif landmarks[16][1] < landmarks[8][1] and landmarks[16][1] < landmarks[12][1] and landmarks[16][1] < landmarks[20][1]:
                    finger_label = "Ring Finger"
                    finger_landmark = landmarks[16]
                else:
                    finger_label = "Little Finger"
                    finger_landmark = landmarks[20]
                finger_state = "pointing"

            elif extended_finger_count == 0:
                finger_state = "Fist"
            else:
                finger_state = "Unknown"

            cv2.putText(frame, str(extended_finger_count), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, finger_state, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


            # 손가락 상태에 따라 동작 수행
            # if finger_state == "Fist":
            #     if previous_finger_state != "Fist":
                    # keyboard.press(Key.esc)
                    # keyboard.release(Key.esc)
                    # cv2.putText(frame, "Fist: Cancel", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if finger_state == "pointing":
                # if previous_finger_state != "pointing":
                x, y = int(finger_landmark[0] * frame.shape[1]), int(finger_landmark[1] * frame.shape[0])
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                cv2.putText(frame, f"Coordinates ({finger_label}): ({x}, {y})", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # elif finger_state == "Open_palm":
            #     if previous_finger_state != "Open_palm":
                    # keyboard.press(Key.enter)
                    # keyboard.release(Key.enter)
                    # cv2.putText(frame, "Open Palm: Enter", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                # cv2.putText(frame, str(extended_finger_count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            previous_finger_state = finger_state

    # 손 인식 결과를 프레임에 그리기
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # 프레임을 출력
    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

