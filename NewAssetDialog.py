#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *
from Resources import *
from os import walk

import Theme

class NewAssetDialog(object):
	def __init__(self, parent, project, dict_key = None):
		## THEME COLORS ##
		self.theme = Theme.Theme(Resources.readLine("save/options.spi", 2))

		self.root = parent
		self.top = Toplevel(self.root)
		self.top.transient(self.root)
		self.top.title("Super Pipe || Add asset")
		self.top["bg"] = self.theme.main_color

		self.top.resizable(width = False, height = False)

		top_frame = Frame(self.top, borderwidth = 0, bg = self.theme.main_color)
		top_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

		top_frame.columnconfigure(0, pad = 5)
		top_frame.columnconfigure(1, pad = 5)
		
		top_frame.rowconfigure(0, pad = 5)
		top_frame.rowconfigure(1, pad = 5)
		top_frame.rowconfigure(2, pad = 5)
		top_frame.rowconfigure(3, pad = 5)
		top_frame.rowconfigure(4, pad = 5)
		top_frame.rowconfigure(5, pad = 5)
		top_frame.rowconfigure(6, pad = 5)

		label = Label(top_frame, text = "Select asset software", bg = self.theme.main_color, fg = self.theme.text_color)
		label.grid(row = 0, column = 0, columnspan = 3)

		self.rb_software = IntVar()
		self.softwares_list = ("maya", "houdini", "blender")
		i = 0

		for software in self.softwares_list:
			rb_software = Radiobutton(top_frame, text = software.upper(), variable = self.rb_software, value = i, bg = self.theme.main_color, activebackground = self.theme.main_color, fg = self.theme.text_color, activeforeground = self.theme.text_color, selectcolor = self.theme.second_color)
			rb_software.grid(row = int(i/2) + 1, column = i % 2, sticky = W)

			if software == project.default_software:
				rb_software.select()

			i += 1

		# rb_software1 = Radiobutton(top_frame, text = "MAYA", variable = self.rb_software, value = 1, bg = self.theme.main_color, activebackground = self.theme.main_color, fg = self.theme.text_color, activeforeground = self.theme.text_color, selectcolor = self.theme.second_color)
		# rb_software1.grid(row = 1, column = 0, sticky = W)

		# rb_software2 = Radiobutton(top_frame, text = "HOUDINI", variable = self.rb_software, value = 2, bg = self.theme.main_color, activebackground = self.theme.main_color, fg = self.theme.text_color, activeforeground = self.theme.text_color, selectcolor = self.theme.second_color)
		# rb_software2.grid(row = 1, column = 1, sticky = W)

		# rb_software3 = Radiobutton(top_frame, text = "BLENDER", variable = self.rb_software, value = 3, bg = self.theme.main_color, activebackground = self.theme.main_color, fg = self.theme.text_color, activeforeground = self.theme.text_color, selectcolor = self.theme.second_color)
		# rb_software3.grid(row = 2, column = 0, sticky = W)

		# rb_software1.select()

		label = Label(top_frame, text = "Select asset category", bg = self.theme.main_color, fg = self.theme.text_color)
		label.grid(row = 3, column = 0, columnspan = 3)

		self.categories_list = ttk.Treeview(top_frame, height = 5, show = "tree", selectmode = "browse")
		ttk.Style().configure("Treeview", background = self.theme.list_color)
		self.categories_list.insert("", 1, "character", text = "CHARACTER")
		self.categories_list.insert("", 2, "fx", text = "FX")
		self.categories_list.insert("", 3, "props", text = "PROPS")
		self.categories_list.insert("", 4, "set", text = "SET")
		self.categories_list.grid(row = 4, column = 0, columnspan = 2)

		assets = project.getAssetList()

		for asset in assets:
			if asset[0] != "backup":
				if path.isdir(project.getDirectory() + "/04_asset" + asset[1] + "/" + asset[0] + "/superpipe"):
					cur_asset = Asset(project.getDirectory(), asset[1], asset[0])

					asset_subfolders = asset[1].split("/")

					for i in range(len(asset_subfolders)):
						if not self.categories_list.exists(asset_subfolders[i].lower()):
							if i > 1:
								self.categories_list.insert(asset_subfolders[i - 1].lower(), END, asset_subfolders[i].lower(), text = asset_subfolders[i].upper(), tags = ("folder"))
				else:
					dialog = lambda: OkDialog.OkDialog(self.parent, "ERROR", "The asset \"" + asset[0] + "\" has a problem !", padding = 20)
					self.wait_window(dialog().top)

		name_label = Label(top_frame, text = "Asset name : ", bg = self.theme.main_color, fg = self.theme.text_color)
		name_label.grid(row = 5, column = 0, sticky = E)

		self.name_entry = Entry(top_frame, relief = FLAT, bg = self.theme.button_color2)
		self.name_entry.grid(row = 5, column = 1, sticky = W)
		self.name_entry.focus_set()

		submit_button = Button(top_frame, text = "Create asset", bg = self.theme.button_color1, activebackground = self.theme.over_button_color1, fg = self.theme.text_color, activeforeground = self.theme.text_color, bd = 0, width = 12, height = 1)
		submit_button["command"] = lambda: self.submit(dict_key)
		submit_button.grid(row = 6, column = 0, sticky = W, pady = (10, 0))

		self.top.bind("<Return>", lambda event, a = dict_key:self.submit(a))

		cancel_button = Button(top_frame, text = "Cancel", bg = self.theme.button_color2, activebackground = self.theme.over_button_color2, fg = self.theme.text_color, activeforeground = self.theme.text_color, bd = 0, width = 8, height = 1)
		cancel_button["command"] = self.top.destroy
		cancel_button.grid(row = 6, column = 1, sticky = E, pady = (10, 0))

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

	def submit(self, dict_key):
		print(self.softwares_list[self.rb_software.get()])
		parent = self.categories_list.focus()
		category_list = []

		if parent:
			category_list.insert(0, parent)
		
			while parent:
				parent = self.categories_list.parent(parent)
				if parent:
					category_list.insert(0, parent)

		category = "/" + "/".join(category_list)

		name = self.name_entry.get()
		name = Resources.normString(name)
		software = self.softwares_list[self.rb_software.get()]
		if category and name:
			d, key1, key2, key3 = dict_key
			d[key1] = category
			d[key2] = name
			d[key3] = software
			self.top.destroy()
