#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *
from Resources import *

class PreferencesDialog(object):
    def __init__(self, parent, project_options_path, dict_key = None):
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
        self.top.title("Superpipe || Preferences")
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
        top_frame.rowconfigure(4, pad = 5)
        top_frame.rowconfigure(5, pad = 5)
        top_frame.rowconfigure(6, pad = 5)

        ## MAYA ##
        label = Label(top_frame, text = "Path to Maya", bg = self.main_color, fg = self.text_color)
        label.grid(row = 0, column = 0, columnspan = 4)

        self.var_maya_text = StringVar()
        self.var_maya_text.set(Resources.readLine("save/options.spi", 2))

        self.maya_path_entry = Entry(top_frame, textvariable = self.var_maya_text, state = DISABLED, width = 75, relief = FLAT, disabledbackground = self.disabled_button_color2, disabledforeground = self.disabled_text_color)
        self.maya_path_entry.grid(row = 1, column = 0, columnspan = 3)

        maya_path_button = Button(top_frame, text ="Browse", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        maya_path_button["command"] = lambda: self.mayaPathEntry()
        maya_path_button.grid(row = 1, column = 3, sticky = E)

        ## HOUDINI ##
        label = Label(top_frame, text = "Path to Houdini", bg = self.main_color, fg = self.text_color)
        label.grid(row = 2, column = 0, columnspan = 4)

        self.houdini_var_text = StringVar()
        self.houdini_var_text.set(Resources.readLine("save/options.spi", 3))

        self.houdini_path_entry = Entry(top_frame, textvariable = self.houdini_var_text, state = DISABLED, width = 75, relief = FLAT, disabledbackground = self.disabled_button_color2, disabledforeground = self.disabled_text_color)
        self.houdini_path_entry.grid(row = 3, column = 0, columnspan = 3)

        houdini_path_button = Button(top_frame, text ="Browse", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        houdini_path_button["command"] = lambda: self.houdiniPathEntry()
        houdini_path_button.grid(row = 3, column = 3, sticky = E)

        ## CUSTOM LINK ##
        label = Label(top_frame, text = "Edit custom link", bg = self.main_color, fg = self.text_color)
        label.grid(row = 4, column = 0, columnspan = 4)

        self.var_custom_link = StringVar()
        self.var_custom_link.set(Resources.readLine(project_options_path, 1))

        self.link_entry = Entry(top_frame, textvariable = self.var_custom_link, width = 75, relief = FLAT, bg = self.button_color2)
        self.link_entry.grid(row = 5, column = 0, columnspan = 4, sticky = W + E)

        ## SAVE/CANCEL ##
        save_button = Button(top_frame, text = "Save", bg = self.button_color1, activebackground = self.over_button_color1, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        save_button["command"] = lambda: self.saveEntry(dict_key)
        save_button.grid(row = 6, column = 0, sticky = W)

        cancel_button = Button(top_frame, text = "Cancel", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        cancel_button["command"] = self.top.destroy
        cancel_button.grid(row = 6, column = 3, sticky = E)

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

    def houdiniPathEntry(self):
        houdini_path = filedialog.askopenfilename(title = "Select Houdini.exe",  filetypes = [("Houdini","*Houdini*.exe")])

        if houdini_path:
            self.houdini_var_text.set(houdini_path)

        self.top.focus()

    def saveEntry(self, dict_key):
        maya_path = self.maya_path_entry.get()
        houdini_path = self.houdini_path_entry.get()
        custom_link = self.link_entry.get()
        if custom_link and maya_path and houdini_path:
            d, key1, key2, key3 = dict_key
            d[key1] = custom_link
            d[key2] = maya_path
            d[key3] = houdini_path
            self.top.destroy()
