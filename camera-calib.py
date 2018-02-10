import numpy as np
from matplotlib import pyplot as plt
import sys
import cv2

cap = cv2.VideoCapture(0)


farmid = (338,124)
midleft = (160,195) #len = 100
midmid = (306,194)
midright = (482,193) #len = 238-183
nearleft = (67,414)
nearmid = (326, 410)
nearright = (585,411) #len = 474-392
points = [farmid, midleft, midmid,
          midright, nearleft, nearmid, nearright]

farmidB = ((124,72),(544,151))
midleftB = ((22,157),(215,351)) #len = 100
midmidB = ((240,163),(410,351))
midrightB = ((427,167),(615,351)) #len = 238-183
nearleftB = ((16,370),(186,462))
nearmidB = ((217,365), (439,452))
nearrightB = ((461,370),(632,453)) #len = 474-392
bounds = [farmidB, midleftB, midmidB,
          midrightB, nearleftB, nearmidB, nearrightB]

def drawSquare(b,frame):
    (p1,p2) = b
    (x1,y1) = p1
    (x2,y2) = p2
    cv2.line(frame, (x1,y1),(x1,y2),(255,0,0),5)
    cv2.line(frame, (x2,y1),(x2,y2),(255,0,0),5)
    cv2.line(frame, (x1,y1),(x2,y1),(255,0,0),5)
    cv2.line(frame, (x1,y2),(x2,y2),(255,0,0),5)

ix,iy = -1,-1
def mousepos(event,x,y,flags,param):
    global ix,iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        ix,iy = x,y


while(True):
    ret, frame = cap.read()

    points = [farmid, midleft, midmid,
              midright, nearleft, nearmid, nearright]

    for (x, y) in points:
        cv2.circle(frame, (x, y), 5, (255, 0, 0))
    for bound in bounds:
        drawSquare(bound,frame)

    cv2.imshow("hi", frame)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mousepos)

    cv2.imshow('image', frame)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(ix, iy)
        #print(frame.shape)


# mouse callback function


# Create a black image, a window and bind the function to window
