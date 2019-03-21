#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Main import *
from tkinter import *

import Theme

class NewShotDialog(object):
	def __init__(self, parent, project, dict_key = None):
		## THEME COLORS ##
		self.theme = Theme.Theme(Resources.readLine("save/options.spi", 2))

		self.root = parent
		self.top = Toplevel(self.root)
		self.top.transient(self.root)
		self.top.title("Super Pipe || Add shot")
		self.top["bg"] = self.theme.main_color

		self.top.resizable(width = False, height = False)

		self.project = project

		top_frame = Frame(self.top, borderwidth = 0, bg = self.theme.main_color)
		top_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

		label = Label(top_frame, text = "Select sequence", bg = self.theme.main_color, fg = self.theme.text_color)
		label.pack(padx = 4, pady = 4)

		self.sequence_list = Listbox(top_frame, bg = self.theme.list_color, selectbackground = self.theme.second_color, bd = 0, highlightthickness = 0, width = 30, exportselection = False)
		self.sequence_list.pack(fill = BOTH, pady = (5, 15))

		for sequence in range(self.project.getSequenceNumber()):
			self.sequence_list.insert(END, "Sequence " + str(sequence + 1))

		self.sequence_list.select_set(END)

		submit_button = Button(top_frame, text = "Create shot", bg = self.theme.button_color1, activebackground = self.theme.over_button_color1, fg = self.theme.text_color, activeforeground = self.theme.text_color, bd = 0, width = 12, height = 1)
		submit_button["command"] = lambda: self.createShotEntry(dict_key)
		submit_button.pack(side = LEFT, padx = 4, pady = 4)

		self.top.bind("<Return>", lambda event, a = dict_key:self.createShotEntry(a))

		add_sequence_button = Button(top_frame, text = "Add sequence", bg = self.theme.button_color2, activebackground = self.theme.over_button_color2, fg = self.theme.text_color, activeforeground = self.theme.text_color, bd = 0, width = 12, height = 1)
		add_sequence_button["command"] = lambda: self.addSequenceEntry(self.project)
		add_sequence_button.pack(side = LEFT, padx = 4, pady = 4)

		cancel_button = Button(top_frame, text = "Cancel", bg = self.theme.button_color2, activebackground = self.theme.over_button_color2, fg = self.theme.text_color, activeforeground = self.theme.text_color, bd = 0, width = 8, height = 1)
		cancel_button["command"] = self.top.destroy
		cancel_button.pack(padx = 4, pady = 4)

		self.top.bind("<Escape>", lambda event: self.top.destroy())

		self.top.update_idletasks()
		w = self.top.winfo_screenwidth()
		h = self.top.winfo_screenheight()
		size = tuple(int(_) for _ in self.top.geometry().split("+")[0].split("x"))
		x = w/2 - size[0]/2
		y = h/2 - size[1]/2
		self.top.geometry("%dx%d+%d+%d" % (size + (x, y)))

		self.top.iconbitmap("img/icon.ico")
		self.top.focus()

	def addSequenceEntry(self, project):
		project.addSequence()

		self.sequence_list.delete(0, END)

		for sequence in range(project.getSequenceNumber()):
			self.sequence_list.insert(END, "Sequence " + str(sequence + 1))

		self.sequence_list.select_set(END)

	def createShotEntry(self, dict_key):
		sequence = self.sequence_list.curselection()
		if sequence:
			data = sequence[0] + 1
			d, key = dict_key
			d[key] = data
			self.top.destroy()
