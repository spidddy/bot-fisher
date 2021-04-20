import numpy as np
import cv2
from mss.linux import MSS as mss
from PIL import Image
import time
import pyautogui as pg
import imutils
import mss
import numpy
import pyautogui

template = cv2.imread("11.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

color_yellow = (0,255,255)

mon = {'top': 80, 'left': 350, 'width': 100, 'height': 100}

def process_image(original_image):

    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    return processed_image

def ss():
    op = 1

    with mss.mss() as sct:
        old_x = int(0)
        time_sleeps = int(1.5)

        monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

        while "Screen capturing":
            last_time = time.time()

            img = numpy.array(sct.grab(monitor))


            gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.7)
            op += 1
            print (op)

            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
                for p in img:

                    pts = (pt[0],pt[1])
                    x = (pt[0])
                    y = (pt[1])
                    #print(x)
                    if 100 < x < 500:
                        pyautogui.mouseDown(button='left')

                        if old_x!=0:
                            print('Разница',old_x - x)
                            if old_x-x>30:
                                time_sleeps=time_sleeps+1
                            if old_x - x < -30:
                                time_sleeps=time_sleeps-1
                        else:
                            old_x = x
                        time.sleep(time_sleeps)
                        print('x===',x)



                        print('Время сна',time_sleeps)
                        pyautogui.mouseUp(button='left')
                        x = 0
                        break
                    else:
                        x = 0
                        continue
                    break
                else:
                        continue
                break
            key = cv2.waitKey(1)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
            if op > 70:
                return

def screen_record():
    sct = mss.mss()
    last_time = time.time()

    while(True):
        img = sct.grab(mon)
        print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()

        img = np.array(img)
        processed_image = process_image(img)
        mean = np.mean(processed_image)
        print('mean = ', mean)

        if  mean <= float(0.11):
            print('SSSSSSSS ')
            pyautogui.click(button='left')
            break
            return
        else:
            time.sleep(0.01)
            continue
        return
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

while "Черный":
    #pyautogui.moveTo(831, 475,duration=1)
    time.sleep(6)
    pyautogui.moveTo(431,175,duration=1)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(470,200,duration=1)
    pyautogui.mouseUp(button='left')
    time.sleep(2)
    screen_record()
    time.sleep(0.01)
    ss()
    cv2.waitKey()