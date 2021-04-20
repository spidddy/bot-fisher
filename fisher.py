import numpy as np
import cv2
import time
import mss
import numpy
import pyautogui

def bobber(coord):
    left, top, long = bait[coord]
    pyautogui.moveTo(left, top, duration=1)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(470, 200, duration=long)
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
        bobber(square)
        time.sleep(1)
        top, left = square
        mon = {'top': top*100+40, 'left': left*100, 'width': 100, 'height': 100}
        mmax = 0
        fmean = 0
        while True:
            sct = mss.mss()
            img = np.array(sct.grab(mon))
            time.sleep(0.01)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(img, 200, 300)
            mean = np.mean(edges)
            trashhold = 0.85
            if top >= 4:
                trashhold = 0.6
            if fmean == 0:
                fmean = mean
            if fmean - mean > mmax:
                mmax = fmean - mean

            print(mmax, trashhold)


            if fmean - mean > trashhold:
                pyautogui.click(button='left')
                print('КЛЮЕТ')
    #            pyautogui.click(button='left')
    #            time.sleep(5)
                break
        op = 1
        with mss.mss() as sct:
            old_x = 0
            time_wait = 1
            while True:
                img = numpy.array(sct.grab(monitor))
                gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= 0.7)
                op += 1
                print(op)
                for pt in zip(*loc[::-1]):
                    for p in img:
        #                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
                        x = pt[0]
                        print('X coord: ', x)
                        if 400 < x < 600:
                            pyautogui.mouseDown(button='left')
                            if old_x != 0:
                                print('Разница', old_x - x)
                                if old_x - x > 10:
                                    time_wait = time_wait + 0.5
                                if old_x - x < -10 and time_wait > 0.5:
                                    time_wait = time_wait - 0.5
                            else:
                                old_x = x
                            time.sleep(time_wait)
                            print('x===', x)
                            pyautogui.mouseUp(button='left')
                            break
                        else:
                            continue
                    break
                if op > 70:
                    break

#cv2.waitKey()
