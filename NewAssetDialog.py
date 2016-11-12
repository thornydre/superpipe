#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *
from Resources import *

class NewAssetDialog(object):
    def __init__(self, parent, dict_key = None):
        self.root = parent
        self.top = Toplevel(self.root)
        self.top.transient(self.root)
        self.top.title("Super Pipe || Add asset")
        self.top["bg"] = "#666666"

        self.top.resizable(width = False, height = False)

        top_frame = Frame(self.top, borderwidth = 0, bg = "#666666")
        top_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

        top_frame.columnconfigure(0, pad = 5)
        top_frame.columnconfigure(1, pad = 5)
        
        top_frame.rowconfigure(0, pad = 5)
        top_frame.rowconfigure(1, pad = 5)
        top_frame.rowconfigure(2, pad = 5)
        top_frame.rowconfigure(3, pad = 5)
        top_frame.rowconfigure(4, pad = 5)

        label = Label(top_frame, text = "Select asset category", bg = "#666666")
        label.grid(row = 0, column = 0, columnspan = 2)

        self.rb_selection = IntVar()
        rb1 = Radiobutton(top_frame, text = "CHARACTER", variable = self.rb_selection, value = 1, bg = "#666666", activebackground = "#666666")
        rb1.grid(row = 1, column = 0, sticky = W)

        rb2 = Radiobutton(top_frame, text = "FX", variable = self.rb_selection, value = 2, bg = "#666666", activebackground = "#666666")
        rb2.grid(row = 1, column = 1, sticky = W)

        rb3 = Radiobutton(top_frame, text = "PROPS", variable = self.rb_selection, value = 3, bg = "#666666", activebackground = "#666666")
        rb3.grid(row = 2, column = 0, sticky = W)

        rb4 = Radiobutton(top_frame, text = "SET", variable = self.rb_selection, value = 4, bg = "#666666", activebackground = "#666666")
        rb4.grid(row = 2, column = 1, sticky = W)

        rb1.select()

        name_label = Label(top_frame, text = "Asset name : ", bg = "#666666", fg = "#FFFFFF")
        name_label.grid(row = 3, column = 0, sticky = E)

        self.name_entry = Entry(top_frame)
        self.name_entry.grid(row = 3, column = 1, sticky = W)
        self.name_entry.focus_set()

        submit_button = Button(top_frame, text = "Create asset", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 12, height = 1)
        submit_button["command"] = lambda: self.submit(dict_key)
        submit_button.grid(row = 4, column = 0, sticky = W)

        self.top.bind("<Return>", lambda event, a = dict_key:self.submit(a))

        cancel_button = Button(top_frame, text = "Cancel", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1)
        cancel_button["command"] = self.top.destroy
        cancel_button.grid(row = 4, column = 1, sticky = E)

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
        category = self.rb_selection.get()
        name = self.name_entry.get()
        name = Resources.normString(name)
        if category and name:
            d, key1, key2 = dict_key
            d[key1] = category
            d[key2] = name
            self.top.destroy()
