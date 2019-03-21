#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Main import *
from tkinter import *
from Resources import *
from os import listdir

import Theme

class ProjectSettingsDialog(object):
	def __init__(self, parent, project, dict_key = None):
		## THEME COLORS ##
		self.theme = Theme.Theme(Resources.readLine("save/options.spi", 2))

		self.root = parent
		self.top = Toplevel(self.root)
		self.top.transient(self.root)
		self.top.title("Superpipe || Project settings")
		self.top["bg"] = self.theme.main_color

		self.top.resizable(width = False, height = False)

		top_frame = Frame(self.top, borderwidth = 0, bg = self.theme.main_color)
		top_frame.pack(fill = "both", expand = False, padx = 10, pady = 10)

		top_frame.columnconfigure(0, pad = 5)
		top_frame.columnconfigure(1, pad = 5)
		top_frame.columnconfigure(2, pad = 5)
		top_frame.columnconfigure(3, pad = 5)
		top_frame.columnconfigure(4, pad = 5)
		
		top_frame.rowconfigure(0, pad = 5)
		top_frame.rowconfigure(1, pad = 5)
		top_frame.rowconfigure(2, pad = 5)

		## RESOLUTION ##
		resolution_label = Label(top_frame, text = "Default shots resolution", bg = self.theme.main_color, fg = self.theme.text_color)
		resolution_label.grid(row = 0, column = 0, columnspan = 5)

		res_str = Resources.readLine(project.getDirectory() + "/project_option.spi", 2)

		if res_str:
			res = res_str.split("x")
		else:
			res = (0, 0)

		self.var_res_x = StringVar()
		self.var_res_x.set(res[0])
		self.var_res_y = StringVar()
		self.var_res_y.set(res[1])

		res_x_label = Label(top_frame, text = "x :", bg = self.theme.main_color, fg = self.theme.text_color)
		res_x_label.grid(row = 1, column = 0, sticky = E)

		self.res_x_entry = Entry(top_frame, justify = CENTER, width = 6, relief = FLAT, bg = self.theme.button_color2, validate="key", validatecommand = (self.root.register(self.validateResEntry), '%P', '%S'))
		self.res_x_entry.grid(row = 1, column = 1, sticky = W)

		self.res_x_entry.delete(0)
		self.res_x_entry.insert(0, res[0])

		res_y_label = Label(top_frame, text = "y :", bg = self.theme.main_color, fg = self.theme.text_color)
		res_y_label.grid(row = 1, column = 2, sticky = E)

		self.res_y_entry = Entry(top_frame, justify = CENTER, width = 6, relief = FLAT, bg = self.theme.button_color2, validate="key", validatecommand = (self.root.register(self.validateResEntry), '%P', '%S'))
		self.res_y_entry.grid(row = 1, column = 3, sticky = W)

		self.res_y_entry.delete(0)
		self.res_y_entry.insert(0, res[1])

		cancel_button = Button(top_frame, text = "Apply to all shots", bg = self.theme.button_color2, activebackground = self.theme.over_button_color2, activeforeground = self.theme.text_color, fg = self.theme.text_color, bd = 0, width = 14, height = 1)
		cancel_button["command"] = lambda: self.applyResToAll(project)
		cancel_button.grid(row = 1, column = 4, sticky = W)

		## SAVE/CANCEL ##
		save_button = Button(top_frame, text = "Save", bg = self.theme.button_color1, activebackground = self.theme.over_button_color1, activeforeground = self.theme.text_color, fg = self.theme.text_color, bd = 0, width = 8, height = 1)
		save_button["command"] = lambda: self.saveEntry(dict_key)
		save_button.grid(row = 2, column = 0, columnspan = 2, sticky = W, pady = (10, 0))

		cancel_button = Button(top_frame, text = "Cancel", bg = self.theme.button_color2, activebackground = self.theme.over_button_color2, activeforeground = self.theme.text_color, fg = self.theme.text_color, bd = 0, width = 8, height = 1)
		cancel_button["command"] = self.top.destroy
		cancel_button.grid(row = 2, column = 4, sticky = E, pady = (10, 0))

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

	def validateResEntry(self, P, S):
		valid = S.isnumeric() and len(P) < 5

		if not valid:
			self.root.bell()

		return valid

	def applyResToAll(self, project):
		project.setResolution((self.res_x_entry.get(), self.res_y_entry.get()))
		project.setAllShotsRes()

	def saveEntry(self, dict_key):
		res_x = self.res_x_entry.get()
		res_y = self.res_y_entry.get()
		if res_x and res_y:
			d, key1 = dict_key
			d[key1] = (res_x, res_y)
			self.top.destroy()
