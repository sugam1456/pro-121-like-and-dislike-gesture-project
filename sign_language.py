import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4
finger_fold_status = []
lm_list = []
hand_landmark= []

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    results = hands.process(img)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            lm_list = []  # Clear lm_list for each frame
            # Accessing the landmarks by their position
            for id, lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)

            for tip in finger_tips:
                x, y = int(lm_list[tip].x * w), int(lm_list[tip].y * h)
                cv2.circle(img, (x, y), 15, (255, 0, 0), cv2.FILLED)

                if tip - 2 >= 0 and len(lm_list) > tip - 2:
                    if lm_list[tip].x < lm_list[tip - 3].x:
                        cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                        finger_fold_status.append(True)
                    else:
                        finger_fold_status.append(False)

    if all(finger_fold_status) and len(lm_list) > thumb_tip:
        if (thumb_tip - 2 >= 0 and len(lm_list) > thumb_tip - 2 and
                lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y):
                 print("LIKE")
                 cv2.putText(img, "Like", (20, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

        if (thumb_tip - 2 >= 0 and len(lm_list) > thumb_tip - 2 and
                lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y):
                 print("DISLIKE")
                 cv2.putText(img, "DisLike", (20, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    mp_draw.draw_landmarks(img, hand_landmark,
                           mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec((0, 0, 255), 2, 2),
                           mp_draw.DrawingSpec((0, 255, 0), 4, 2))

    cv2.imshow("hand tracking", img)
    cv2.waitKey(1)