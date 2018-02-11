import threading
import queue
big_queue=queue.Queue()
big_queue2=queue.Queue()
from ui import *
from cloudloop2 import *

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

global_labels = ["", False, False, False, False, False, False, False]
index = 0;


def labelDecide(labels):
    if "product" in labels:
        global_labels[0] = "product"
        global_labels[index + 1] = True
    else:
        global_labels[index + 1] = False
    if "bottle" in labels:
        global_labels[0] = "product"
        global_labels[index + 1] = True
    else:
        global_labels[index + 1] = False


def drawSquare(b, frame):
    (p1, p2) = b
    (x1, y1) = p1
    (x2, y2) = p2
    cv2.line(frame, (x1, y1), (x1, y2), (255, 0, 0), 5)
    cv2.line(frame, (x2, y1), (x2, y2), (255, 0, 0), 5)
    cv2.line(frame, (x1, y1), (x2, y1), (255, 0, 0), 5)
    cv2.line(frame, (x1, y2), (x2, y2), (255, 0, 0), 5)


def run2():
    print("CV")

    cap = cv2.VideoCapture(0)
    client = vision.ImageAnnotatorClient()

    farmidB = ((124, 72), (544, 151))
    midleftB = ((22, 157), (215, 351))  # len = 100
    midmidB = ((240, 163), (410, 351))
    midrightB = ((427, 167), (615, 351))  # len = 238-183
    nearleftB = ((16, 370), (186, 462))
    nearmidB = ((217, 365), (439, 452))
    nearrightB = ((461, 370), (632, 453))  # len = 474-392
    bounds = [farmidB, midleftB, midmidB,
              midrightB, nearleftB, nearmidB, nearrightB]

    while (True):
        ret, frame = cap.read()
        ((x1, y1), (x2, y2)) = bounds[index]
        cropped = frame[y1:y2, x1:x2]
        drawSquare(bounds[index], frame)
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
        index += 1
        index = index % 7
        big_queue.put(global_labels[0])
        big_queue2.put(global_labels[1:])


# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import threading
import numpy as np
from PIL import ImageTk
import PIL.Image
import math


