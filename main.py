import numpy as np
import cv2
import time
import mss
import numpy
import pyautogui

if __name__ == '__main__':
    def nothing(*arg):
        pass

value = 00
image = cv2.imread('dark.png')
sct = mss.mss()
monitor = {"top": 40, "left": 0, "width": 1024, "height": 768}
cv2.namedWindow( "result" ) # создаем главное окно
cv2.namedWindow( "result2" ) # создаем главное окно
cv2.namedWindow( "settings" ) # создаем окно настроек

#cap = video.create_capture(0)
# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
crange = [0,0,0, 0,0,0]

while True:
    #    image = np.array(sct.grab(monitor))
    image = cv2.imread('dark.png')
    image2 = cv2.imread('light.png')
    #    flag, img = cap.read()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)
    thresh2 = cv2.inRange(hsv2, h_min, h_max)
    cv2.imshow('result', thresh)
    cv2.imshow('result2', thresh2)
    ch = cv2.waitKey(5)
    if ch == 27:
        break
image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
b, g, r = cv2.split(image)
b[b*2 > (r+g)*1.5] = 255
# lim = 255 - value
# v[v > lim] = 255
# v[v <= lim] += value
lower_blue = np.array([70, 0, 0])
upper_blue = np.array([255, 40, 40])

final_hsv = cv2.merge((b, g, r))
z = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
mask = cv2.inRange(final_hsv, lower_blue, upper_blue)

# Bitwise-AND mask and original image
# res = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow('mask', mask)
#cv2.imshow('res', res)
cv2.waitKey(1)
too_far_away =[(0, 0), (1, 0), (2, 0), (6, 0), (0, 1), (1, 1), (0, 2), (0, 3),
               (0, 7), (0, 8), (0, 9), (1, 8)]

template = cv2.imread("11.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]
template2 = cv2.imread("fish.png", cv2.IMREAD_GRAYSCALE)
w2, h2 = template.shape[::-1]
left_border = 100
right_border = 150
fish = 0
water =[]
for i in range(10):
    for j in range(7):
        cv2.rectangle(image, (i * 100, j * 100 + 40), (i * 100 + 100, j * 100 + 140), (0, 255, 0), 1)
        text = str(j) + ' ' + str(i)
        cv2.putText(image, text, (i*100 + 30, j*100 + 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
        segment = mask[j * 100 + 40:j * 100 + 140, i * 100:i * 100 + 100]
        mean = np.mean(segment)
        print(mean)
        if mean < 8 and (j, i) not in too_far_away:
            print('top=', j, ' left=', i, ' Water')
            cv2.putText(image, 'W', (i * 100 + 30, j * 100 + 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
            water.append((j, i))
        else:
            print('top=', j, ' left=', i, ' No fish here')
        cv2.imshow('water', mask)
        cv2.moveWindow('water', 30, -900)
cv2.waitKey()