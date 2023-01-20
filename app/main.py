import cv2
from handDetector import HandDetector
import numpy as np
import pyautogui
import time
import os


# os.environ['DISPLAY'] = ':1'


class HandAsMouse:
    def __init__(self):
        self.cam_width, self.cam_height = 640, 480
        self.frame_reduction = 100
        self.p_time = 0
        self.ploc_x, self.ploc_y = 0, 0
        # cloc_x, cloc_y = 0, 0
        self.smoothening = 7
        pyautogui.PAUSE = 0

    def main(self):

        cap = cv2.VideoCapture(0)
        cap.set(3, self.cam_width)
        cap.set(4, self.cam_height)
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
                    (self.frame_reduction, self.frame_reduction),
                    (self.cam_width - self.frame_reduction, self.cam_height - self.frame_reduction),
                    (255, 0, 255),
                    2)

                self.mosue_move(fingers, img, src_height, src_width, x1, y1)

                img = self.mouse_left_click(fingers, hd, img)

                img = self.mouse_right_click(fingers, hd, img)

            c_time = time.time()
            fps = 1 / (c_time - self.p_time)
            self.p_time = c_time

            img = cv2.flip(img, 1)
            cv2.putText(img, f'{int(fps)}',
                        (20, 50), cv2.FONT_HERSHEY_PLAIN,
                        3, (255, 0, 0), 3)

            cv2.imshow("Image", img)
            cv2.waitKey(1)

            # if 0xFF == ord('q'):
            #     cv2.destroyAllWindows()

    def mouse_right_click(self, fingers, hd, img):
        if fingers[4] == 1:
            length, img, line_info = hd.find_distance(8, 12, img)

            # cv2.putText(img, f'{int(length)}',
            #             (20, 50), cv2.FONT_HERSHEY_PLAIN,
            #             3, (255, 0, 0), 3)
            # img = cv2.flip(img, 1)

            # if length < 70:
            #     cv2.circle(
            #         img,
            #         (line_info[4], line_info[5]),
            #         15, (0, 255, 0),
            #         cv2.FILLED)
            pyautogui.click(button='right')
                # time.sleep(1)
        return img


    def mouse_left_click(self, fingers, hd, img):
        if fingers[0] == 1 and fingers[1] != 1:
        # if fingers[1] == 1 and fingers[2] == 1:
            length, img, line_info = hd.find_distance(8, 12, img)

            # cv2.putText(img, f'{int(length)}',
            #             (20, 50), cv2.FONT_HERSHEY_PLAIN,
            #             3, (255, 0, 0), 3)
            # img = cv2.flip(img, 1)

            if length < 70:
                cv2.circle(
                    img,
                    (line_info[4], line_info[5]),
                    15, (0, 255, 0),
                    cv2.FILLED)
                pyautogui.click()
                # time.sleep(1)
        return img

    def mosue_move(self, fingers, img, src_height, src_width, x1, y1):
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(
                x1,
                (self.frame_reduction, self.cam_width - self.frame_reduction),
                (0, src_width))
            y3 = np.interp(
                y1,
                (self.frame_reduction, self.cam_height - self.frame_reduction),
                (0, src_height))

            cloc_x = self.ploc_x + (x3 - self.ploc_x) / self.smoothening
            cloc_y = self.ploc_y + (y3 - self.ploc_y) / self.smoothening

            pyautogui.moveTo(src_width - cloc_x, cloc_y)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            self.ploc_x, self.ploc_y = cloc_x, cloc_y


if __name__ == '__main__':
    ham = HandAsMouse()
    ham.main()
