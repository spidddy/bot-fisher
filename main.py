import numpy as np
import cv2
import time
import mss
import numpy
import pyautogui
cv2.waitKey(500)
sct = mss.mss()
image = np.array(sct.grab({"top": 80, "left": 50, "width": 200, "height": 90}))
#image = cv2.imread('Screenshot_15.png')
edges = cv2.Canny(image,100,200)
gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
templ = cv2.imread('icon3.png')
edges2 = cv2.Canny(templ,30,400)
res = cv2.matchTemplate(edges, edges2, cv2.TM_CCORR_NORMED)
loc = np.where(res >= 0.65)
if len(loc[::-1][0]) == 0:
    print('gggggggggggggggggggggg')
    image = np.array(sct.grab({"top": 720, "left": 500, "width": 80, "height": 80}))
    edges = cv2.Canny(image, 100, 200)
    templ = cv2.imread('button.png')
    edges2 = cv2.Canny(templ, 30, 400)
    res = cv2.matchTemplate(edges, edges2, cv2.TM_CCORR_NORMED)
    loc = np.where(res >= 0.65)
    if len(loc[::-1][0]) == 0:
        print('No bait')
        pyautogui.press('i')
        image = np.array(sct.grab({"top": 420, "left": 680, "width": 320, "height": 250}))
        edges = cv2.Canny(image, 100, 200)
        templ = cv2.imread('bait.png')
        edges2 = cv2.Canny(templ, 30, 400)
        res = cv2.matchTemplate(edges, edges2, cv2.TM_CCORR_NORMED)
        loc = np.where(res >= 0.65)
        if len(loc[::-1][0]) == 0:
            print('Bait over')
        else:
            x = loc[::-1][0][0] + 700
            y = loc[::-1][1][0] + 440
            pyautogui.moveTo(x, y, duration=1)
            pyautogui.click(button='right')
        pyautogui.press('i')
        time.sleep(11)
        pyautogui.press('1')

    else:
        print('Oh, yea')
        pyautogui.press('1')
cv2.imshow('ooo1oo', image)
#cv2.imshow('ooooo', edges2)
cv2.waitKey()