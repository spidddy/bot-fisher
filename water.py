import numpy as np
import cv2
import time
import mss
import numpy
import pyautogui
import pyglet
import random
from collections import deque

import matplotlib.pyplot as plt  # $ pip install matplotlib
import matplotlib.animation as animation

npoints = 30
x = deque([0], maxlen=npoints)
y = deque([0], maxlen=npoints)
fig, ax = plt.subplots()
[line] = ax.step(x, y)


def update(dy):
    x.append(x[-1] + 1)  # update data
    y.append(y[-1] + dy)

    line.set_xdata(x)  # update plot data
    line.set_ydata(y)

    ax.relim()  # update axes limits
    ax.autoscale_view(True, True, True)
    return line, ax


def data_gen():
    while True:
        yield 1 if random.random() < 0.5 else -1


ani = animation.FuncAnimation(fig, update, data_gen)
plt.show()