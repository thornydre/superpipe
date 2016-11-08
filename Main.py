#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from NewProjectDialog import *
from Shot import *
from Project import *
from Resources import *
from tkinter import *
from tkinter import filedialog, ttk
from os import path, makedirs
from urllib.parse import urlsplit

import NewShotDialog
import NewAssetDialog
import RenameAssetDialog
import PreferencesDialog
import EditCustomLinkDialog
import YesNoDialog
import OkDialog
import subprocess
import webbrowser

class SuperPipe(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg = "#666666")

        self.parent = parent

        self.current_project = None
        self.current_sequence = 1

        if not path.isfile("save/options.spi"):
            with open("save/options.spi", "w") as f:
                f.write("C:/Program Files/Autodesk/Maya2017/bin/maya.exe\nC:/Program Files/Autodesk/Maya2017/bin/maya.exe\n\n")
            f.close()

        self.maya_path = Resources.readLine("save/options.spi", 1)
        self.nuke_path = Resources.readLine("save/options.spi", 2)

        self.initUI()

    def initUI(self):
        self.parent["bg"] = "#666666"
        self.parent.title("Super Pipe")
        self.grid(sticky = N + S + E + W)

        self.parent.bind("<F5>", self.refresh)

        menu_bar = Menu(self.parent)

        menu_file = Menu(menu_bar, tearoff = 0)
        menu_file.add_command(label="New project", command = self.newProjectCommand)
        menu_file.add_command(label="Set project", command = self.setProjectCommand)
        menu_file.add_separator()
        menu_file.add_command(label="Quit", command = self.parent.destroy)
        menu_bar.add_cascade(label="File", menu = menu_file)

        menu_edit = Menu(menu_bar, tearoff = 0)
        menu_edit.add_command(label = "Clean backups", command = self.cleanBackupsCommand)
        menu_edit.add_command(label = "Clean student versions", command = self.cleanStudentCommand)
        menu_edit.add_separator()
        menu_edit.add_command(label = "Edit custom link", command = self.editCustomLinkCommand)
        menu_edit.add_command(label = "Preferences", command = self.preferencesCommand)
        menu_bar.add_cascade(label = "Edit", menu = menu_edit)

        menu_help = Menu(menu_bar, tearoff = 0)
        menu_help.add_command(label = "Credits", command = self.about)
        menu_bar.add_cascade(label = "Help", menu = menu_help)

        self.parent.config(menu = menu_bar)

        self.parent.columnconfigure(0, pad = 0)
        self.parent.columnconfigure(1, pad = 0)
        self.parent.columnconfigure(2, pad = 0, weight = 2)
        self.parent.columnconfigure(3, pad = 0)
        self.parent.columnconfigure(4, pad = 0)

        self.parent.rowconfigure(0, pad = 0)

        ###############################################################################################################

        ## // SIDE BAR \\ ##
        left_side_bar = Frame(self.parent, bg = "#666666")
        left_side_bar.grid(row = 0, column = 0, sticky = N)

        left_side_bar.columnconfigure(0, pad = 0)
        left_side_bar.columnconfigure(1, pad = 0)

        left_side_bar.rowconfigure(0, pad = 20)
        left_side_bar.rowconfigure(1, pad = 5)
        left_side_bar.rowconfigure(2, pad = 5)
        left_side_bar.rowconfigure(3, pad = 5)
        left_side_bar.rowconfigure(4, pad = 5)
        left_side_bar.rowconfigure(5, pad = 20)

        self.add_asset_button = Button(left_side_bar, text = "Add asset", state = DISABLED, bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1, command = self.addAssetCommand)
        self.add_asset_button.grid(row = 0, column = 0)

        self.add_shot_button = Button(left_side_bar, text = "Add shot", state = DISABLED, bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1, command = self.addShotCommand)
        self.add_shot_button.grid(row = 0, column = 1)

        ## ASSETS LIST ##
        asset_label = Label(left_side_bar, text = "Assets", bg = "#666666", font = "Helvetica 10 bold")
        asset_label.grid(row = 1, column = 0, columnspan = 2)

        self.asset_list = ttk.Treeview(left_side_bar, height = 8, show = "tree", selectmode = "browse")
        ttk.Style().configure("Treeview", background = "#777777")
        self.asset_list.tag_configure("done", background = "#89C17F")
        self.asset_list.tag_configure("urgent", background = "#E55252")
        self.asset_list.insert("", 1, "character", text = "CHARACTER")
        self.asset_list.insert("", 3, "fx", text = "FX")
        self.asset_list.insert("", 4, "props", text = "PROPS")
        self.asset_list.insert("", 5, "set", text = "SET")
        self.asset_list.grid(row = 2, column = 0, columnspan = 2, sticky = N + S + W + E)
        self.asset_list.bind("<ButtonRelease-1>", self.assetListCommand)

        ## SHOTS LIST ##
        shot_label = Label(left_side_bar, text = "Shots", bg = "#666666", font = "Helvetica 10 bold")
        shot_label.grid(row = 3, column = 0, columnspan = 2)

        self.shot_list = Listbox(left_side_bar, bg = "#777777", selectbackground = "#555555", bd = 0, highlightthickness = 0, width = 30, height = 40, exportselection = False)
        self.shot_list.grid(row = 4, column = 0, columnspan = 2, sticky = N + S + W + E)
        self.shot_list.bind("<<ListboxSelect>>", self.shotlistCommand)

        self.shots_preview_button = Button(left_side_bar, text = "Shots preview", state = DISABLED, bg = "#888888", fg = "#FFFFFF", bd = 0, width = 12, height = 1, command = self.shotsPreviewCommand)
        self.shots_preview_button.grid(row = 5, column = 0, columnspan = 2)

        self.custom_button = Button(left_side_bar, text = "Custom link", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 12, height = 1, command = self.customButtonCommand)
        self.custom_button.grid(row = 6, column = 0, columnspan = 2)

        ###############################################################################################################

        separator = Frame(self.parent, bg = "#333333", bd = 0, width = 5, height = 10)
        separator.grid(row = 0, column = 1, sticky = N + S + W + E)

        ###############################################################################################################

        ## // SHOTS MAIN FRAME \\ ##
        self.main_area_shot = Frame(self.parent, bg = "#666666", bd = 0)
        self.main_area_shot.grid(row = 0, column = 2, sticky = N + S + W + E)
        self.main_area_shot.pi = self.main_area_shot.grid_info()

        self.main_area_shot.columnconfigure(0, pad = 10, minsize = 40)
        self.main_area_shot.columnconfigure(1, pad = 10)
        self.main_area_shot.columnconfigure(2, pad = 10, minsize = 50)
        self.main_area_shot.columnconfigure(3, pad = 10)
        self.main_area_shot.columnconfigure(4, pad = 10, weight = 2)
        self.main_area_shot.columnconfigure(5, pad = 10)

        self.main_area_shot.rowconfigure(0, pad = 20, minsize = 75)
        self.main_area_shot.rowconfigure(1, pad = 5, minsize = 75)
        self.main_area_shot.rowconfigure(2, pad = 5, minsize = 50)
        self.main_area_shot.rowconfigure(3, pad = 5, minsize = 410)

        ## SHOT INFOS ##
        self.up_down_shot = Frame(self.main_area_shot, bg = "#666666", bd = 0)
        self.up_down_shot.grid(row = 0, column = 0, sticky = N + S, pady = 10)
        self.up_down_shot.pi = self.up_down_shot.grid_info()

        self.up_down_shot.columnconfigure(0, pad = 0)

        self.up_down_shot.rowconfigure(0, pad = 0, weight = 1)
        self.up_down_shot.rowconfigure(1, pad = 0, weight = 1)

        self.up_button_img = PhotoImage(file = "img/arrow_up.gif")
        self.up_button = Button(self.up_down_shot, image = self.up_button_img, compound = "left", bg = "#888888", fg = "#FFFFFF", bd = 0, command = self.moveShotDownCommand)
        self.up_button.grid(row = 0, column = 0, sticky = N)
        self.up_button.pi = self.up_button.grid_info()
        self.up_button.grid_forget()

        self.down_button_img = PhotoImage(file = "img/arrow_down.gif")
        self.down_button = Button(self.up_down_shot, image = self.down_button_img, compound = "left", bg = "#888888", fg = "#FFFFFF", bd = 0, command = self.moveShotUpCommand)
        self.down_button.grid(row = 1, column = 0, sticky = S)
        self.down_button.pi = self.down_button.grid_info()
        self.down_button.grid_forget()

        self.var_shot_nb_label = StringVar()
        self.var_shot_nb_label.set("NO SHOT SELECTED")
        shot_nb_label = Label(self.main_area_shot, textvariable = self.var_shot_nb_label, bg = "#666666", height = 1, anchor = NW, font = "Helvetica 11 bold")
        shot_nb_label.grid(row = 0, column = 1)

        self.delete_shot_button_img = PhotoImage(file = "img/red_cross.gif")
        self.delete_shot_button = Button(self.main_area_shot, image = self.delete_shot_button_img, bg = "#666666", activebackground = "#666666", cursor = "hand2", fg = "#FFFFFF", bd = 0, command = self.deleteShotCommand)
        self.delete_shot_button.grid(row = 0, column = 2)
        self.delete_shot_button.pi = self.delete_shot_button.grid_info()
        self.delete_shot_button.grid_forget()

        self.set_shot_button = Button(self.main_area_shot, text = "Set shot", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1, command = self.setShotCommand)
        self.set_shot_button.grid(row = 0, column = 3)
        self.set_shot_button.pi = self.set_shot_button.grid_info()
        self.set_shot_button.grid_forget()

        self.var_selection_path_label = StringVar()
        shot_path_label = Label(self.main_area_shot, textvariable = self.var_selection_path_label, bg = "#666666", height = 1, anchor = NW)
        shot_path_label.grid(row = 0, column = 4)

        self.var_check_show_last = IntVar()
        shot_show_last_only_button = Checkbutton(self.main_area_shot, text = "Show only last versions", variable = self.var_check_show_last, bg = "#666666", activebackground = "#666666", command = self.toggleLastVersions)
        shot_show_last_only_button.grid(row = 0, column = 5, sticky = E)

        ## SHOT STATE ##
        self.shot_state_line = Frame(self.main_area_shot, bg = "#666666", bd = 0)
        self.shot_state_line.grid(row = 1, column = 0, columnspan = 6, sticky = W + E, pady = 10)

        self.shot_state_line.columnconfigure(0, pad = 10)
        self.shot_state_line.columnconfigure(1, pad = 10)
        self.shot_state_line.columnconfigure(2, pad = 10)

        self.priority_shot_label = Label(self.shot_state_line, text = "Priority : ", bg = "#666666", height = 1, anchor = NW, font = "Helvetica 9 bold")
        self.priority_shot_label.grid(row = 0, column = 0, sticky = E)
        self.priority_shot_label.pi = self.priority_shot_label.grid_info()
        self.priority_shot_label.grid_forget()

        self.var_shot_priority = StringVar(self.shot_state_line)
        self.var_shot_priority.set("Low")

        self.priority_shot_menu = OptionMenu(self.shot_state_line, self.var_shot_priority, "Low", "Medium", "High", "Urgent", command = self.priorityShotCommand)
        self.priority_shot_menu.config(bg = "#888888", activebackground = "#888888", bd = 0, width = 8)
        self.priority_shot_menu.grid(row = 0, column = 2, sticky = W)
        self.priority_shot_menu.pi = self.priority_shot_menu.grid_info()
        self.priority_shot_menu.grid_forget()

        self.var_shot_done = IntVar()
        self.done_shot_button = Checkbutton(self.shot_state_line, text = "Shot done", variable = self.var_shot_done, bg = "#666666", activebackground = "#666666", command = self.toggleShotDone)
        self.done_shot_button.grid(row = 0, column = 3)
        self.done_shot_button.pi = self.done_shot_button.grid_info()
        self.done_shot_button.grid_forget()

        ## SHOT ACTIONS ##
        self.shot_actions_line = Frame(self.main_area_shot, bg = "#666666", bd = 0)
        self.shot_actions_line.grid(row = 2, column = 0, columnspan = 6, sticky = W + E, pady = 10)

        self.shot_actions_line.columnconfigure(0, pad = 10)
        self.shot_actions_line.columnconfigure(1, pad = 10, weight = 1)
        self.shot_actions_line.columnconfigure(2, pad = 10)

        self.open_shot_layout_button = Button(self.shot_actions_line, text = "Open shot", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 13, height = 1, command = self.openShotCommand)
        self.open_shot_layout_button.grid(row = 0, column = 1, sticky = N)
        self.open_shot_layout_button.pi = self.open_shot_layout_button.grid_info()
        self.open_shot_layout_button.grid_forget()

        ## PICTURES ##
        pictures_shot = Frame(self.main_area_shot, bg = "#555555", bd = 0)
        pictures_shot.grid(row = 3, column = 0, columnspan = 6, sticky = N + S + W + E, pady = 20)

        pictures_shot.columnconfigure(0, weight = 2, minsize = 550)
        pictures_shot.columnconfigure(1, weight = 2, minsize = 550)

        prev_pict_label = Label(pictures_shot, text = "Previous shot", bg = "#555555", height = 1, anchor = N, font = "Helvetica 11")
        prev_pict_label.grid(row = 0, column = 0, pady = 10)

        self.shot_prev_pict_caneva = Canvas(pictures_shot, bg = "#555555", bd = 0, highlightthickness = 0)
        self.shot_prev_pict_caneva.grid(row = 1, column = 0, pady = 20)
        self.shot_prev_pict_caneva.pi = self.shot_prev_pict_caneva.grid_info()
        self.shot_prev_pict_caneva.grid_forget()
        self.shot_prev_gifdict = {}

        shot_nb_label = Label(pictures_shot, text = "This shot", bg = "#555555", height = 1, anchor = N, font = "Helvetica 11")
        shot_nb_label.grid(row = 0, column = 1, pady = 10)

        self.shot_pict_caneva = Canvas(pictures_shot, bg = "#555555", bd = 0, highlightthickness = 0)
        self.shot_pict_caneva.grid(row = 1, column = 1, pady = 20)
        self.shot_pict_caneva.pi = self.shot_pict_caneva.grid_info()
        self.shot_pict_caneva.grid_forget()
        self.shot_gifdict = {}

        ###############################################################################################################

        ## // ASSETS MAIN FRAME \\ ##
        self.main_area_asset = Frame(self.parent, bg = "#666666", bd = 0, width = 1000, height = 300)
        self.main_area_asset.grid(row = 0, column = 2, sticky = N + S + W + E)
        self.main_area_asset.pi = self.main_area_asset.grid_info()
        self.main_area_asset.grid_forget()

        self.main_area_asset.columnconfigure(0, pad = 10, minsize = 40)
        self.main_area_asset.columnconfigure(1, pad = 10)
        self.main_area_asset.columnconfigure(2, pad = 10, minsize = 50)
        self.main_area_asset.columnconfigure(3, pad = 10)
        self.main_area_asset.columnconfigure(4, pad = 10, weight = 2)
        self.main_area_asset.columnconfigure(5, pad = 10)

        self.main_area_asset.rowconfigure(0, pad = 20, minsize = 75)
        self.main_area_asset.rowconfigure(1, pad = 5, minsize = 75)
        self.main_area_asset.rowconfigure(2, pad = 5, minsize = 30)
        self.main_area_asset.rowconfigure(3, pad = 5, minsize = 410)

        self.var_asset_label = StringVar()
        self.var_asset_label.set("NO ASSET SELECTED")
        shot_nb_label = Label(self.main_area_asset, textvariable = self.var_asset_label, bg = "#666666", height = 1, anchor = NW, font = "Helvetica 11 bold")
        shot_nb_label.grid(row = 0, column = 0)

        self.delete_asset_button_img = PhotoImage(file = "img/red_cross.gif")
        self.delete_asset_button = Button(self.main_area_asset, image = self.delete_asset_button_img, bg = "#666666", activebackground = "#666666", fg = "#FFFFFF", cursor = "hand2", bd = 0, command = self.deleteAssetCommand)
        self.delete_asset_button.grid(row = 0, column = 1)
        self.delete_asset_button.pi = self.delete_asset_button.grid_info()
        self.delete_asset_button.grid_forget()

        self.rename_asset_button = Button(self.main_area_asset, text = "Rename asset", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 12, height = 1, command = self.renameAssetCommand)
        self.rename_asset_button.grid(row = 0, column = 2)
        self.rename_asset_button.pi = self.rename_asset_button.grid_info()
        self.rename_asset_button.grid_forget()

        self.set_asset_button = Button(self.main_area_asset, text = "Set asset", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 8, height = 1, command = self.setAssetCommand)
        self.set_asset_button.grid(row = 0, column = 3)
        self.set_asset_button.pi = self.set_asset_button.grid_info()
        self.set_asset_button.grid_forget()

        asset_path_label = Label(self.main_area_asset, textvariable = self.var_selection_path_label, bg = "#666666", height = 1, anchor = NW)
        asset_path_label.grid(row = 0, column = 4)

        asset_show_last_only_button = Checkbutton(self.main_area_asset, text = "Show only last versions", variable = self.var_check_show_last, bg = "#666666", activebackground = "#666666", command = self.toggleLastVersions)
        asset_show_last_only_button.grid(row = 0, column = 5)

        ## ASSET STATE ##
        self.asset_state_line = Frame(self.main_area_asset, bg = "#666666", bd = 0)
        self.asset_state_line.grid(row = 1, column = 0, columnspan = 6, sticky = W + E, pady = 10)

        self.asset_state_line.columnconfigure(0, pad = 10)
        self.asset_state_line.columnconfigure(1, pad = 10)
        self.asset_state_line.columnconfigure(2, pad = 10)

        self.priority_asset_label = Label(self.asset_state_line, text = "Priority : ", bg = "#666666", height = 1, anchor = NW, font = "Helvetica 9 bold")
        self.priority_asset_label.grid(row = 0, column = 0, sticky = E)
        self.priority_asset_label.pi = self.priority_asset_label.grid_info()
        self.priority_asset_label.grid_forget()

        self.var_asset_priority = StringVar(self.asset_state_line)
        self.var_asset_priority.set("Low")

        self.priority_asset_menu = OptionMenu(self.asset_state_line, self.var_asset_priority, "Low", "Medium", "High", "Urgent", command = self.priorityAssetCommand)
        self.priority_asset_menu.config(bg = "#888888", activebackground = "#888888", bd = 0, width = 8)
        self.priority_asset_menu.grid(row = 0, column = 2, sticky = W)
        self.priority_asset_menu.pi = self.priority_asset_menu.grid_info()
        self.priority_asset_menu.grid_forget()

        self.var_asset_done = IntVar()
        self.done_asset_button = Checkbutton(self.asset_state_line, text = "Asset done", variable = self.var_asset_done, bg = "#666666", activebackground = "#666666", command = self.toggleAssetDone)
        self.done_asset_button.grid(row = 0, column = 3)
        self.done_asset_button.pi = self.done_asset_button.grid_info()
        self.done_asset_button.grid_forget()

        ## ASSET ACTIONS ##
        self.asset_actions_line = Frame(self.main_area_asset, bg = "#666666", bd = 0)
        self.asset_actions_line.grid(row = 2, column = 0, columnspan = 6, sticky = W + E, pady = 10)

        self.asset_actions_line.columnconfigure(0, pad = 10)
        self.asset_actions_line.columnconfigure(1, pad = 10, weight = 1)
        self.asset_actions_line.columnconfigure(2, pad = 10)

        self.open_asset_button = Button(self.asset_actions_line, text = "Open asset", bg = "#888888", fg = "#FFFFFF", bd = 0, width = 13, height = 1, command = self.openAssetCommand)
        self.open_asset_button.grid(row = 0, column = 1, sticky = N)
        self.open_asset_button.pi = self.open_asset_button.grid_info()
        self.open_asset_button.grid_forget()

        ## PICTURES ##
        pictures_asset = Frame(self.main_area_asset, bg = "#555555", bd = 0)
        pictures_asset.grid(row = 3, column = 0, columnspan = 6, sticky = N + S + W + E, pady = 20)

        pictures_asset.columnconfigure(0, weight = 1)

        prev_pict_label = Label(pictures_asset, text = "This asset", bg = "#555555", height = 1, anchor = N, font = "Helvetica 11")
        prev_pict_label.grid(row = 0, column = 0, pady = 10)

        self.asset_pict_caneva = Canvas(pictures_asset, bg = "#555555")
        self.asset_pict_caneva.grid(row = 1, column = 0, pady = 20)
        self.asset_pict_caneva.pi = self.asset_pict_caneva.grid_info()
        self.asset_pict_caneva.grid_forget()
        self.asset_gifdict = {}

        ###############################################################################################################

        ## SHOTS PREVIEW ##
        self.main_area_preview = Frame(self.parent, bg = "#666666", bd = 0, width = 100, height = 100)
        self.main_area_preview.grid(row = 0, column = 2, sticky = N + W + E)
        self.main_area_preview.pi = self.main_area_preview.grid_info()
        self.main_area_preview.grid_forget()

        self.preview_canva_scroll = Canvas(self.main_area_preview, bg = "#666666", bd = 0, highlightthickness = 0, yscrollincrement = 20)

        self.shots_preview_list = Frame(self.preview_canva_scroll, bg = "#666666", bd = 0, width = 1000, height = 300)
        self.shots_preview_list.grid()

        self.shots_preview_list.columnconfigure(0, pad = 25, weight = 1)
        self.shots_preview_list.columnconfigure(1, pad = 25, weight = 1)
        self.shots_preview_list.columnconfigure(2, pad = 25, weight = 1)
        self.shots_preview_list.columnconfigure(3, pad = 25, weight = 1)
        self.shots_preview_list.columnconfigure(4, pad = 25, weight = 1)

        scrollbar = Scrollbar(self.main_area_preview, orient = "vertical", bd = 0, command = self.preview_canva_scroll.yview)
        self.preview_canva_scroll.configure(yscrollcommand = scrollbar.set)

        scrollbar.pack(side = "right", fill = "y")
        self.preview_canva_scroll.pack(side="left")
        self.preview_canva_scroll.create_window((0, 0), window = self.shots_preview_list, anchor = N + W)
        self.shots_preview_list.bind("<Configure>", self.scrollCommand)
        self.shots_preview_list.bind("<MouseWheel>", self.wheelScrollCommand)

        self.preview_gifdict = {}

        ###############################################################################################################

        separator = Frame(self.parent, bg = "#333333", bd = 0, width = 5, height = 10)
        separator.grid(row = 0, column = 3, sticky = N + S + W + E)

        ###############################################################################################################

        right_side_bar = Frame(self.parent, bg = "#666666")
        right_side_bar.grid(row = 0, column = 4, sticky = N)

        right_side_bar.columnconfigure(0, pad = 0)

        right_side_bar.rowconfigure(0, pad = 20)
        right_side_bar.rowconfigure(1, pad = 5)

        ## VERSIONS ##
        versions_label = Label(right_side_bar, text = "Versions", bg = "#666666", font = "Helvetica 10 bold")
        versions_label.grid(row = 1, column = 0, columnspan = 2)

        self.version_list = Listbox(right_side_bar, bg = "#777777", selectbackground = "#555555", bd = 0, highlightthickness = 0, width = 50, height = 70, exportselection = False)
        self.version_list.grid(row = 4, column = 0, columnspan = 2, sticky = N + S + W + E)
        self.version_list.bind("<<ListboxSelect>>", self.versionslistCommand)

        ###############################################################################################################

        project_directory = Resources.readLine("save/options.spi", 3)

        if project_directory:
            if path.isdir(project_directory):
                self.current_project = Project(project_directory)
                self.current_sequence = self.current_project.getCurrentSequence()
                self.add_shot_button.config(state = NORMAL)
                self.add_asset_button.config(state = NORMAL)
                self.shots_preview_button.config(state = NORMAL)

                self.parent.title("Super Pipe || " + self.current_project.getDirectory())

                self.updateShotListView()
                self.updateAssetListView()

    def newProjectCommand(self):
        NewProjectDialog.root = self.parent

        self.current_sequence = 1

        directory = {"dir":""}

        dialog = lambda: NewProjectDialog.NewProjectDialog((directory, "dir"))
        self.wait_window(dialog().top)

        if directory["dir"]:
            self.current_project = Project(directory["dir"])
            self.current_sequence = self.current_project.getCurrentSequence()

            Resources.writeAtLine("save/options.spi", directory["dir"], 3)

            self.add_shot_button.config(state = NORMAL)
            self.add_asset_button.config(state = NORMAL)
            self.shots_preview_button.config(state = NORMAL)

            self.parent.title("Super Pipe || " + self.current_project.getDirectory())

            self.updateShotListView()
            self.updateAssetListView()

    def setProjectCommand(self):
        directory = filedialog.askdirectory(title = "New project", mustexist  = False)

        if directory:
            self.current_project = Project(directory)

            Resources.writeAtLine("save/options.spi", directory, 3)

            self.current_sequence = self.current_project.getCurrentSequence()

            self.add_shot_button.config(state = NORMAL)
            self.add_asset_button.config(state = NORMAL)
            self.shots_preview_button.config(state = NORMAL)

            self.parent.title("Super Pipe || " + self.current_project.getDirectory())

            self.updateShotListView()
            self.updateAssetListView()

    def setShotCommand(self):
        selected_line = self.shot_list.curselection()[0]
        selected_shot = self.shot_list.get(selected_line)

        shot = self.current_project.getSelection()
        shot.setShot()

        self.set_shot_button.grid_forget()
        self.open_shot_layout_button.grid(self.open_shot_layout_button.pi)
        self.done_shot_button.grid(self.done_shot_button.pi)

        self.updateVersionListView(shot = shot)
        self.version_list.select_set(0)

        selected_line = self.version_list.curselection()[0]
        self.var_selection_path_label.set(self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.get(selected_line))

        self.versionslistCommand(None)

    def setAssetCommand(self):
        selected_asset = self.asset_list.focus()

        asset = self.current_project.getSelection()
        asset.setAsset()

        self.set_asset_button.grid_forget()
        self.open_asset_button.grid(self.open_asset_button.pi)
        self.done_asset_button.grid(self.done_asset_button.pi)

        self.updateVersionListView(asset = asset)
        self.version_list.select_set(0)

        self.versionslistCommand(None)

    def deleteShotCommand(self):
        selected_line = self.shot_list.curselection()[0]
        selected_shot = self.shot_list.get(selected_line)

        yesno = {"result" : ""}

        dialog = lambda: YesNoDialog.YesNoDialog("Delete shot", "Delete shot \"" + selected_shot + "\" ?", (yesno, "result"))
        self.wait_window(dialog().top)

        if yesno["result"] == "yes":
            self.current_project.removeShot(selected_shot)

            self.updateShotListView()

            self.clearMainFrame("shot")

            self.updateVersionListView()

    def deleteAssetCommand(self):
        selected_asset = self.asset_list.focus()

        yesno = {"result" : ""}

        dialog = lambda: YesNoDialog.YesNoDialog("Delete asset", "Delete asset \"" + selected_asset + "\" from \"" + self.asset_list.parent(selected_asset).upper() + "\" category ?", (yesno, "result"))
        self.wait_window(dialog().top)

        if yesno["result"] == "yes":
            self.current_project.removeAsset(selected_asset, self.asset_list.parent(selected_asset))

            self.updateAssetListView()

            self.clearMainFrame("asset")

            self.updateVersionListView()

    def addShotCommand(self):
        NewShotDialog.root = self.parent

        sequence = {"seq": -1}

        dialog = lambda: NewShotDialog.NewShotDialog((sequence, "seq"))
        self.wait_window(dialog().top)

        if sequence["seq"] >= 0:
            self.current_sequence += sequence["seq"]
            self.current_project.createShot(self.current_sequence)
            self.updateShotListView()
            self.shot_list.select_set(END)
            self.shotlistCommand(None)

    def addAssetCommand(self):
        NewAssetDialog.root = self.parent

        asset = {"cat": None, "name" : None}

        dialog = lambda: NewAssetDialog.NewAssetDialog((asset, "cat", "name"))
        self.wait_window(dialog().top)

        if asset["cat"] and asset["name"]:
            if self.current_project.createAsset(asset["name"], Resources.getCategoryName(asset["cat"])):
                self.updateAssetListView()

                self.asset_list.item(Resources.getCategoryName(asset["cat"]), open = True)

                self.asset_list.selection_set(asset["name"])
                self.asset_list.focus_set()
                self.asset_list.focus(asset["name"])
                self.assetListCommand(None)
            else:
                dialog = lambda: OkDialog.OkDialog("Asset already exists", "The asset \"" + asset["name"] + "\" already exists")
                self.wait_window(dialog().top)

    def shotlistCommand(self, e):
        if self.shot_list.size() != 0:
            selected_line = self.shot_list.curselection()[0]
            selected_shot = self.shot_list.get(selected_line)
            self.var_shot_nb_label.set(selected_shot.replace("s", "SEQUENCE ").replace("p", " SHOT "))

            if selected_line == 0 and selected_line == self.shot_list.size() - 1:
                self.up_button.grid_forget()
                self.down_button.grid_forget()
            elif selected_line == 0:
                self.up_button.grid_forget()
                self.down_button.grid(self.down_button.pi)
            elif selected_line == self.shot_list.size() - 1:
                self.down_button.grid_forget()
                self.up_button.grid(self.up_button.pi)
            else:
                self.down_button.grid(self.down_button.pi)
                self.up_button.grid(self.up_button.pi)

            self.main_area_shot.grid(self.main_area_shot.pi)
            self.main_area_asset.grid_forget()
            self.main_area_preview.grid_forget()

            self.asset_list.selection_remove(self.asset_list.focus())

            self.delete_shot_button.grid(self.delete_shot_button.pi)

            self.current_project.setSelection(shot_name = selected_shot)
            shot = self.current_project.getSelection()

            self.updateVersionListView(shot = shot)
            self.version_list.select_set(0)

            self.var_shot_done.set(int(Resources.readLine(shot.getDirectory() + "/data/shot_data.spi", 1)))
            self.var_shot_priority.set(Resources.readLine(shot.getDirectory() + "/data/shot_data.spi", 2))

            self.priority_shot_label.grid(self.priority_shot_label.pi)
            self.priority_shot_menu.grid(self.priority_shot_menu.pi)

            if shot.isSet():
                self.set_shot_button.grid_forget()
                self.open_shot_layout_button.grid(self.open_shot_layout_button.pi)
                self.done_shot_button.grid(self.done_shot_button.pi)

                pict_path = shot.getDirectory() + "/images/screenshots/" + self.version_list.get(self.version_list.curselection()[0]).strip(".ma") + ".gif"

                selected_line = self.version_list.curselection()[0]
                self.var_selection_path_label.set(self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.get(selected_line))

                if path.isfile(pict_path):
                    pict = PhotoImage(file = pict_path)

                    self.shot_gifdict[pict_path] = pict

                    self.shot_pict_caneva.grid(self.shot_pict_caneva.pi)
                    self.shot_pict_caneva.create_image(0, 0, anchor = N + W, image = pict)
                    self.shot_pict_caneva.config(height = pict.height(), width = pict.width())

                else:
                    self.shot_pict_caneva.grid_forget()

            else:
                self.set_shot_button.grid(self.set_shot_button.pi)
                self.open_shot_layout_button.grid_forget()
                self.done_shot_button.grid_forget()

                self.shot_pict_caneva.grid_forget()

                self.var_selection_path_label.set("")

            prev_pict_path = ""

            prev_shot_nb = shot.getShotNb() - 1

            if prev_shot_nb > 0:
                for shot_dir in listdir(self.current_project.getDirectory() + "/05_shot/"):
                    if shot_dir != "backup":
                        if int(shot_dir[-2:]) == prev_shot_nb:
                            all_picts_path = self.current_project.getDirectory() + "/05_shot/" + shot_dir + "/images/screenshots/"

                            all_picts_path_array = []

                            for f in listdir(all_picts_path):
                                if "small.gif" not in f:
                                    all_picts_path_array.append(all_picts_path + f)

                            if all_picts_path_array:
                                prev_pict_path = max(all_picts_path_array, key = path.getmtime)

            if path.isfile(prev_pict_path):
                pict = PhotoImage(file = prev_pict_path)

                self.shot_prev_gifdict[prev_pict_path] = pict

                self.shot_prev_pict_caneva.grid(self.shot_prev_pict_caneva.pi)
                self.shot_prev_pict_caneva.create_image(0, 0, anchor = N + W, image = pict)
                self.shot_prev_pict_caneva.config(height = pict.height(), width = pict.width())
            else:
                self.shot_prev_pict_caneva.grid_forget()

    def assetListCommand(self, e):
        if self.asset_list.focus():
            self.main_area_asset.grid(self.main_area_asset.pi)
            self.main_area_shot.grid_forget()
            self.main_area_preview.grid_forget()

            self.shot_list.selection_clear(0, END)

            if self.asset_list.focus() not in ["character", "fx", "props", "set"]:
                selected_asset = self.asset_list.focus()

                self.current_project.setSelection(asset_name = selected_asset, asset_cat = self.asset_list.parent(selected_asset))
                asset = self.current_project.getSelection()

                self.var_asset_label.set("ASSET " + self.asset_list.focus().upper())
                self.delete_asset_button.grid(self.delete_asset_button.pi)
                self.rename_asset_button.grid(self.rename_asset_button.pi)

                self.priority_asset_label.grid(self.priority_asset_label.pi)
                self.priority_asset_menu.grid(self.priority_asset_menu.pi)

                self.updateVersionListView(asset = asset)
                self.version_list.select_set(0)

                self.var_asset_done.set(int(Resources.readLine(asset.getDirectory() + "/data/asset_data.spi", 1)))
                self.var_asset_priority.set(Resources.readLine(asset.getDirectory() + "/data/asset_data.spi", 2))

                if asset:
                    if asset.isSet():
                        self.set_asset_button.grid_forget()
                        self.open_asset_button.grid(self.open_asset_button.pi)

                        selected_line = self.version_list.curselection()[0]
                        self.var_selection_path_label.set(self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.get(selected_line))

                        self.done_asset_button.grid(self.done_asset_button.pi)

                        pict_path = asset.getDirectory() + "/images/screenshots/" + self.version_list.get(self.version_list.curselection()[0]).strip(".ma") + ".gif"

                        if path.isfile(pict_path):
                            pict = PhotoImage(file = pict_path)

                            self.asset_gifdict[pict_path] = pict

                            self.asset_pict_caneva.grid(self.asset_pict_caneva.pi)
                            self.asset_pict_caneva.create_image(0, 0, anchor = N + W, image = pict)
                            self.asset_pict_caneva.config(height = pict.height(), width = pict.width())
                        else:
                            self.asset_pict_caneva.grid_forget()
                            
                    else:
                        self.set_asset_button.grid(self.set_asset_button.pi)
                        self.open_asset_button.grid_forget()
                        self.var_selection_path_label.set("")
                        self.asset_pict_caneva.grid_forget()
                        self.done_asset_button.grid_forget()

            else:
                self.var_asset_label.set("NO ASSET SELECTED")
                self.var_selection_path_label.set("")
                self.delete_asset_button.grid_forget()
                self.rename_asset_button.grid_forget()
                self.set_asset_button.grid_forget()
                self.open_asset_button.grid_forget()
                self.version_list.delete(0, END)
                self.asset_pict_caneva.grid_forget()
                self.priority_asset_label.grid_forget()
                self.priority_asset_menu.grid_forget()
                self.done_asset_button.grid_forget()

    def versionslistCommand(self, e):
        if self.version_list.size() != 0:
            self.open_asset_button.grid(self.open_asset_button.pi)

            selected_line = self.version_list.curselection()[0]
            selected_asset_version = self.version_list.get(selected_line)

            if path.isfile(self.current_project.getSelection().getDirectory() + "/scenes/" + selected_asset_version):
                self.var_selection_path_label.set(self.current_project.getSelection().getDirectory() + "/scenes/" + selected_asset_version)
            else:
                self.var_selection_path_label.set(self.current_project.getSelection().getDirectory() + "/scenes/edits/" + selected_asset_version)

            pict_path = self.current_project.getSelection().getDirectory() + "/images/screenshots/" + selected_asset_version.strip(".ma") + ".gif"

            if self.current_project.getSelectionType() == "shot":
                if path.isfile(pict_path):
                    pict = PhotoImage(file = pict_path)

                    self.shot_gifdict[pict_path] = pict

                    self.shot_pict_caneva.grid(self.shot_pict_caneva.pi)
                    self.shot_pict_caneva.create_image(0, 0, anchor = N + W, image = pict)
                    self.shot_pict_caneva.config(height = pict.height(), width = pict.width())
                else:
                    self.shot_pict_caneva.grid_forget()

            elif self.current_project.getSelectionType() == "asset":
                if path.isfile(pict_path):
                    pict = PhotoImage(file = pict_path)

                    self.asset_gifdict[pict_path] = pict

                    self.asset_pict_caneva.grid(self.asset_pict_caneva.pi)
                    self.asset_pict_caneva.create_image(0, 0, anchor = N + W, image = pict)
                    self.asset_pict_caneva.config(height = pict.height(), width = pict.width())
                else:
                    self.asset_pict_caneva.grid_forget()

    def openShotCommand(self):
        selected_line = self.version_list.curselection()[0]
        selected_shot_version = self.version_list.get(selected_line)

        shot = self.current_project.getSelection()

        if path.isfile(self.maya_path):
            if path.isfile(shot.getDirectory() + "/scenes/" + selected_shot_version):
                maya_file = shot.getDirectory() + "/scenes/" + selected_shot_version
            else:
                maya_file = shot.getDirectory() + "/scenes/edits/" + selected_shot_version

            subprocess.Popen("%s %s" % (self.maya_path, maya_file))
        else:
            dialog = lambda: OkDialog.OkDialog("Maya path", "Check Maya path in Edit > Preferences")
            self.wait_window(dialog().top)

    def openAssetCommand(self):
        selected_line = self.version_list.curselection()[0]
        selected_asset_version = self.version_list.get(selected_line)

        asset = self.current_project.getSelection()

        if path.isfile(self.maya_path):
            if path.isfile(asset.getDirectory() + "/scenes/" + selected_asset_version):
                maya_file = asset.getDirectory() + "/scenes/" + selected_asset_version
            else:
                maya_file = asset.getDirectory() + "/scenes/edits/" + selected_asset_version

            subprocess.Popen("%s %s" % (self.maya_path, maya_file))
        else:
            dialog = lambda: OkDialog.OkDialog("Maya path", "Check Maya path in Edit > Preferences")
            self.wait_window(dialog().top)

    def renameAssetCommand(self):
        asset_name = {"name" : None}

        dialog = lambda: RenameAssetDialog.RenameAssetDialog((asset_name, "name"))
        self.wait_window(dialog().top)

        if asset_name["name"]:
            asset = self.current_project.getSelection()
            if asset.renameAsset(asset_name["name"]):
                self.current_project.updateAssetList()
                self.updateAssetListView()

                self.asset_list.selection_set(asset_name["name"])
                self.asset_list.focus_set()
                self.asset_list.focus(asset_name["name"])
                self.assetListCommand(None)
            else:
                dialog = lambda: OkDialog.OkDialog("Error", "The asset \"" + asset_name["name"] + "\" already exists !")
                self.wait_window(dialog().top)

    def updateShotListView(self):
        self.shot_list.delete(0, END)

        shots = self.current_project.getShotList()

        for shot in shots:
            self.shot_list.insert(shot[0], shot[1])

            cur_shot = Shot(self.current_project.getDirectory(), shot[1])

            if cur_shot.isDone():
                self.shot_list.itemconfig(shot[0] - 1, bg = "#89C17F", selectbackground = "#466341")
            elif cur_shot.getPriority() == "Urgent":
                self.shot_list.itemconfig(shot[0] - 1, bg = "#E55252", selectbackground = "#822121")
            
    def updateAssetListView(self):
        for child in self.asset_list.get_children("character"):
            self.asset_list.delete(child)
        for child in self.asset_list.get_children("fx"):
            self.asset_list.delete(child)
        for child in self.asset_list.get_children("props"):
            self.asset_list.delete(child)
        for child in self.asset_list.get_children("set"):
            self.asset_list.delete(child)

        assets = self.current_project.getAssetList()

        for asset in assets:
            if asset[0] != "backup":
                cur_asset = Asset(self.current_project.getDirectory(), asset[0], asset[1])

                if cur_asset.isDone():
                    self.asset_list.insert(asset[1], END, asset[0], text = asset[0], tags = ("done"))
                elif cur_asset.getPriority() == "Urgent":
                    self.asset_list.insert(asset[1], END, asset[0], text = asset[0], tags = ("urgent"))
                else:
                    self.asset_list.insert(asset[1], END, asset[0], text = asset[0])

    def updateVersionListView(self, shot = None, asset = None):
        self.version_list.delete(0, END)

        if shot:
            shot_versions = shot.getVersionsList(self.var_check_show_last.get())

            if shot_versions:
                for shot_version in shot_versions:
                    self.version_list.insert(END, shot_version)

        elif asset:
            asset_versions = asset.getVersionsList(self.var_check_show_last.get())

            if asset_versions:
                for asset_version in asset_versions:
                    self.version_list.insert(END, asset_version)

    def moveShotUpCommand(self):
        self.current_project.moveShotUp(self.current_project.getSelection().getShotName())

        new_selection = self.shot_list.curselection()[0] + 1
        self.updateShotListView()
        self.shot_list.select_set(new_selection)

        self.shotlistCommand(None)

    def moveShotDownCommand(self):
        self.current_project.moveShotDown(self.current_project.getSelection().getShotName())

        new_selection = self.shot_list.curselection()[0] - 1
        self.updateShotListView()
        self.shot_list.select_set(new_selection)

        self.shotlistCommand(None)

    def toggleLastVersions(self):
        if self.current_project.getSelectionType() == "shot":
            self.updateVersionListView(shot = self.current_project.getSelection())
        elif self.current_project.getSelectionType() == "asset":
            if self.asset_list.focus() not in ["character", "fx", "props", "set"]:
                self.updateVersionListView(asset = self.current_project.getSelection())

        self.version_list.select_set(0)

    def toggleShotDone(self):
        selected_shot = self.shot_list.curselection()[0]
        self.current_project.getSelection().updateShotState(self.var_shot_priority.get(), self.var_shot_done.get())
        self.updateShotListView()
        self.shot_list.select_set(selected_shot)

    def toggleAssetDone(self):
        selected_asset = self.asset_list.focus()
        self.current_project.getSelection().updateAssetState(self.var_asset_priority.get(), self.var_asset_done.get())
        self.updateAssetListView()
        self.asset_list.selection_set(selected_asset)
        self.asset_list.focus_set()
        self.asset_list.focus(selected_asset)

    def priorityShotCommand(self, priority):
        selected_shot = self.shot_list.curselection()[0]
        self.current_project.getSelection().updateShotState(priority, self.var_shot_done.get())
        self.updateShotListView()
        self.shot_list.select_set(selected_shot)

    def priorityAssetCommand(self, priority):
        selected_asset = self.asset_list.focus()
        self.current_project.getSelection().updateAssetState(priority, self.var_asset_done.get())
        self.updateAssetListView()
        self.asset_list.selection_set(selected_asset)
        self.asset_list.focus_set()
        self.asset_list.focus(selected_asset)

    def shotsPreviewCommand(self):
        self.main_area_shot.grid_forget()
        self.main_area_asset.grid_forget()

        self.main_area_preview.grid(self.main_area_preview.pi)

        self.asset_list.selection_remove(self.asset_list.focus())
        self.shot_list.selection_clear(0, END)

        self.version_list.delete(0, END)

        all_shots_preview = []

        for shot_dir in listdir(self.current_project.getDirectory() + "/05_shot/"):
            if shot_dir != "backup":
                all_picts_path = self.current_project.getDirectory() + "/05_shot/" + shot_dir + "/images/screenshots/"

                all_picts_path_array = []

                for f in listdir(all_picts_path):
                    if "small.gif" in f:
                        all_picts_path_array.append(all_picts_path + f)

                cur_shot = Shot(self.current_project.getDirectory(), shot_dir)

                if all_picts_path_array:
                    all_shots_preview.append([cur_shot.getShotNb(), max(all_picts_path_array, key = path.getmtime)])
                else:
                    all_shots_preview.append([cur_shot.getShotNb(), "img/img_not_available.gif"])

        for nb, img in all_shots_preview:
            shot_preview_caneva = Canvas(self.shots_preview_list, bg = "#555555", bd = 0, highlightthickness = 0)

            pict = PhotoImage(file = img)

            self.preview_gifdict[nb] = pict

            shot_preview_caneva.create_image(0, 0, anchor = N + W, image = pict)
            shot_preview_caneva.config(height = pict.height(), width = pict.width())

            shot_preview_caneva.grid(row = int((nb - 1)/5), column = (nb - 1) % 5, pady = 20)
            shot_preview_caneva.bind("<MouseWheel>", self.wheelScrollCommand)

    ###############################################################################################################

    def editCustomLinkCommand(self):
        if not path.isfile(self.current_project.getDirectory() + "/project_option.spi"):
            with open(self.current_project.getDirectory() + "/project_option.spi", "w") as f:
                f.write("www.google.fr\n")
            f.close()

        link = {"link" : None}

        dialog = lambda: EditCustomLinkDialog.EditCustomLinkDialog(self.current_project.getDirectory() + "/project_option.spi", (link, "link"))
        self.wait_window(dialog().top)

        if link["link"]:
            Resources.writeAtLine(self.current_project.getDirectory() + "/project_option.spi", link["link"], 1)

    def customButtonCommand(self):
        base_url = Resources.readLine(self.current_project.getDirectory() + "/project_option.spi", 1)
        
        # url = urlsplit(base_url)
        # url.geturl()

        webbrowser.open(base_url)

    def clearMainFrame(self, type):
        if type == "shot":
            self.var_shot_nb_label.set("NO SHOT SELECTED")
            self.up_down_shot.grid_forget()
            self.delete_shot_button.grid_forget()
            self.set_shot_button.grid_forget()
            self.var_selection_path_label.set("")
            self.shot_pict_caneva.grid_forget()
            self.open_shot_layout_button.grid_forget()
            self.priority_shot_menu.grid_forget()
            self.priority_shot_label.grid_forget()
            self.done_shot_button.grid_forget()
        elif type == "asset":
            self.var_asset_label.set("NO ASSET SELECTED")
            self.delete_asset_button.grid_forget()
            self.rename_asset_button.grid_forget()
            self.set_asset_button.grid_forget()
            self.var_selection_path_label.set("")
            self.asset_pict_caneva.grid_forget()
            self.open_asset_button.grid_forget()
            self.priority_asset_menu.grid_forget()
            self.priority_asset_label.grid_forget()
            self.done_asset_button.grid_forget()

    def cleanBackupsCommand(self):
        yesno = {"result" : ""}

        dialog = lambda: YesNoDialog.YesNoDialog("Clean backups", "Clean all the backups ?", (yesno, "result"))
        self.wait_window(dialog().top)

        if yesno["result"] == "yes":
            self.current_project.cleanBackups()

    def cleanStudentCommand(self):
        yesno = {"result" : ""}

        dialog = lambda: YesNoDialog.YesNoDialog("Clean student versions", "Make all your files easy to save again ?", (yesno, "result"))
        self.wait_window(dialog().top)

        if yesno["result"] == "yes":
            self.current_project.removeAllStudentVersions()

    def preferencesCommand(self):
        preferences = {"maya_path" : "", "nuke_path" : ""}

        dialog = lambda: PreferencesDialog.PreferencesDialog((preferences, "maya_path", "nuke_path"))
        self.wait_window(dialog().top)

        if preferences["maya_path"] and preferences["nuke_path"]:
            self.maya_path = preferences["maya_path"]
            self.nuke_path = preferences["nuke_path"]

            Resources.writeAtLine("save/options.spi", preferences["maya_path"], 1)
            Resources.writeAtLine("save/options.spi", preferences["nuke_path"], 2)

    def about(self):
        dialog = lambda: OkDialog.OkDialog("Credits", "Super Pipe\nPipeline manager\n(C) Lucas Boutrot")
        self.wait_window(dialog().top)

    def refresh(self, e):
        self.versionslistCommand(None)

    def scrollCommand(self, e):
        self.preview_canva_scroll.configure(scrollregion = self.preview_canva_scroll.bbox("all"), width = 2000, height = self.parent.winfo_height())

    def wheelScrollCommand(self, e):
        self.preview_canva_scroll.yview_scroll(int(-1 * e.delta/120), "units")

def main():
    root = Tk()
    root.geometry("1280x720")
    root.state("zoomed")
    app = SuperPipe(root)
    root.iconbitmap("img/icon.ico")
    root.mainloop()

if __name__ == "__main__":
    main()
