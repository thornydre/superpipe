#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from Resources import *
from PIL import ImageTk

import cv2
import PIL

class CustomVideoPlayer(Canvas):
    def __init__(self, parent, video, width, bg):
        self.video_width = width
        self.video_height = self.video_width / 1.85
        self.playblast_shot_gifdict = {}

        # self.video_capture = cv2.VideoCapture(video)
        # self.video_capture.set(0, int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)) * int(self.video_capture.get(cv2.CAP_PROP_FPS )))
        # success,captured_image = self.video_capture.read()
        # cv2_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGBA)

        # extracted_image = PIL.Image.fromarray(cv2_image)
        # resized_image = Resources.resizeImage(extracted_image, self.video_width)
        # tk_image = ImageTk.PhotoImage(image = resized_image)

        # self.video_height = tk_image.height()

        super().__init__(parent, width = self.video_width, height = self.video_height, bg = bg, bd = 0, highlightthickness = 0)

        # self.playblast_shot_gifdict["temp_img"] = tk_image

        self.create_text(self.video_width/2, self.video_height/2, font = ("Helvetica", 50), text = "ERROR", fill = "#D34E4E")

        self.bind("<Motion>", self.update)

    def update(self, event):
        self.delete("all")

        x = event.x

        try:
            second = x / self.video_width * int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)) / int(self.video_capture.get(cv2.CAP_PROP_FPS)) * 1000

            self.video_capture.set(0, second)
            success,test_img = self.video_capture.read()

            cv2_image = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGBA)

            test_img = PIL.Image.fromarray(cv2_image)
            test_img = Resources.resizeImage(test_img, self.video_width)
            tk_image = ImageTk.PhotoImage(image = test_img)

            self.playblast_shot_gifdict["temp_img"] = tk_image

            self.create_image(0, 0, anchor = N + W, image = tk_image)

        except:
            self.create_text(self.video_width/2, self.video_height/2, font = ("Helvetica", 50), text = "ERROR", fill = "#D34E4E")

    def updateVideo(self, video):
        self.delete("all")

        try:
            self.video_capture = cv2.VideoCapture(video)

            second = 0.5 * int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)) / int(self.video_capture.get(cv2.CAP_PROP_FPS)) * 1000

            self.video_capture.set(0, second)
            success,test_img = self.video_capture.read()

            cv2_image = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGBA)

            test_img = PIL.Image.fromarray(cv2_image)
            test_img = Resources.resizeImage(test_img, self.video_width)
            tk_image = ImageTk.PhotoImage(image = test_img)

            self.playblast_shot_gifdict["temp_img"] = tk_image

            self.create_image(0, 0, anchor = N + W, image = tk_image)
            self.config(width = tk_image.width(), height = tk_image.height())

        except:
            self.create_text(self.video_width/2, self.video_height/2, font = ("Helvetica", 50), text = "ERROR", fill = "#D34E4E")
