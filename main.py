import cv2
from handDetector import HandDetector
import numpy as np
import pyautogui
import time


def main():
    cam_width, cam_height = 640, 480
    frame_reduction = 100
    p_time = 0
    ploc_x, ploc_y = 0, 0
    # cloc_x, cloc_y = 0, 0
    smoothening = 7
    pyautogui.PAUSE = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, cam_width)
    cap.set(4, cam_height)
    hd = HandDetector()
    src_width, src_height = pyautogui.size()

    while True:
        success, img = cap.read()

        img = hd.find_hand(img, True)
        lm_list, bbox = hd.find_pos(img)

        if len(lm_list) != 0:
            x1, y1 = lm_list[8][1:]
            # x2, y2 = lm_list[12][1:]

            fingers = hd.fingers_up()
            cv2.rectangle(
                img,
                (frame_reduction, frame_reduction),
                (cam_width - frame_reduction, cam_height - frame_reduction),
                (255, 0, 255),
                2)

            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(
                    x1,
                    (frame_reduction, cam_width - frame_reduction),
                    (0, src_width))
                y3 = np.interp(
                    y1,
                    (frame_reduction, cam_height - frame_reduction),
                    (0, src_height))

                cloc_x = ploc_x + (x3 - ploc_x) / smoothening
                cloc_y = ploc_y + (y3 - ploc_y) / smoothening

                pyautogui.moveTo(src_width - cloc_x, cloc_y)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                ploc_x, ploc_y = cloc_x, cloc_y

            if fingers[1] == 1 and fingers[2] == 1:
                length, img, line_info = hd.find_distance(8, 12, img)
                if length < 40:
                    cv2.circle(
                        img,
                        (line_info[4], line_info[5]),
                        15, (0, 255, 0),
                        cv2.FILLED)
                    pyautogui.click()

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        img = cv2.flip(img, 1)
        cv2.putText(img, f'{int(fps)}',
                    (20, 50), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

        # if 0xFF == ord('q'):
        #     cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
