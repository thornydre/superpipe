#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *
from Resources import *

class EditCustomLinkDialog(object):
    root = None
    def __init__(self, project_options_path, dict_key = None):
        self.top = Toplevel(self.root)
        self.top.title("Super Pipe || Rename asset")
        self.top["bg"] = "#666666"

        self.top.resizable(width = False, height = False)

        top_frame = Frame(self.top, borderwidth = 0, bg = "#666666")
        top_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

        top_frame.columnconfigure(0, pad = 5)
        top_frame.columnconfigure(1, pad = 5)
        
        top_frame.rowconfigure(0, pad = 5)
        top_frame.rowconfigure(1, pad = 5)

        name_label = Label(top_frame, text = "Custom link : ", bg = "#666666", fg = "#FFFFFF")
        name_label.grid(row = 0, column = 0, sticky = E)

        self.var_custom_link = StringVar()
        self.var_custom_link.set(Resources.readLine(project_options_path, 1))

        self.link_entry = Entry(top_frame, textvariable = self.var_custom_link, width = 75)
        self.link_entry.grid(row = 0, column = 1, sticky = W)
        self.link_entry.focus_set()

        submit_button = Button(top_frame, text = "Submit", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 12, height = 1)
        submit_button["command"] = lambda: self.submit(dict_key)
        submit_button.grid(row = 1, column = 0, sticky = W)

        self.top.bind("<Return>", lambda event, a = dict_key:self.submit(a))

        cancel_button = Button(top_frame, text = "Cancel", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1)
        cancel_button["command"] = self.top.destroy
        cancel_button.grid(row = 1, column = 1, sticky = E)

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
        link = self.link_entry.get()
        if link:
            d, key = dict_key
            d[key] = link
            self.top.destroy()