class contents(object):
    def __init__(self, contents, color="black"):
        self.contents = contents
        self.texts = ""
        self.color = color
        self.count = 0

    def filt(self, data):
        if data.time % 1 == 0 and (data.time // 1) < len(self.contents):
            self.texts += self.contents[data.time // 1]
        if self.texts[-1] == " ":
            self.count += 1
        if self.count != 0 and self.count % 5 == 0:
            self.texts += "\n"
            self.count += 1
        if data.time // 1 == len(self.contents):
            return

    def draw(self, canvas, data):
        canvas.create_text(data.width / 2, 4.25 * data.height / 5, text=self.texts, font="Point 40", fill=self.color)


class text(object):
    def __init__(self, x, y, contents, font, color="black"):
        self.x = x
        self.y = y
        self.contents = contents
        self.font = font
        self.color = color

    def move(self, speed):
        self.font += speed

    def draw(self, canvas, data):
        canvas.create_text(self.x, self.y, text=self.contents, font="Point %d" % (self.font), fill=self.color)


def modeAdjust(s, bools, data):
    n = -1
    for i in range(-1, -8, -1):
        if bools[i] == True:
            n = i
    if n == 0:
        data.flag1 = True

    if s == "bag":
        data.situation = 2
    if s == "bottle":
        data.situation = 1
    if data.situation == 1 and n == 1:
        data.flag3 = True
    if data.situation == 1 and n != 1:
        data.flag5 = True
    if data.situation == 2 and n == 2:
        data.flag3 = True
    if data.situation == 2 and n != 2:
        data.flag5 = True
    if data.situation == 2 and n == 5:
        data.flag4 = True
    if data.situation == 2 and n != 5:
        data.flag6 = True
    if data.situation == 1 and n == 4:
        data.flag4 = True
    if data.situation == 1 and n != 4:
        data.flag6 = True


####################################
# customize these functions
####################################

def init(data):
    data.t1 = text(data.width / 2, 0.5 * data.height / 1, "( -_- ) zzZ", 150)
    data.mode = "init"
    data.c1 = contents("Why do Java developers wear glasses? Because they don't C#", "black")
    bg1 = PIL.Image.open("bg1.jpeg")
    bg1 = bg1.resize((800, 600))
    data.bg1 = ImageTk.PhotoImage(bg1)
    data.time = 0
    data.situation = 3
    data.speed = 20
    data.flag1 = None
    data.flag2 = None
    data.flag3 = None
    data.flag4 = None
    data.flag5 = None
    data.flag6 = None
    bg3 = PIL.Image.open("volcano.jpg")
    bg3 = bg3.resize((800, 600))
    data.bg3 = ImageTk.PhotoImage(bg3)


def mousePressed(event, data):
    # use event.x and event.y
    pass


def keyPressed(event, data):
    # use event.char and event.keysym
    pass


def timerFired(data):
    s=""
    bools=[]
    if big_queue.empty() != True:
        s = big_queue.get()
    if big_queue2.empty() != True:
        bools = big_queue2.get()
    if s!="" and len(bools)>0:
        modeAdjust(s, bools, data)

    if data.mode == "init":
        data.c1.filt(data)
        data.time += 1

    if data.flag1 == True:
        data.mode = "near1"
        data.time = 0

        im1 = PIL.Image.open("main_image.png")
        im1 = im1.resize((500, 600))
        data.im1 = ImageTk.PhotoImage(im1)
        data.flag1 = False
    if data.mode == "near1":
        data.time += 1
        if data.time % 30 == 0:
            data.time = 0
            data.mode = "near1b"
            data.t2 = text(data.width / 2, data.height / 2, "( *w* )", 150)
            data.c2 = contents("One does not simply throw; they recycle", "black")
    if data.mode == "near1b":
        data.c2.filt(data)
        data.time += 1
        if data.time % 5 == 0:
            data.speed *= -1
        data.t2.move(data.speed)
        if data.time % 30 == 0:
            data.time = 0
            data.mode = "near2"
            if data.situation == 1:
                im2 = PIL.Image.open("right_point.png")
                im2 = im2.resize((100, 100))
                data.im2 = ImageTk.PhotoImage(im2)
                im3 = PIL.Image.open("bin.png")
                im3 = im3.resize((100, 100))
                data.im3 = ImageTk.PhotoImage(im3)
            elif data.situation == 2:
                im2 = PIL.Image.open("right_point.png")
                im2 = im2.rotate(180)
                im2 = im2.resize((100, 100))
                im3 = PIL.Image.open("bin.png")
                im3 = im3.resize((100, 100))
                data.im3 = ImageTk.PhotoImage(im3)
                data.im2 = ImageTk.PhotoImage(im2)
            else:
                im2 = PIL.Image.open("right_point.png")
                im2 = im2.rotate(270)
                im2 = im2.resize((100, 100))
                im3 = PIL.Image.open("bin.png")
                im3 = im3.resize((100, 100))
                data.im3 = ImageTk.PhotoImage(im3)
                data.im2 = ImageTk.PhotoImage(im2)
            data.t3 = text(data.width / 2, data.height / 2, "( >U< )", 150)
            data.c3 = contents("Just a few steps! Make waste management great again!", "black")
            data.flag2 = False

    if data.mode == "near2":
        data.c3.filt(data)
        data.time += 1
        if data.time % 5 == 0:
            data.speed *= -1
        data.t3.move(data.speed)
    if data.flag3 == True:
        data.mode = "good1"
        im4 = PIL.Image.open("thumb.png")
        im4 = im4.resize((100, 100))
        data.im4 = ImageTk.PhotoImage(im4)
        im5 = PIL.Image.open("forward.png")
        im5 = im5.resize((100, 100))
        data.im5 = ImageTk.PhotoImage(im5)
        data.time = 0
        data.t4 = text(data.width / 2, data.height / 2, "\( >V< )/", 120)
        data.c4 = contents("Great Job! Go Eagles go!", "black")
        data.flag3 = False
    if data.mode == "good1":
        data.c4.filt(data)
        data.time += 1
        if data.time % 5 == 0:
            data.speed *= -1
        data.t4.move(data.speed)

    if data.flag4 == True:
        data.mode = "good2"
        data.time = 0
        im6 = PIL.Image.open("baby.jpg")
        im6 = im6.resize((180, 130))
        data.im6 = ImageTk.PhotoImage(im6)
        im7 = PIL.Image.open("flag.png")
        im7 = im7.resize((100, 100))
        data.im7 = ImageTk.PhotoImage(im7)
        data.t5 = text(data.width / 2, data.height / 2, "b( ~_^ )d", 120)
        data.c5 = contents("Got you! Thank you for your cooperation and patience!", "black")
        data.flag4 = False
    if data.mode == "good2":
        data.c5.filt(data)
        data.time += 1
        if data.time % 5 == 0:
            data.speed *= -1
        data.t5.move(data.speed)
    if data.flag5 == True:
        data.mode = "not1"
        im8 = PIL.Image.open("nervous.png")
        im8 = im8.resize((100, 100))
        data.im8 = ImageTk.PhotoImage(im8)
        data.time = 0
        data.t6 = text(data.width / 2, data.height / 2, "〴⋋_⋌〵", 120, "green")
        data.c6 = contents("My friend! What are you doing now? You are marching to the wrong bin!", "green")
        data.flag5 = False
    if data.mode == "not1":
        data.c6.filt(data)
        data.time += 1
        if data.time % 5 == 0:
            data.speed *= -1
        data.t6.move(data.speed)

    if data.flag6 == True:
        data.mode = "not2"
        data.time = 0
        im9 = PIL.Image.open("boom.jpeg")
        im9 = im9.resize((100, 100))
        data.im9 = ImageTk.PhotoImage(im9)
        im10 = PIL.Image.open("contamination.jpg")
        im10 = im10.resize((100, 100))
        data.im10 = ImageTk.PhotoImage(im10)
        data.t7 = text(data.width / 2, data.height / 2, "ノಠ_ಠノ", 80, "green")
        data.c7 = contents(
            "Oh! Nightmare! See what you have done! You have destroyed my perfect day, and many other trash bins'!",
            "green")
        data.flag6 = False
    if data.mode == "not2":
        data.c7.filt(data)
        data.time += 1
        if data.time % 5 == 0:
            data.speed *= -1
        data.t7.move(data.speed)


def redrawAll(canvas, data):
    if data.mode in ["init", "near1", "near2", "good1", "good2", "near1b"]:
        canvas.create_image(data.width / 2, data.height / 2, image=data.bg1)

    if data.mode in ["not1", "not2"]:
        canvas.create_image(data.width / 2, data.height / 2, image=data.bg3)
    if data.mode == "init":
        data.t1.draw(canvas, data)
        data.c1.draw(canvas, data)
    if data.mode == "near1":
        canvas.create_image(data.width / 2, data.height / 2, image=data.im1)
    if data.mode == "near1b":
        data.t2.draw(canvas, data)
        data.c2.draw(canvas, data)
    if data.mode == "near2":
        if data.situation == 1:
            canvas.create_image(data.width / 3, data.height / 4, image=data.im2)
            canvas.create_image(data.width * 2 / 3, data.height / 4, image=data.im3)
        elif data.situation == 2:
            canvas.create_image(2 * data.width / 3, data.height / 4, image=data.im2)
            canvas.create_image(data.width / 3, data.height / 4, image=data.im3)
        else:
            canvas.create_image(data.width / 2, data.height / 7, image=data.im2)
            canvas.create_image(data.width / 2, data.height / 3, image=data.im3)
        data.t3.draw(canvas, data)
        data.c3.draw(canvas, data)
    if data.mode == "good1":
        canvas.create_image(data.width / 3, data.height / 4, image=data.im4)
        canvas.create_image(data.width * 2 / 3, data.height / 4, image=data.im5)
        data.t4.draw(canvas, data)
        data.c4.draw(canvas, data)
    if data.mode == "good2":
        canvas.create_image(data.width / 3, data.height / 4, image=data.im6)
        canvas.create_image(data.width * 2 / 3, data.height / 4, image=data.im7)
        data.t5.draw(canvas, data)
        data.c5.draw(canvas, data)
    if data.mode == "not1":
        canvas.create_image(data.width / 2, data.height / 4, image=data.im8)
        data.t6.draw(canvas, data)
        data.c6.draw(canvas, data)
    if data.mode == "not2":
        canvas.create_image(data.width / 3, data.height / 4, image=data.im9)
        canvas.create_image(data.width * 2 / 3, data.height / 4, image=data.im10)
        data.t7.draw(canvas, data)
        data.c7.draw(canvas, data)


####################################
# use the run function as-is
####################################

def newrun(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100  # milliseconds

    # create the root and the canvas
    root = Toplevel()
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


def newfinal():
    print("UI")
    newrun(800, 600)

def main():
    camera_thread=threading.Thread(run2())
    ui_thread=threading.Thread(newfinal())
    ui_thread.start()
    camera_thread.start()
    ui_thread.join()
    camera_thread.join()
main()