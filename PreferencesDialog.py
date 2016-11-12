#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *
from Resources import *

class PreferencesDialog(object):
    def __init__(self, parent, dict_key = None):
        self.root = parent
        self.top = Toplevel(self.root)
        self.top.transient(self.root)
        self.top.title("Preferences")
        self.top["bg"] = "#666666"

        self.top.resizable(width = False, height = False)

        top_frame = Frame(self.top, borderwidth = 0, bg = "#666666")
        top_frame.pack(fill = "both", expand = False, padx = 10, pady = 10)

        top_frame.columnconfigure(0, pad = 5)
        top_frame.columnconfigure(1, pad = 5)
        top_frame.columnconfigure(2, pad = 5)
        top_frame.columnconfigure(3, pad = 5)
        
        top_frame.rowconfigure(0, pad = 5)
        top_frame.rowconfigure(1, pad = 5)
        top_frame.rowconfigure(2, pad = 5)
        top_frame.rowconfigure(3, pad = 5)
        top_frame.rowconfigure(4, pad = 5)

        ## MAYA ##
        label = Label(top_frame, text = "Path to Maya", bg = "#666666")
        label.grid(row = 0, column = 0, columnspan = 4)

        self.var_maya_text = StringVar()
        self.var_maya_text.set(Resources.readLine("save/options.spi", 1))

        self.maya_path_entry = Entry(top_frame, textvariable = self.var_maya_text, state = DISABLED, width = 75)
        self.maya_path_entry.grid(row = 1, column = 0, columnspan = 3)

        maya_path_button = Button(top_frame, text ="Browse", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1)
        maya_path_button["command"] = lambda: self.mayaPathEntry()
        maya_path_button.grid(row = 1, column = 3, sticky = E)

        ## NUKE ##
        label = Label(top_frame, text = "Path to Nuke", bg = "#666666")
        label.grid(row = 2, column = 0, columnspan = 4)

        self.nuke_var_text = StringVar()
        self.nuke_var_text.set(Resources.readLine("save/options.spi", 1))

        self.nuke_path_entry = Entry(top_frame, textvariable = self.nuke_var_text, state = DISABLED, width = 75)
        self.nuke_path_entry.grid(row = 3, column = 0, columnspan = 3)

        nuke_path_button = Button(top_frame, text ="Browse", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1)
        nuke_path_button["command"] = lambda: self.nukePathEntry()
        nuke_path_button.grid(row = 3, column = 3, sticky = E)

        ## SAVE/CANCEL ##
        save_button = Button(top_frame, text = "Save", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1)
        save_button["command"] = lambda: self.saveEntry(dict_key)
        save_button.grid(row = 4, column = 0, sticky = W)

        cancel_button = Button(top_frame, text = "Cancel", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1)
        cancel_button["command"] = self.top.destroy
        cancel_button.grid(row = 4, column = 3, sticky = E)

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

    def mayaPathEntry(self):
        maya_path = filedialog.askopenfilename(title = "Select Maya.exe",  filetypes = [("Maya","*maya*.exe")])

        if maya_path:
            self.var_maya_text.set(maya_path)

        self.top.focus()

    def nukePathEntry(self):
        nuke_path = filedialog.askopenfilename(title = "Select Nuke.exe",  filetypes = [("Nuke","*nuke*.exe")])

        if nuke_path:
            self.nuke_var_text.set(nuke_path)

        self.top.focus()

    def saveEntry(self, dict_key):
        maya_path = self.maya_path_entry.get()
        nuke_path = self.nuke_path_entry.get()
        if maya_path and nuke_path:
            d, key1, key2 = dict_key
            d[key1] = maya_path
            d[key2] = nuke_path
            self.top.destroy()
