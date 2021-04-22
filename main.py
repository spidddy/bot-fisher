import numpy as np
import cv2
import time
import mss
import numpy
import pyautogui
#cv2.waitKey(500)
sct = mss.mss()
template = cv2.imread("11.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]
template2 = cv2.imread("fish.png", cv2.IMREAD_GRAYSCALE)
w2, h2 = template.shape[::-1]

while True:
    image = np.array(sct.grab({"top": 390, "left": 400, "width": 230, "height": 90}))
    gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.7)
    res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    loc2 = np.where(res >= 0.7)
    if len(loc[::-1][0]) != 0:
        x = loc[::-1][0][0]
        y = loc[::-1][1][0]
        x2 = loc2[::-1][0][0]
        y2 = loc2[::-1][1][0]
        print(x, y)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if x < 80:
            pyautogui.mouseDown(button='left')
        if x > 150:
            pyautogui.mouseUp(button='left')

    cv2.imshow('Bait', image)
    cv2.moveWindow('Bait', 100, -240)
    cv2.waitKey(1)