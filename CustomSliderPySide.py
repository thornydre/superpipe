#!/usr/bin/python

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class CustomSliderPySide(QWidget):
	released = Signal()
	
	def __init__(self, width, height, steps):
		self.steps_name = steps
		self.steps = len(self.steps_name)
		self.current_step = 1
		self.active = True
		self.percentage = 0

		super(CustomSliderPySide, self).__init__()

		self.setMinimumSize(1, 30)
		self.resize(width, height)    


	def mousePressEvent(self, e):
		self.update(e)


	def mouseReleaseEvent(self, e):
		self.released.emit()


	def mouseMoveEvent(self, e):
		self.update(e)


	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)

		font = QFont("Serif", 7, QFont.Light)
		qp.setFont(font)

		size = self.size()
		w = size.width()
		h = size.height()

		qp.setPen(QColor(100, 100, 100))
		qp.setBrush(QColor(100, 100, 100))
		qp.drawRect(0, 0, w, h)

		qp.setPen(QColor(184, 184, 255))
		qp.setBrush(QColor(184, 184, 255))
		qp.drawRect(0, 0, w * self.percentage * 0.01, h)

		pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)

		qp.setPen(pen)

		for i in range(self.steps - 1):
			qp.drawLine(w/self.steps * (i + 1) + 1, 5, w/self.steps * (i + 1) + 1, h - 5)

		i = 0

		for step_name in self.steps_name:
			text_bounds = qp.fontMetrics().boundingRect(step_name)
			fw = text_bounds.width()
			fh = text_bounds.height()
			qp.drawText(w/self.steps * i + w/self.steps/2 - fw/2, h/2 + fh/2, step_name)
			i += 1

		qp.end()


	def update(self, e = None):
		size = self.size()
		w = size.width()
		
		if e:
			if self.active:
				x = e.x()
				if x > w/self.steps * self.current_step - w/self.steps and x <= w/self.steps * self.current_step:
					self.setPercentage(int(x / w * 100))
				elif x < w/self.steps * self.current_step - w/self.steps:
					self.setPercentage(int((w/self.steps * self.current_step - w/self.steps) / w * 100))
				elif x >= w/self.steps * self.current_step:
					self.setPercentage(int((w/self.steps * self.current_step + 1) / w * 100))
		else:
			self.setPercentage(int((w/self.steps * self.current_step - w/self.steps) / w * 100))

		self.repaint()


	def setCurrentStep(self, step):
		i = 1

		for step_name in self.steps_name:
			if step_name == step:
				self.current_step = i
			i += 1

		self.update()


	def nextStep(self):
		self.current_step += 1
		self.update()


	def previousStep(self):
		self.current_step -= 1
		self.update()


	def setActive(self, active):
		self.active = active


	def setPercentage(self, percentage):
		self.percentage = percentage


	def getPercentage(self):
		return self.percentage


	def getCurrentStep(self):
		return self.steps_name[self.current_step]
