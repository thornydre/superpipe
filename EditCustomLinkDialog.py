#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *
from Resources import *

class EditCustomLinkDialog(object):
    def __init__(self, parent, project_options_path, dict_key = None):
        ## THEME COLORS ##
        self.main_color = Resources.readLine("save/themes.spi", 1)
        self.button_color1 = Resources.readLine("save/themes.spi", 4)
        self.over_button_color1 = Resources.readLine("save/themes.spi", 5)
        self.button_color2 = Resources.readLine("save/themes.spi", 6)
        self.over_button_color2 = Resources.readLine("save/themes.spi", 7)
        self.text_color = Resources.readLine("save/themes.spi", 9)

        self.root = parent
        self.top = Toplevel(self.root)
        self.top.transient(self.root)
        self.top.title("Super Pipe || Rename asset")
        self.top["bg"] = self.main_color

        self.top.resizable(width = False, height = False)

        top_frame = Frame(self.top, borderwidth = 0, bg = self.main_color)
        top_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

        top_frame.columnconfigure(0, pad = 5)
        top_frame.columnconfigure(1, pad = 5)
        
        top_frame.rowconfigure(0, pad = 5)
        top_frame.rowconfigure(1, pad = 5)

        name_label = Label(top_frame, text = "Custom link : ", bg = self.main_color, fg = self.text_color)
        name_label.grid(row = 0, column = 0, sticky = E)

        self.var_custom_link = StringVar()
        self.var_custom_link.set(Resources.readLine(project_options_path, 1))

        self.link_entry = Entry(top_frame, textvariable = self.var_custom_link, width = 75, relief = FLAT, bg = self.button_color2)
        self.link_entry.grid(row = 0, column = 1, sticky = W)
        self.link_entry.focus_set()

        submit_button = Button(top_frame, text = "Submit", bg = self.button_color1, activebackground = self.over_button_color1, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 12, height = 1)
        submit_button["command"] = lambda: self.submit(dict_key)
        submit_button.grid(row = 1, column = 0, sticky = W)

        self.top.bind("<Return>", lambda event, a = dict_key:self.submit(a))

        cancel_button = Button(top_frame, text = "Cancel", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
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
