import math
import time

from mediapipe import solutions as mps
import cv2


class HandDetector:
    tip_ids = [4, 8, 12, 16, 20]

    def __init__(self, static_image_mode=False,
                 max_num_hands=1,
                 model_complexity=1,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):

        self.lmList = None
        self.results = None
        self.mpHands = mps.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mpDraw = mps.drawing_utils

    def find_hand(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_mhl in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, hand_mhl,
                        self.mpHands.HAND_CONNECTIONS
                    )
        return img

    def find_pos(self, img, draw=True):
        xList, yList, bbox = [], [], []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            hand_landmarks = self.results.multi_hand_landmarks[0]
            for h_id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([h_id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax, ymin, ymax = min(xList), max(xList), min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
            if draw:
                cv2.rectangle(
                    img,
                    (xmin - 20, ymin - 20),
                    (xmax + 20, ymax + 20),
                    (0, 255, 0),
                    2
                )

        return self.lmList, bbox

    def find_distance(self, p1, p2, img, draw=True, r=15, t=3):

        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

    def fingers_up(self):

        fingers = []
        # Thumb
        if self.lmList[self.tip_ids[0]][1] < self.lmList[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for f_id in range(1, 5):
            if self.lmList[self.tip_ids[f_id]][2] < self.lmList[self.tip_ids[f_id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def finger_like(self):
        # print(self.lmList[4][2], self.lmList[8][2])
        if self.lmList[4][2] < self.lmList[8][2]:
            print(True, self.lmList[4][1], self.lmList[8][2])

            return True
        else:
            print(False, self.lmList[4][1], self.lmList[8][2])

            return False
