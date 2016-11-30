#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *

class NewProjectDialog(object):
    def __init__(self, parent, dict_key = None):
        ## THEME COLORS ##
        self.main_color = Resources.readLine("save/themes.spi", 1)
        self.button_color1 = Resources.readLine("save/themes.spi", 4)
        self.over_button_color1 = Resources.readLine("save/themes.spi", 5)
        self.button_color2 = Resources.readLine("save/themes.spi", 6)
        self.over_button_color2 = Resources.readLine("save/themes.spi", 7)
        self.disabled_button_color2 = Resources.readLine("save/themes.spi", 10)
        self.text_color = Resources.readLine("save/themes.spi", 9)
        self.disabled_text_color = Resources.readLine("save/themes.spi", 11)

        self.root = parent
        self.top = Toplevel(self.root)
        self.top.transient(self.root)
        self.top.title("New project")
        self.top["bg"] = self.main_color

        self.top.resizable(width = False, height = False)

        top_frame = Frame(self.top, borderwidth = 0, bg = self.main_color)
        top_frame.pack(fill = "both", expand = False, padx = 10, pady = 10)

        top_frame.columnconfigure(0, pad = 5)
        top_frame.columnconfigure(1, pad = 5)
        top_frame.columnconfigure(2, pad = 5)
        top_frame.columnconfigure(3, pad = 5)
        
        top_frame.rowconfigure(0, pad = 5)
        top_frame.rowconfigure(1, pad = 5)
        top_frame.rowconfigure(2, pad = 5)
        top_frame.rowconfigure(3, pad = 5)

        label = Label(top_frame, text = "New project", bg = self.main_color, fg = self.text_color)
        label.grid(row = 0, column = 0, columnspan = 4)

        self.var_text = StringVar()

        self.directory_entry = Entry(top_frame, textvariable = self.var_text, state = DISABLED, width = 75, relief = FLAT, disabledbackground = self.disabled_button_color2, disabledforeground = self.disabled_text_color)
        self.directory_entry.grid(row = 1, column = 0, columnspan = 3)

        directory_button = Button(top_frame, text ="Browse", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        directory_button["command"] = lambda: self.directoryEntry()
        directory_button.grid(row = 1, column = 3, sticky = E)

        name_label = Label(top_frame, text = "Project name : ", bg = self.main_color, fg = self.text_color)
        name_label.grid(row = 2, column = 0, sticky = E)

        self.name_entry = Entry(top_frame, relief = FLAT, bg = self.button_color2)
        self.name_entry.grid(row = 2, column = 1, sticky = W)

        submit_button = Button(top_frame, text = "Create project", bg = self.button_color1, activebackground = self.over_button_color1, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 12, height = 1)
        submit_button["command"] = lambda: self.submit(dict_key)
        submit_button.grid(row = 3, column = 0, sticky = W)

        self.top.bind("<Return>", lambda event, a = dict_key:self.submit(a))

        cancel_button = Button(top_frame, text = "Cancel", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        cancel_button["command"] = self.top.destroy
        cancel_button.grid(row = 3, column = 3, sticky = E)

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

    def directoryEntry(self):
        directory = filedialog.askdirectory(title = "New project", mustexist  = False)

        self.var_text.set(directory)

        self.top.lift()

    def submit(self, dict_key):
        directory = self.directory_entry.get()
        name = self.name_entry.get()
        if directory and name:
            d, key = dict_key
            d[key] = directory + "/" + name
            self.top.destroy()
