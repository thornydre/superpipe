#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from tkinter import *
from Resources import *
from tkinter import ttk

class ManageBackupsDialog(object):
    def __init__(self, parent, project, dict_key = None):
        ## THEME COLORS ##
        self.main_color = Resources.readLine("save/themes.spi", 1)
        self.second_color = Resources.readLine("save/themes.spi", 2)
        self.list_color = Resources.readLine("save/themes.spi", 3)
        self.button_color1 = Resources.readLine("save/themes.spi", 4)
        self.over_button_color1 = Resources.readLine("save/themes.spi", 5)
        self.button_color2 = Resources.readLine("save/themes.spi", 6)
        self.over_button_color2 = Resources.readLine("save/themes.spi", 7)
        self.text_color = Resources.readLine("save/themes.spi", 9)

        self.root = parent
        self.top = Toplevel(self.root)
        self.top.transient(self.root)
        self.top.title("Super Pipe || Clean backups")
        self.top["bg"] = self.main_color

        self.top.resizable(width = False, height = False)

        self.project = project

        top_frame = Frame(self.top, borderwidth = 0, bg = self.main_color)
        top_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

        top_frame.columnconfigure(0, pad = 5)
        top_frame.columnconfigure(1, pad = 5)
        
        top_frame.rowconfigure(0, pad = 5)
        top_frame.rowconfigure(1, pad = 5)
        top_frame.rowconfigure(2, pad = 5)
        top_frame.rowconfigure(3, pad = 5)
        top_frame.rowconfigure(4, pad = 5)

        label = Label(top_frame, text = "Select backups to delete", bg = self.main_color, fg = self.text_color)
        label.grid(row = 0, column = 0, columnspan = 2)

        self.backup_list = ttk.Treeview(top_frame, height = 15, show = "tree")
        ttk.Style().configure("Treeview", background = self.list_color)
        self.backup_list.insert("", 1, "shots", text = "SHOTS")
        self.backup_list.insert("", 2, "character", text = "CHARACTER")
        self.backup_list.insert("", 3, "fx", text = "FX")
        self.backup_list.insert("", 4, "props", text = "PROPS")
        self.backup_list.insert("", 5, "set", text = "SET")
        self.backup_list.grid(row = 1, column = 0, columnspan = 2)

        for folder in listdir(self.project.getDirectory() + "/05_shot/backup/"):
            self.backup_list.insert("shots", END, folder, text = folder)

        for folder in listdir(self.project.getDirectory() + "/04_asset/character/backup/"):
            self.backup_list.insert("character", END, folder, text = folder)

        for folder in listdir(self.project.getDirectory() + "/04_asset/FX/backup/"):
            self.backup_list.insert("fx", END, folder, text = folder)

        for folder in listdir(self.project.getDirectory() + "/04_asset/props/backup/"):
            self.backup_list.insert("props", END, folder, text = folder)

        for folder in listdir(self.project.getDirectory() + "/04_asset/set/backup/"):
            self.backup_list.insert("set", END, folder, text = folder)

        submit_button = Button(top_frame, text = "Delete", bg = self.button_color1, activebackground = self.over_button_color1, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 12, height = 1)
        submit_button["command"] = lambda: self.submit(dict_key)
        submit_button.grid(row = 2, column = 0, sticky = W, pady = (10, 0))

        self.top.bind("<Return>", lambda event, a = dict_key:self.submit(a))

        cancel_button = Button(top_frame, text = "Cancel", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 8, height = 1)
        cancel_button["command"] = self.top.destroy
        cancel_button.grid(row = 2, column = 1, sticky = E, pady = (10, 0))

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
        backups = self.backup_list.selection()

        categories = ["shots", "character", "fx", "props", "set"]

        for backup in backups:
            if backup not in categories:
                if self.backup_list.parent(backup) == "shots":
                    rmtree(self.project.getDirectory() + "/05_shot/backup/" + backup)
                else:
                    rmtree(self.project.getDirectory() + "/04_asset/" + self.backup_list.parent(backup) + "/backup/" + backup)

        self.top.destroy()
