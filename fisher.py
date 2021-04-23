import numpy as np
import cv2
import time
import mss
import pyautogui

"""
Бот рыболов для Albion online
"""

pyautogui.moveTo(30, 30, duration=1)
pyautogui.click(button='left')


def bobber(coord):
    left, top, long = bait[coord]
    pyautogui.moveTo(left, top, duration=1)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(left + 30, top + 30, duration=long)
    pyautogui.mouseUp(button='left')


sct = mss.mss()
monitor = {"top": 40, "left": 0, "width": 1024, "height": 768}
image = np.array(sct.grab(monitor))
template = cv2.imread("11.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]
template2 = cv2.imread("fish.png", cv2.IMREAD_GRAYSCALE)
w2, h2 = template.shape[::-1]
left_border = 100
right_border = 150
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# последующие переменные определяют границы воды

lower_blue = np.array([0, 23, 25])
upper_blue = np.array([255, 164, 255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)

too_far_away = [(0, 0), (1, 0), (2, 0), (6, 0), (0, 1), (1, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                (0, 6), (0, 7), (0, 8), (0, 9), (1, 8), (1, 9), (2, 9)]
water = []
bait = {(3, 0): (73, 380, 1),
        (4, 0): (73, 490, 0.65),
        (5, 0): (73, 590, 1),
        (2, 1): (138, 280, 0.6),
        (3, 1): (138, 380, 0.4),
        (3, 2): (250, 380, 0.2),
        (3, 3): (350, 380, 0.1),
        (3, 6): (650, 380, 0.45),
        (4, 1): (138, 480, 0.43),
        (4, 2): (138, 580, 0.33),
        (4, 3): (370, 480, 0.19),
        (4, 4): (450, 480, 0.1),
        (5, 1): (150, 580, 0.5),
        (1, 2): (247, 175, 0.5),
        (2, 2): (247, 275, 0.3),
        (5, 2): (267, 600, 0.39),
        (1, 3): (364, 184, 0.36),
        (5, 3): (364, 600, 0.3),
        (5, 4): (454, 600, 0.25),
        (1, 4): (482, 192, 0.2),
        (1, 6): (650, 170, 0.4),
        (4, 6): (610, 480, 0.1),
        (5, 5): (550, 570, 0.22),
        (6, 5): (550, 570, 0.33),
        (6, 6): (650, 670, 0.4),
        (5, 6): (650, 570, 0.22),
        (4, 7): (750, 484, 0.25),
        (2, 8): (850, 280, 1),
        (3, 8): (850, 380, 0.5),
        (3, 9): (950, 380, 0.8),
        (4, 8): (850, 480, 0.5),
        (4, 9): (950, 480, 1),
        (1, 7): (750, 170, 1),
        (2, 7): (750, 285, 0.45)}

for i in range(10):
    for j in range(7):
        segment = mask[j * 100 + 40:j * 100 + 140, i * 100:i * 100 + 100]
        mean = np.mean(segment)
        if mean < 8 and (j, i) not in too_far_away:
            water.append((j, i))

while True:
    for square in water:
        # square = (4, 2)

        image = np.array(sct.grab({"top": 80, "left": 50, "width": 200, "height": 90}))
        edges = cv2.Canny(image, 100, 200)
        gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        templ = cv2.imread('icon3.png')
        edges2 = cv2.Canny(templ, 30, 400)
        res = cv2.matchTemplate(edges, edges2, cv2.TM_CCORR_NORMED)
        loc = np.where(res >= 0.65)
        if len(loc[::-1][0]) == 0:
            image = np.array(sct.grab({"top": 720, "left": 500, "width": 80, "height": 80}))
            edges = cv2.Canny(image, 100, 200)
            templ = cv2.imread('button.png')
            edges2 = cv2.Canny(templ, 30, 400)
            res = cv2.matchTemplate(edges, edges2, cv2.TM_CCORR_NORMED)
            loc = np.where(res >= 0.65)
            if len(loc[::-1][0]) == 0:
                pyautogui.press('i')
                image = np.array(sct.grab({"top": 420, "left": 680, "width": 320, "height": 250}))
                edges = cv2.Canny(image, 100, 200)
                templ = cv2.imread('bait.png')
                edges2 = cv2.Canny(templ, 30, 400)
                res = cv2.matchTemplate(edges, edges2, cv2.TM_CCORR_NORMED)
                loc = np.where(res >= 0.65)
                if len(loc[::-1][0]) != 0:
                    x = loc[::-1][0][0] + 700
                    y = loc[::-1][1][0] + 440
                    pyautogui.moveTo(x, y, duration=1)
                    pyautogui.click(button='right')
                pyautogui.press('i')
                time.sleep(11)
                pyautogui.press('1')

            else:
                pyautogui.press('1')
        bobber(square)
        time.sleep(1)
        top, left = square
        mon = {'top': top * 100 + 40, 'left': left * 100, 'width': 100, 'height': 100}
        mmax = 0
        firstmean = 0
        minmean = 100
        trashhold = 0

        while True:
            sct = mss.mss()
            img = np.array(sct.grab(mon))
            time.sleep(0.03)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(img, 200, 300)
            mean = np.mean(edges)
            name = str(square[0]) + str(square[1])
            cv2.imshow(name, edges)
            cv2.moveWindow(name, 400, 800)
            cv2.waitKey(5)
            if firstmean == 0:
                firstmean = mean
            firstmean = int((firstmean + mean) * 50) / 100

            if mean < minmean:
                minmean = mean
            if mean < firstmean - 0.25:
                pyautogui.click(button='left')
                break
        time.sleep(0.3)
        op = 0
        fish = 0
        cv2.destroyWindow(name)
        while True:
            image = np.array(sct.grab({"top": 390, "left": 400, "width": 230, "height": 90}))
            gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.7)
            res = cv2.matchTemplate(gray_frame, template2, cv2.TM_CCOEFF_NORMED)
            loc2 = np.where(res >= 0.7)
            if len(loc[::-1][0]) != 0:
                x = loc[::-1][0][0]
                y = loc[::-1][1][0]
                x2 = loc2[::-1][0][0]
                y2 = loc2[::-1][1][0]
                if fish == 0:
                    fish = x2

                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.rectangle(image, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 3)
                if x < left_border or x2 < fish:
                    pyautogui.mouseDown(button='left')
                if x > right_border:
                    pyautogui.mouseUp(button='left')
                fish = x2
            else:
                pyautogui.mouseUp(button='left')
                time.sleep(1)
                break
