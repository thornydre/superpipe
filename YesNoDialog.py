#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *

class YesNoDialog(object):
    def __init__(self, parent, window_name, question, dict_key):
        ## THEME COLORS ##
        self.theme = Resources.readLine("save/options.spi", 2)
        self.main_color = Resources.readLine("save/themes/" + self.theme + ".spi", 1)
        self.button_color1 = Resources.readLine("save/themes/" + self.theme + ".spi", 4)
        self.over_button_color1 = Resources.readLine("save/themes/" + self.theme + ".spi", 5)
        self.button_color2 = Resources.readLine("save/themes/" + self.theme + ".spi", 6)
        self.over_button_color2 = Resources.readLine("save/themes/" + self.theme + ".spi", 7)
        self.text_color = Resources.readLine("save/themes/" + self.theme + ".spi", 9)

        self.root = parent
        self.top = Toplevel(self.root)
        self.top.transient(self.root)
        self.top.title("Superpipe || " + window_name)
        self.top["bg"] = self.main_color

        self.top.resizable(width = False, height = False)

        top_frame = Frame(self.top, borderwidth = 0, bg = self.main_color)
        top_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

        label = Label(top_frame, text = question, bg = self.main_color, fg = self.text_color)
        label.pack(padx = 4, pady = 4)

        yes_button = Button(top_frame, text = "Yes", bg = self.button_color1, activebackground = self.over_button_color1, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 10, height = 1)
        yes_button["command"] = lambda: self.yes(dict_key)
        yes_button.pack(side = LEFT, padx = 4, pady = 4)

        self.top.bind("<Return>", lambda event, a = dict_key:self.yes(a))

        no_button = Button(top_frame, text = "No", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 10, height = 1)
        no_button["command"] = self.top.destroy
        no_button.pack(side = RIGHT, padx = 4, pady = 4)

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

    def yes(self, dict_key):
        d, key = dict_key
        d[key] = "yes"
        self.top.destroy()
