#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *

class NewShotDialog(object):
    def __init__(self, parent, dict_key = None):
        self.root = parent
        self.top = Toplevel(self.root)
        self.top.transient(self.root)
        self.top.title("Super Pipe || Add shot")
        self.top["bg"] = "#666666"

        self.top.resizable(width = False, height = False)

        top_frame = Frame(self.top, borderwidth = 0, bg = "#666666")
        top_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

        label = Label(top_frame, text = "Select sequence", bg = "#666666")
        label.pack(padx = 4, pady = 4)

        keep_sequence_button = Button(top_frame, text = "Keep sequence", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 12, height = 1)
        keep_sequence_button["command"] = lambda: self.keepSequenceEntry(dict_key)
        keep_sequence_button.pack(side = LEFT, padx = 4, pady = 4)

        self.top.bind("<Return>", lambda event, a = dict_key:self.keepSequenceEntry(a))

        add_sequence_button = Button(top_frame, text = "Add sequence", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 12, height = 1)
        add_sequence_button["command"] = lambda: self.addSequenceEntry(dict_key)
        add_sequence_button.pack(side = LEFT, padx = 4, pady = 4)

        cancel_button = Button(top_frame, text = "Cancel", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1)
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

    def keepSequenceEntry(self, dict_key):
        sequence = 0
        data = sequence
        d, key = dict_key
        d[key] = data
        self.top.destroy()

    def addSequenceEntry(self, dict_key):
        sequence = 1
        d, key = dict_key
        d[key] = sequence
        self.top.destroy()
