#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *
from Resources import *

class NewAssetDialog(object):
    def __init__(self, parent, dict_key = None):
        ## THEME COLORS ##
        self.main_color = Resources.readLine("save/themes.spi", 1)
        self.second_color = Resources.readLine("save/themes.spi", 2)
        self.button_color1 = Resources.readLine("save/themes.spi", 4)
        self.over_button_color1 = Resources.readLine("save/themes.spi", 5)
        self.button_color2 = Resources.readLine("save/themes.spi", 6)
        self.over_button_color2 = Resources.readLine("save/themes.spi", 7)
        self.text_color = Resources.readLine("save/themes.spi", 9)

        self.root = parent
        self.top = Toplevel(self.root)
        self.top.transient(self.root)
        self.top.title("Super Pipe || Add asset")
        self.top["bg"] = self.main_color

        self.top.resizable(width = False, height = False)

        top_frame = Frame(self.top, borderwidth = 0, bg = self.main_color)
        top_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

        top_frame.columnconfigure(0, pad = 5)
        top_frame.columnconfigure(1, pad = 5)
        
        top_frame.rowconfigure(0, pad = 5)
        top_frame.rowconfigure(1, pad = 5)
        top_frame.rowconfigure(2, pad = 5)
        top_frame.rowconfigure(3, pad = 5)
        top_frame.rowconfigure(4, pad = 5)

        label = Label(top_frame, text = "Select asset software", bg = self.main_color, fg = self.text_color)
        label.grid(row = 0, column = 0, columnspan = 2)

        self.rb_software = IntVar()
        rb_software1 = Radiobutton(top_frame, text = "MAYA", variable = self.rb_software, value = 1, bg = self.main_color, activebackground = self.main_color, fg = self.text_color, activeforeground = self.text_color, selectcolor = self.second_color)
        rb_software1.grid(row = 1, column = 0, sticky = W)

        rb_software2 = Radiobutton(top_frame, text = "HOUDINI", variable = self.rb_software, value = 2, bg = self.main_color, activebackground = self.main_color, fg = self.text_color, activeforeground = self.text_color, selectcolor = self.second_color)
        rb_software2.grid(row = 1, column = 1, sticky = W)

        rb_software1.select()

        label = Label(top_frame, text = "Select asset category", bg = self.main_color, fg = self.text_color)
        label.grid(row = 2, column = 0, columnspan = 2)

        self.rb_category = IntVar()
        rb_category1 = Radiobutton(top_frame, text = "CHARACTER", variable = self.rb_category, value = 1, bg = self.main_color, activebackground = self.main_color, fg = self.text_color, activeforeground = self.text_color, selectcolor = self.second_color)
        rb_category1.grid(row = 3, column = 0, sticky = W)

        rb_category2 = Radiobutton(top_frame, text = "FX", variable = self.rb_category, value = 2, bg = self.main_color, activebackground = self.main_color, fg = self.text_color, activeforeground = self.text_color, selectcolor = self.second_color)
        rb_category2.grid(row = 3, column = 1, sticky = W)

        rb_category3 = Radiobutton(top_frame, text = "PROPS", variable = self.rb_category, value = 3, bg = self.main_color, activebackground = self.main_color, fg = self.text_color, activeforeground = self.text_color, selectcolor = self.second_color)
        rb_category3.grid(row = 4, column = 0, sticky = W)

        rb_category4 = Radiobutton(top_frame, text = "SET", variable = self.rb_category, value = 4, bg = self.main_color, activebackground = self.main_color, fg = self.text_color, activeforeground = self.text_color, selectcolor = self.second_color)
        rb_category4.grid(row = 4, column = 1, sticky = W)

        rb_category1.select()

        name_label = Label(top_frame, text = "Asset name : ", bg = self.main_color, fg = self.text_color)
        name_label.grid(row = 5, column = 0, sticky = E)

        self.name_entry = Entry(top_frame, relief = FLAT, bg = self.button_color2)
        self.name_entry.grid(row = 5, column = 1, sticky = W)
        self.name_entry.focus_set()

        submit_button = Button(top_frame, text = "Create asset", bg = self.button_color1, activebackground = self.over_button_color1, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 12, height = 1)
        submit_button["command"] = lambda: self.submit(dict_key)
        submit_button.grid(row = 6, column = 0, sticky = W)

        self.top.bind("<Return>", lambda event, a = dict_key:self.submit(a))

        cancel_button = Button(top_frame, text = "Cancel", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        cancel_button["command"] = self.top.destroy
        cancel_button.grid(row = 6, column = 1, sticky = E)

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
        category = self.rb_category.get()
        name = self.name_entry.get()
        name = Resources.normString(name)
        software = self.rb_software.get()
        if category and name:
            d, key1, key2, key3 = dict_key
            d[key1] = category
            d[key2] = name
            d[key3] = software
            self.top.destroy()
