#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *

class CustomSlider(Canvas):
	def __init__(self, parent, width, height, bg, fg, txt, grid, steps):
		self.width = width
		self.height = height
		self.steps_name = steps
		self.steps = len(self.steps_name)
		self.current_step = 1
		self.fg_color = fg
		self.grid_color = grid
		self.txt_color = txt
		self.active = True
		self.percentage = 0

		super().__init__(parent, width = self.width, height = self.height, bg = bg, bd = 0, highlightthickness = 0)

		self.bind("<B1-Motion>", self.update)
		self.bind("<Button-1>", self.update)

		for i in range(self.steps - 1):
			self.create_line(self.width/self.steps * (i + 1) + 1, 5, self.width/self.steps * (i + 1) + 1, self.height - 5, fill = self.grid_color, width = 1)

		i = 0

		for step_name in self.steps_name:
			self.create_text(self.width/self.steps/2 + self.width/self.steps * i, self.height/2, text = step_name, fill = self.txt_color)
			i += 1

	def update(self, event = None):
		if event:
			if self.active:
				x = event.x

				if x > self.width/self.steps * self.current_step - self.width/self.steps and x <= self.width/self.steps * self.current_step:
					self.delete("all")
					self.create_rectangle(0, 0, x, self.height, fill = self.fg_color, width = 0)
					self.percentage = int(x / self.width * 100)
				elif x < self.width/self.steps * self.current_step - self.width/self.steps:
					self.delete("all")
					self.create_rectangle(0, 0, self.width/self.steps * self.current_step - self.width/self.steps + 1, self.height, fill = self.fg_color, width = 0)
					self.percentage = int((self.width/self.steps * self.current_step - self.width/self.steps) / self.width * 100)
				elif x >= self.width/self.steps * self.current_step:
					self.delete("all")
					self.create_rectangle(0, 0, self.width/self.steps * self.current_step + 1, self.height, fill = self.fg_color, width = 0)
					self.percentage = int((self.width/self.steps * self.current_step + 1) / self.width * 100)

				for i in range(self.steps - 1):
					self.create_line(self.width/self.steps * (i + 1) + 1, 5, self.width/self.steps * (i + 1) + 1, self.height - 5, fill = self.grid_color, width = 1)

				i = 0

				for step_name in self.steps_name:
					self.create_text(self.width/self.steps/2 + self.width/self.steps * i, self.height/2, text = step_name, fill = self.txt_color)
					i += 1
		else:
			self.delete("all")
			self.create_rectangle(0, 0, self.width/self.steps * self.current_step - self.width/self.steps + 1, self.height, fill = self.fg_color, width = 0)
			self.percentage = int((self.width/self.steps * self.current_step - self.width/self.steps) / self.width * 100)

			for i in range(self.steps - 1):
				self.create_line(self.width/self.steps * (i + 1) + 1, 5, self.width/self.steps * (i + 1) + 1, self.height - 5, fill = self.grid_color, width = 1)

			i = 0

			for step_name in self.steps_name:
				self.create_text(self.width/self.steps/2 + self.width/self.steps * i, self.height/2, text = step_name, fill = self.txt_color)
				i += 1

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

		self.delete("all")
		self.create_rectangle(0, 0, self.width * self.percentage/100, self.height, fill = self.fg_color, width = 0)

		for i in range(self.steps - 1):
			self.create_line(self.width/self.steps * (i + 1) + 1, 5, self.width/self.steps * (i + 1) + 1, self.height - 5, fill = self.grid_color, width = 1)

		i = 0

		for step_name in self.steps_name:
			self.create_text(self.width/self.steps/2 + self.width/self.steps * i, self.height/2, text = step_name, fill = self.txt_color)
			i += 1

	def getPercentage(self):
		return self.percentage

	def getCurrentStep(self):
		return self.steps_name[self.current_step]
