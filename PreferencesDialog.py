#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *
from Resources import *
from tkinter import ttk
from os import listdir, path

class PreferencesDialog(object):
    def __init__(self, parent, project_options_path, dict_key = None):
        ## THEME COLORS ##
        self.theme = Resources.readLine("save/options.spi", 2)
        self.main_color = Resources.readLine("save/themes/" + self.theme + ".spi", 1)
        self.second_color = Resources.readLine("save/themes/" + self.theme + ".spi", 2)
        self.button_color1 = Resources.readLine("save/themes/" + self.theme + ".spi", 4)
        self.over_button_color1 = Resources.readLine("save/themes/" + self.theme + ".spi", 5)
        self.button_color2 = Resources.readLine("save/themes/" + self.theme + ".spi", 6)
        self.over_button_color2 = Resources.readLine("save/themes/" + self.theme + ".spi", 7)
        self.disabled_button_color2 = Resources.readLine("save/themes/" + self.theme + ".spi", 10)
        self.text_color = Resources.readLine("save/themes/" + self.theme + ".spi", 9)
        self.disabled_text_color = Resources.readLine("save/themes/" + self.theme + ".spi", 11)

        self.root = parent
        self.top = Toplevel(self.root)
        self.top.transient(self.root)
        self.top.title("Superpipe || Preferences")
        self.top["bg"] = self.main_color

        self.top.resizable(width = False, height = False)

        tabs_frame = ttk.Notebook(self.top, padding = 0)

        ## // SOFTWARES \\ ##
        softwares_frame = Frame(tabs_frame, borderwidth = 0, bg = self.main_color)
        softwares_frame.pack()

        softwares_frame.columnconfigure(0, pad = 5)
        softwares_frame.columnconfigure(1, pad = 5)
        softwares_frame.columnconfigure(2, pad = 5)
        softwares_frame.columnconfigure(3, pad = 5)
        
        softwares_frame.rowconfigure(0, pad = 5)
        softwares_frame.rowconfigure(1, pad = 5)
        softwares_frame.rowconfigure(2, pad = 5)
        softwares_frame.rowconfigure(3, pad = 5)
        softwares_frame.rowconfigure(4, pad = 5)
        softwares_frame.rowconfigure(5, pad = 5)
        softwares_frame.rowconfigure(6, pad = 5)
        softwares_frame.rowconfigure(7, pad = 5)
        softwares_frame.rowconfigure(8, pad = 5)

        ## MAYA ##
        label = Label(softwares_frame, text = "Path to Maya", bg = self.main_color, fg = self.text_color)
        label.grid(row = 0, column = 0, columnspan = 2)

        self.var_maya_text = StringVar()
        self.var_maya_text.set(Resources.readLine("save/options.spi", 3))

        self.maya_path_entry = Entry(softwares_frame, textvariable = self.var_maya_text, state = DISABLED, width = 75, relief = FLAT, disabledbackground = self.disabled_button_color2, disabledforeground = self.disabled_text_color)
        self.maya_path_entry.grid(row = 1, column = 0)

        maya_path_button = Button(softwares_frame, text ="Browse", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        maya_path_button["command"] = lambda: self.mayaPathEntry()
        maya_path_button.grid(row = 1, column = 1, sticky = E)

        ## HOUDINI ##
        label = Label(softwares_frame, text = "Path to Houdini", bg = self.main_color, fg = self.text_color)
        label.grid(row = 2, column = 0, columnspan = 2)

        self.houdini_var_text = StringVar()
        self.houdini_var_text.set(Resources.readLine("save/options.spi", 4))

        self.houdini_path_entry = Entry(softwares_frame, textvariable = self.houdini_var_text, state = DISABLED, width = 75, relief = FLAT, disabledbackground = self.disabled_button_color2, disabledforeground = self.disabled_text_color)
        self.houdini_path_entry.grid(row = 3, column = 0)

        houdini_path_button = Button(softwares_frame, text ="Browse", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        houdini_path_button["command"] = lambda: self.houdiniPathEntry()
        houdini_path_button.grid(row = 3, column = 1, sticky = E)

        ## BLENDER ##
        label = Label(softwares_frame, text = "Path to Blender", bg = self.main_color, fg = self.text_color)
        label.grid(row = 4, column = 0, columnspan = 2)

        self.blender_var_text = StringVar()
        self.blender_var_text.set(Resources.readLine("save/options.spi", 5))

        self.blender_path_entry = Entry(softwares_frame, textvariable = self.blender_var_text, state = DISABLED, width = 75, relief = FLAT, disabledbackground = self.disabled_button_color2, disabledforeground = self.disabled_text_color)
        self.blender_path_entry.grid(row = 5, column = 0)

        blender_path_button = Button(softwares_frame, text = "Browse", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        blender_path_button["command"] = lambda: self.blenderPathEntry()
        blender_path_button.grid(row = 5, column = 1, sticky = E)

        ## VLC ##
        label = Label(softwares_frame, text = "Path to VLC", bg = self.main_color, fg = self.text_color)
        label.grid(row = 6, column = 0, columnspan = 2)

        self.vlc_var_text = StringVar()
        self.vlc_var_text.set(Resources.readLine("save/options.spi", 6))

        self.vlc_path_entry = Entry(softwares_frame, textvariable = self.vlc_var_text, state = DISABLED, width = 75, relief = FLAT, disabledbackground = self.disabled_button_color2, disabledforeground = self.disabled_text_color)
        self.vlc_path_entry.grid(row = 7, column = 0)

        vlc_path_button = Button(softwares_frame, text = "Browse", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        vlc_path_button["command"] = lambda: self.vlcPathEntry()
        vlc_path_button.grid(row = 7, column = 1, sticky = E)

        ## CUSTOM LINK ##
        label = Label(softwares_frame, text = "Edit custom link", bg = self.main_color, fg = self.text_color)
        label.grid(row = 8, column = 0, columnspan = 2)

        self.var_custom_link = StringVar()
        self.var_custom_link.set(Resources.readLine(project_options_path, 1))

        self.link_entry = Entry(softwares_frame, textvariable = self.var_custom_link, width = 75, relief = FLAT, bg = self.button_color2)
        self.link_entry.grid(row = 9, column = 0, columnspan = 2, sticky = W + E)

        ## // THEME \\ ##
        themes_frame = Frame(tabs_frame, borderwidth = 0, bg = self.main_color)
        themes_frame.pack()

        label = Label(themes_frame, text = "Select theme", bg = self.main_color, fg = self.text_color)
        label.grid(row = 0, column = 0, columnspan = 4, sticky = W + E)

        self.rb_theme = IntVar()
        self.themes_list = sorted(listdir("save/themes/"))
        i = 0

        for theme in self.themes_list:
            themes_frame.columnconfigure(int(i/4) + 1, weight = 1)
            rb_theme = Radiobutton(themes_frame, text = path.splitext(theme)[0], variable = self.rb_theme, value = i, bg = self.main_color, activebackground = self.main_color, fg = self.text_color, activeforeground = self.text_color, selectcolor = self.second_color)
            rb_theme.grid(row = int(i/4) + 1, column = i % 4, sticky = W)

            if self.theme == path.splitext(theme)[0]:
                rb_theme.select()

            i += 1

        tabs_frame.add(softwares_frame, text = "Softwares", padding = 10)
        tabs_frame.add(themes_frame, text = "Themes", padding = 10)
        tabs_frame.grid(row = 0, column = 0, sticky = W + E, columnspan = 4)

        ## SAVE/CANCEL ##
        save_button = Button(self.top, text = "Save", bg = self.button_color1, activebackground = self.over_button_color1, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        save_button["command"] = lambda: self.saveEntry(dict_key)
        save_button.grid(row = 1, column = 0, sticky = W, pady = 10, padx = 10)

        cancel_button = Button(self.top, text = "Cancel", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        cancel_button["command"] = self.top.destroy
        cancel_button.grid(row = 1, column = 3, sticky = E, pady = 10, padx = 10)

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

    def blenderPathEntry(self):
        blender_path = filedialog.askopenfilename(title = "Select Blender.exe",  filetypes = [("Blender","*Blender*.exe")])

        if blender_path:
            self.blender_var_text.set(blender_path)

        self.top.focus()

    def vlcPathEntry(self):
        vlc_path = filedialog.askopenfilename(title = "Select vlc.exe",  filetypes = [("VLC","*vlc*.exe")])

        if vlc_path:
            self.vlc_var_text.set(vlc_path)

        self.top.focus()

    def saveEntry(self, dict_key):
        custom_link = self.link_entry.get()
        maya_path = self.maya_path_entry.get()
        houdini_path = self.houdini_path_entry.get()
        blender_path = self.blender_path_entry.get()
        vlc_path = self.vlc_path_entry.get()
        theme = path.splitext(self.themes_list)[self.rb_theme.get()])[0]
        if custom_link and maya_path and houdini_path and blender_path and vlc_path and theme:
            d, key1, key2, key3, key4, key5, key6 = dict_key
            d[key1] = custom_link
            d[key2] = maya_path
            d[key3] = houdini_path
            d[key4] = blender_path
            d[key5] = vlc_path
            d[key6] = theme
            self.top.destroy()
