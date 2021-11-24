#!/usr/bin/python

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import cv2
import PIL

class CustomVideoPlayer(QLabel):
	def __init__(self, width, height):
		self.video_width = width
		self.video_height = height
		self.playblast_shot_gifdict = {}

		super(CustomVideoPlayer, self).__init__()

		self.setMinimumSize(width, height)
		self.resize(width, height)


	def update(self, x):
		frame = x / self.video_width * self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)

		self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame)
		success, captured_img = self.video_capture.read()

		if success:
			final_img = cv2.cvtColor(captured_img, cv2.COLOR_BGR2RGBA)
			final_img = cv2.resize(final_img, (self.video_width, self.video_height), interpolation= cv2.INTER_LINEAR)

			if len(final_img.shape) == 3:
				if(final_img.shape[2]) == 4:
					qformat = QImage.Format_RGBA8888
				else:
					qformat = QImage.Format_RGB888

				img = QImage(final_img.data, final_img.shape[1], final_img.shape[0], qformat)

				# img = img.rgbSwapped()
				self.setPixmap(QPixmap.fromImage(img))


	def updateVideo(self, video):
		self.video_capture = cv2.VideoCapture(video)

		self.update(0.5)


	def mouseMoveEvent(self, e):
		self.update(e.position().x())
