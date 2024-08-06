import cv2
import mediapipe as mp
import threading
import queue
import time

# Hand tracking setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Setup for capturing video
cap = cv2.VideoCapture(0)

def hand_tracking(hands_queue, click_queue):
    with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print('Input failed')
                break

            # Flip the image horizontally
            image = cv2.flip(image, 1)

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image.shape[1])
                y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image.shape[0])
                hands_queue.put((x, y))
                
                # Check if index finger and thumb are together
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                distance = ((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2)**0.5
                if distance < 0.05:  # Adjust this threshold as necessary
                    click_queue.put(True)
                    time.sleep(0.2)  # Debounce

            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    hands_queue = queue.Queue()
    click_queue = queue.Queue()
    hand_tracking(hands_queue, click_queue)
