#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Main import *
from tkinter import *

import Theme

class OkDialog(object):
	def __init__(self, parent, window_name, message, padding = 10):
		## THEME COLORS ##
		self.theme = Theme.Theme(Resources.readLine("save/options.spi", 2))

		self.root = parent
		self.top = Toplevel(self.root)
		self.top.transient(self.root)
		self.top.title("Superpipe || " + window_name)
		self.top["bg"] = self.theme.main_color

		self.top.resizable(width = False, height = False)

		top_frame = Frame(self.top, borderwidth = 0, bg = self.theme.main_color)
		top_frame.pack(fill = "both", expand = True, padx = padding, pady = padding)

		label = Label(top_frame, text = message, bg = self.theme.main_color, fg = self.theme.text_color)
		label.pack(padx = 4, pady = 4)

		ok_button = Button(top_frame, text = "OK", bg = self.theme.button_color1, activebackground = self.theme.over_button_color1, fg = self.theme.text_color, activeforeground = self.theme.text_color, bd = 0, width = 10, height = 1)
		ok_button["command"] = self.top.destroy
		ok_button.pack(padx = 4, pady = 4)

		self.top.bind("<Return>", lambda event: self.top.destroy())
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
