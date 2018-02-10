import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
import cv2
import sys
# Python program for Detection of a
# specific color(blue here) using OpenCV with Python

import cv2
import numpy as np

def blueMask (frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([30, 150, 50])
    upper_red = np.array([255, 255, 180])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    return res

def leftBound(img):
    thres = 10
    for x in [t+5 for t in range(len(img[0])-10)]:
        count = 0
        for xmod in range(-1,1):
            for y in range(len(img)):
                if img[y][x+xmod] > 0:
                    count+=1
        if count > thres:
            return x

def rescale(v1,v2,scale):
    mean = (v1+v2)/2
    v1 = (mean-v1)*scale + v1
    v2 = (mean-v2)*scale + v2
    return (int(v1),int(v2))


cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    frame = blueMask(frame)
    edges = cv2.Canny(frame, 100, 200)

    bounds = []
    pic = edges
    for i in range(4):
        bounds.append(leftBound(pic))
        rows, cols = edges.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
        pic = cv2.warpAffine(pic, M, (cols, rows))

    #print(0,bounds)
    bounds[2] = 640 - bounds[2]
    bounds[3] = 480 - bounds[3]
    (bounds[0],bounds[2]) = rescale(bounds[0],bounds[2],1.5)
    (bounds[1], bounds[3]) = rescale(bounds[1], bounds[3], 1.5)
    #print(1,bounds)

    cv2.line(edges, (bounds[0], 0), (bounds[0], 480), (255, 0, 0), 5)
    cv2.line(edges, (bounds[2], 0), (bounds[2], 480), (255, 0, 0), 5)
    cv2.line(edges, (0, bounds[1]), (640, bounds[1]), (255, 0, 0), 5)
    cv2.line(edges, (0, bounds[3]), (640, bounds[3]), (255, 0, 0), 5)
    cv2.imshow("hi", edges)



    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



"""

# OPEN CAMERA
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

"""