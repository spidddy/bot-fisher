import numpy as np
import cv2
import time
import mss
import numpy
import pyautogui
time.sleep(5)
def bobber(coord):
    left, top, long = bait[coord]
    pyautogui.moveTo(left, top, duration=1)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(left+30, top+30, duration=long)
    pyautogui.mouseUp(button='left')

sct = mss.mss()
monitor = {"top": 40, "left": 0, "width": 1024, "height": 768}
image = np.array(sct.grab(monitor))
#image = cv2.imread('Screenshot_15.png')
template = cv2.imread("11.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

too_far_away =[(0, 0), (1, 0), (2, 0), (6, 0), (0, 1), (1, 1), (0, 2), (0, 3), (0, 4), (0, 5),
               (0, 6), (0, 7), (0, 8), (0, 9), (1, 8)]
water = []
bait = {(3, 0): (73, 380, 1),
        (4, 0): (73, 490, 0.6),
        (5, 0): (73, 590, 1),
        (2, 1): (138, 280, 0.6),
        (3, 1): (138, 380, 0.4),
        (3, 2): (250, 380, 0.3),
        (4, 1): (138, 480, 0.4),
        (4, 2): (138, 580, 0.4),
        (5, 1): (138, 595, 0.46),
        (1, 2): (247, 175, 0.5),
        (2, 2): (247, 275, 0.3),
        (5, 2): (267, 600, 0.39),
        (1, 3): (364, 184, 0.36),
        (5, 3): (364, 600, 0.39),
        (1, 4): (482, 192, 0.2),
        (1, 6): (650, 170, 0.4),
        (4, 6): (610, 480, 0.101),
        (5, 6): (650, 570, 0.22),
        (4, 7): (750, 484, 0.25),
        (2, 8): (850, 280, 1),
        (1, 7): (750, 170, 1),
        (2, 7): (750, 285, 0.45)}

for i in range(10):
    for j in range(7):
        cv2.rectangle(image,(i*100, j*100+40),(i*100+100,j*100+140),(0,255,0),1)
        text = str(j) + ' ' + str(i)
#        cv2.putText(image, text, (i*100 + 30, j*100 + 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
        segment = image[j*100+40:j*100+140, i*100:i*100+100]
        edges = cv2.Canny(segment, 100, 200)
        mean = np.mean(edges)
        if mean < 10 and (j, i) not in too_far_away:
            print('top=', j, ' left=', i, ' Water')
            water.append((j, i))
        else:
            print('top=', j, ' left=', i, ' No fish here')
print(water)
while True:
    for square in water:
        #square = (1, 2)

        image = np.array(sct.grab({"top": 80, "left": 50, "width": 200, "height": 90}))
        # image = cv2.imread('Screenshot_15.png')
        edges = cv2.Canny(image, 100, 200)
        gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        templ = cv2.imread('icon3.png')
        edges2 = cv2.Canny(templ, 30, 400)
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
        bobber(square)
        time.sleep(1)
        top, left = square
        mon = {'top': top*100+40, 'left': left*100, 'width': 100, 'height': 100}
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
            cv2.imshow('000', edges)
            cv2.moveWindow('000', 400, 800)
            cv2.waitKey(5)
#            trashhold -= 0.001
            if firstmean == 0:
                firstmean = mean
            firstmean = (firstmean + mean)/2
            if mean < minmean:
                minmean = mean

#            print(firstmean, minmean, mean)


            if mean < firstmean - 0.3:
                pyautogui.click(button='left')
                print('КЛЮЕТ')
    #            pyautogui.click(button='left')
    #            time.sleep(5)
                break
        time.sleep(0.1)
        op = 0
        while True:
            op += 1
            print(op)
            image = np.array(sct.grab({"top": 390, "left": 400, "width": 230, "height": 90}))
            gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.7)
            if len(loc[::-1][0]) != 0:
                x = loc[::-1][0][0]
                y = loc[::-1][1][0]
                print(x, y)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                if x < 110:
                    pyautogui.mouseDown(button='left')
                if x > 150:
                    pyautogui.mouseUp(button='left')
            else:
                pyautogui.mouseUp(button='left')
                time.sleep(1)
                break


            cv2.imshow('Bait', image)
            cv2.moveWindow('Bait', 100, 840)
            cv2.waitKey(1)

#cv2.waitKey()
