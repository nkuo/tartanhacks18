import numpy as np
from matplotlib import pyplot as plt
import sys
import cv2
import io
import os
import time

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

global_labels = ["",False, False, False, False, False, False, False]
index = 0;

def labelDecide(labels):
    if "product" in labels:
        global_labels[0] = "product"
        global_labels[index+1] = True
    else:
        global_labels[index+1] = False
    if "bottle" in labels:
        global_labels[0] = "product"
        global_labels[index+1] = True
    else:
        global_labels[index+1] = False

def drawSquare(b,frame):
    (p1,p2) = b
    (x1,y1) = p1
    (x2,y2) = p2
    cv2.line(frame, (x1,y1),(x1,y2),(255,0,0),5)
    cv2.line(frame, (x2,y1),(x2,y2),(255,0,0),5)
    cv2.line(frame, (x1,y1),(x2,y1),(255,0,0),5)
    cv2.line(frame, (x1,y2),(x2,y2),(255,0,0),5)


def run2():
    print("CV")
    
    cap = cv2.VideoCapture(0)
    client = vision.ImageAnnotatorClient()
    
    farmidB = ((124,72),(544,151))
    midleftB = ((22,157),(215,351)) #len = 100
    midmidB = ((240,163),(410,351))
    midrightB = ((427,167),(615,351)) #len = 238-183
    nearleftB = ((16,370),(186,462))
    nearmidB = ((217,365), (439,452))
    nearrightB = ((461,370),(632,453)) #len = 474-392
    bounds = [farmidB, midleftB, midmidB,
            midrightB, nearleftB, nearmidB, nearrightB]


    while (True):
        ret, frame = cap.read()
        ((x1, y1), (x2, y2)) = bounds[index]
        cropped = frame[y1:y2, x1:x2]
        drawSquare(bounds[index],frame)
        cv2.imwrite("resources/test" + str(index) + ".jpg", cropped)
        file_name = os.path.join(
            os.path.dirname(__file__),
            "resources/test" + str(index) + ".jpg")
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        labels = [x.description for x in labels]
        labelDecide(labels)
        cv2.imshow("hi", frame)
    
        print(global_labels)
    
    
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        index+= 1
        index = index % 7
        big_queue.put(global_labels[0])
        big_queue2.put(global_labels[1:])