#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *
from Resources import *
from os import listdir

class ProjectSettingsDialog(object):
    def __init__(self, parent, project, dict_key = None):
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
        self.top.title("Project settings")
        self.top["bg"] = self.main_color

        self.top.resizable(width = False, height = False)

        top_frame = Frame(self.top, borderwidth = 0, bg = self.main_color)
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
        resolution_label = Label(top_frame, text = "Default shots resolution", bg = self.main_color, fg = self.text_color)
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

        res_x_label = Label(top_frame, text = "x :", bg = self.main_color, fg = self.text_color)
        res_x_label.grid(row = 1, column = 0, sticky = E)

        self.res_x_entry = Entry(top_frame, justify = CENTER, textvariable = self.var_res_x, width = 6, relief = FLAT, bg = self.button_color2)
        self.res_x_entry.grid(row = 1, column = 1, sticky = W)

        res_y_label = Label(top_frame, text = "y :", bg = self.main_color, fg = self.text_color)
        res_y_label.grid(row = 1, column = 2, sticky = E)

        self.res_y_entry = Entry(top_frame, justify = CENTER, textvariable = self.var_res_y, width = 6, relief = FLAT, bg = self.button_color2)
        self.res_y_entry.grid(row = 1, column = 3, sticky = W)

        cancel_button = Button(top_frame, text = "Apply to all shots", bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 14, height = 1)
        cancel_button["command"] = lambda: self.applyResToAll(project)
        cancel_button.grid(row = 1, column = 4, sticky = W)

        ## SAVE/CANCEL ##
        save_button = Button(top_frame, text = "Save", bg = self.button_color1, activebackground = self.over_button_color1, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 8, height = 1)
        save_button["command"] = lambda: self.saveEntry(dict_key)
        save_button.grid(row = 2, column = 0, columnspan = 2, sticky = W)

        cancel_button = Button(top_frame, text = "Cancel", bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 8, height = 1)
        cancel_button["command"] = self.top.destroy
        cancel_button.grid(row = 2, column = 4, sticky = E)

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