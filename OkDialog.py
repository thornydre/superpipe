#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *

class OkDialog(object):
    root = None
    def __init__(self, window_name, message):
        self.top = Toplevel(self.root)
        self.top.title(window_name)
        self.top["bg"] = "#666666"

        self.top.resizable(width = False, height = False)

        top_frame = Frame(self.top, borderwidth = 0, bg = "#666666")
        top_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

        label = Label(top_frame, text = message, bg = "#666666")
        label.pack(padx = 4, pady = 4)

        ok_button = Button(top_frame, text = "OK", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 10, height = 1)
        ok_button["command"] = self.top.destroy
        ok_button.pack(padx = 4, pady = 4)

        self.top.bind("<Return>", self.top.destroy)
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