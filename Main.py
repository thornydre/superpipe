#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from NewProjectDialog import *
from Shot import *
from Project import *
from Resources import *
from tkinter import *
from tkinter import filedialog, ttk
from os import path, mkdir
from urllib.parse import urlsplit

import NewShotDialog
import NewAssetDialog
import RenameAssetDialog
import ProjectSettingsDialog
import PreferencesDialog
import EditCustomLinkDialog
import ManageBackupDialog
import YesNoDialog
import OkDialog
import subprocess
import webbrowser

class SuperPipe(Frame):
    def __init__(self, parent):
        ## THEME COLORS ##
        self.main_color = Resources.readLine("save/themes.spi", 1)
        self.second_color = Resources.readLine("save/themes.spi", 2)
        self.list_color = Resources.readLine("save/themes.spi", 3)
        self.button_color1 = Resources.readLine("save/themes.spi", 4)
        self.over_button_color1 = Resources.readLine("save/themes.spi", 5)
        self.button_color2 = Resources.readLine("save/themes.spi", 6)
        self.over_button_color2 = Resources.readLine("save/themes.spi", 7)
        self.separator_color = Resources.readLine("save/themes.spi", 8)
        self.text_color = Resources.readLine("save/themes.spi", 9)
        self.done_color = Resources.readLine("save/themes.spi", 12)
        self.urgent_color = Resources.readLine("save/themes.spi", 13)
        self.high_color = Resources.readLine("save/themes.spi", 14)
        self.medium_color = Resources.readLine("save/themes.spi", 15)

        Frame.__init__(self, parent, bg = self.main_color)

        self.parent = parent

        self.parent.config(cursor = "wait")
        self.parent.update()

        self.current_project = None
        self.current_sequence = 1

        if not path.isfile("save/options.spi"):
            with open("save/options.spi", "w") as f:
                f.write("C:/Program Files/Autodesk/Maya2017/bin/maya.exe\nC:/Program Files/Autodesk/Maya2017/bin/maya.exe\n\n")
            f.close()

        self.maya_path = Resources.readLine("save/options.spi", 1)
        self.nuke_path = Resources.readLine("save/options.spi", 2)

        self.initUI()

        project_directory = Resources.readLine("save/options.spi", 3)

        if project_directory:
            if path.isdir(project_directory):
                self.current_project = Project(project_directory)
                self.current_sequence = self.current_project.getCurrentSequence()
                self.add_shot_button.config(state = NORMAL)
                self.add_asset_button.config(state = NORMAL)
                self.shots_preview_button.config(state = NORMAL)
                self.custom_button.config(state = NORMAL)

                self.parent.title("Super Pipe || " + self.current_project.getDirectory())

                self.asset_list.configure(selectmode = "browse")

                self.updateShotListView()
                self.updateAssetListView()

        self.parent.config(cursor = "")

    def initUI(self):
        self.parent["bg"] = self.main_color
        self.parent.title("Super Pipe")
        self.pack(fill = "both", expand = True)

        self.parent.bind("<F5>", self.refresh)

        menu_bar = Menu(self.parent)

        menu_file = Menu(menu_bar, tearoff = 0)
        menu_file.add_command(label="New project", command = self.newProjectCommand)
        menu_file.add_command(label="Set project", command = self.setProjectCommand)
        menu_file.add_separator()
        menu_file.add_command(label="Update project", command = self.updateProjectCommand)
        menu_file.add_separator()
        menu_file.add_command(label="Quit", command = self.parent.destroy)
        menu_bar.add_cascade(label="File", menu = menu_file)

        menu_edit = Menu(menu_bar, tearoff = 0)
        menu_edit.add_command(label = "Clean backups", command = self.cleanBackupsCommand)
        menu_edit.add_command(label = "Clean student versions", command = self.cleanStudentCommand)
        menu_edit.add_separator()
        menu_edit.add_command(label = "Project settings", command = self.projectSettingsCommand)
        menu_edit.add_separator()
        menu_edit.add_command(label = "Edit custom link", command = self.editCustomLinkCommand)
        menu_edit.add_command(label = "Preferences", command = self.preferencesCommand)
        menu_bar.add_cascade(label = "Edit", menu = menu_edit)

        menu_help = Menu(menu_bar, tearoff = 0)
        menu_help.add_command(label = "Credits", command = self.about)
        menu_bar.add_cascade(label = "Help", menu = menu_help)

        self.parent.config(menu = menu_bar)

        pw_main = PanedWindow(self.parent, orient="horizontal", height = 2000, bg = self.separator_color, bd = 0, sashwidth = 5)
        pw_side_bar = PanedWindow(pw_main, orient = "vertical", width = 250, bg = self.separator_color, bd = 0, sashwidth = 5)
        main = Frame(pw_main, width = 400, height = 400, background = "black")
        pw_side_bar_top = Frame(pw_side_bar, width = 200, height = 200, background = "gray")
        pw_side_bar_bottom = Frame(pw_side_bar, width = 200, height = 200, background = "white")

        pw_main.pack(fill = "both", expand = True)

        pw_main.add(pw_side_bar)
        pw_main.paneconfigure(pw_side_bar, minsize = 200)

        ###############################################################################################################
       
        top_left_side_bar = Frame(pw_side_bar, bg = self.main_color)

        add_buttons = Frame(top_left_side_bar, bg = self.main_color)
        add_buttons.pack(fill = X, pady = 10)

        add_buttons.columnconfigure(0, weight = 1)
        add_buttons.columnconfigure(1, weight = 1)

        self.add_asset_button = Button(add_buttons, text = "Add asset", state = DISABLED, bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 8, height = 1, command = self.addAssetCommand)
        self.add_asset_button.grid(row = 0, column = 0, sticky = N)

        self.add_shot_button = Button(add_buttons, text = "Add shot", state = DISABLED, bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 8, height = 1, command = self.addShotCommand)
        self.add_shot_button.grid(row = 0, column = 1, sticky = N)

        ## ASSETS LIST ##
        asset_label = Label(top_left_side_bar, text = "Assets", bg = self.main_color, fg = self.text_color, font = "Helvetica 10 bold")
        asset_label.pack(fill = X, pady = 10)

        self.asset_list = ttk.Treeview(top_left_side_bar, height = 16, show = "tree", selectmode = "none")
        ttk.Style().configure("Treeview", background = self.list_color)
        self.asset_list.tag_configure("done", background = self.done_color)
        self.asset_list.tag_configure("urgent", background = self.urgent_color)
        self.asset_list.tag_configure("high", background = self.high_color)
        self.asset_list.tag_configure("medium", background = self.medium_color)
        self.asset_list.insert("", 1, "character", text = "CHARACTER")
        self.asset_list.insert("", 2, "fx", text = "FX")
        self.asset_list.insert("", 3, "props", text = "PROPS")
        self.asset_list.insert("", 4, "set", text = "SET")
        self.asset_list.pack(fill = BOTH, expand = Y)
        self.asset_list.bind("<ButtonRelease-1>", self.assetListCommand)

        pw_side_bar.add(top_left_side_bar)
        pw_side_bar.paneconfigure(top_left_side_bar, minsize = 175)

        bottom_left_side_bar = Frame(pw_side_bar, bg = self.main_color)

        ## SHOTS LIST ##
        shot_label = Label(bottom_left_side_bar, text = "Shots", bg = self.main_color, fg = self.text_color, font = "Helvetica 10 bold")
        shot_label.pack(fill = X, pady = 10)

        self.shot_list = Listbox(bottom_left_side_bar, bg = self.list_color, selectbackground = self.second_color, bd = 0, highlightthickness = 0, width = 30, exportselection = False)
        self.shot_list.pack(fill = BOTH, expand = Y)
        self.shot_list.bind("<<ListboxSelect>>", self.shotlistCommand)

        self.shots_preview_button = Button(bottom_left_side_bar, text = "Shots preview", state = DISABLED, bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 12, height = 1, command = self.shotsPreviewCommand)
        self.shots_preview_button.pack(pady = 10)

        self.custom_button = Button(bottom_left_side_bar, text = "Custom link", state = DISABLED, bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 12, height = 1, command = self.customButtonCommand)
        self.custom_button.pack(pady = 10)

        pw_side_bar.add(bottom_left_side_bar)
        pw_side_bar.paneconfigure(bottom_left_side_bar, minsize = 300)

        ###############################################################################################################

        main_area = Frame(pw_main, bg = self.main_color)

        main_area.columnconfigure(0, weight = 1)

         ## // SHOTS MAIN FRAME \\ ##
        self.main_area_shot = Frame(main_area, bg = self.main_color, bd = 0)
        self.main_area_shot.grid(row = 0, column = 0, sticky = N + S + W + E)
        self.main_area_shot.pi = self.main_area_shot.grid_info()

        self.main_area_shot.columnconfigure(0, pad = 10, minsize = 40)
        self.main_area_shot.columnconfigure(1, pad = 10)
        self.main_area_shot.columnconfigure(2, pad = 10, minsize = 50)
        self.main_area_shot.columnconfigure(3, pad = 10)
        self.main_area_shot.columnconfigure(4, pad = 10)
        self.main_area_shot.columnconfigure(5, pad = 10, weight = 2)
        self.main_area_shot.columnconfigure(6, pad = 10)

        self.main_area_shot.rowconfigure(0, pad = 20, minsize = 75)
        self.main_area_shot.rowconfigure(1, pad = 5, minsize = 75)
        self.main_area_shot.rowconfigure(2, pad = 5, minsize = 410)
        self.main_area_shot.rowconfigure(3, pad = 5, minsize = 50)

        ## SHOT INFOS ##
        self.up_down_shot = Frame(self.main_area_shot, bg = self.main_color, bd = 0)
        self.up_down_shot.grid(row = 0, column = 0, sticky = N + S, pady = 10)
        self.up_down_shot.pi = self.up_down_shot.grid_info()

        self.up_down_shot.columnconfigure(0, pad = 0)

        self.up_down_shot.rowconfigure(0, pad = 0, weight = 1)
        self.up_down_shot.rowconfigure(1, pad = 0, weight = 1)

        self.up_button_img = PhotoImage(file = "img/arrow_up.gif")
        self.up_button = Button(self.up_down_shot, image = self.up_button_img, compound = "left", bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, command = self.moveShotDownCommand)
        self.up_button.grid(row = 0, column = 0, sticky = N)
        self.up_button.pi = self.up_button.grid_info()
        self.up_button.grid_forget()

        self.down_button_img = PhotoImage(file = "img/arrow_down.gif")
        self.down_button = Button(self.up_down_shot, image = self.down_button_img, compound = "left", bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, command = self.moveShotUpCommand)
        self.down_button.grid(row = 1, column = 0, sticky = S)
        self.down_button.pi = self.down_button.grid_info()
        self.down_button.grid_forget()

        self.var_shot_nb_label = StringVar()
        self.var_shot_nb_label.set("NO SHOT SELECTED")
        shot_nb_label = Label(self.main_area_shot, textvariable = self.var_shot_nb_label, bg = self.main_color, fg = self.text_color, height = 1, anchor = NW, font = "Helvetica 11 bold")
        shot_nb_label.grid(row = 0, column = 1)

        self.delete_shot_button_img = PhotoImage(file = "img/red_cross.gif")
        self.delete_shot_button = Button(self.main_area_shot, image = self.delete_shot_button_img, bg = self.main_color, activebackground = self.main_color, cursor = "hand2", fg = self.text_color, bd = 0, command = self.deleteShotCommand)
        self.delete_shot_button.grid(row = 0, column = 2)
        self.delete_shot_button.pi = self.delete_shot_button.grid_info()
        self.delete_shot_button.grid_forget()

        self.set_shot_button = Button(self.main_area_shot, text = "Set shot", bg = self.button_color1, activebackground = self.over_button_color1, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 8, height = 1, command = self.setShotCommand)
        self.set_shot_button.grid(row = 0, column = 3)
        self.set_shot_button.pi = self.set_shot_button.grid_info()
        self.set_shot_button.grid_forget()

        self.var_frame_range = StringVar()

        self.frame_range_entry = Entry(self.main_area_shot, relief = FLAT, bg = self.button_color2, bd = 5, width = 6, justify = CENTER, validate="key", validatecommand = (self.register(self.validateFrameRangeEntry), '%P', '%S'))
        self.frame_range_entry.grid(row = 0, column = 3)
        self.frame_range_entry.pi = self.frame_range_entry.grid_info()
        self.frame_range_entry.grid_forget()

        self.set_shot_frame_range_button = Button(self.main_area_shot, text = "Set frame range", bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 13, height = 1, command = self.setShotFrameRangeCommand)
        self.set_shot_frame_range_button.grid(row = 0, column = 4)
        self.set_shot_frame_range_button.pi = self.set_shot_frame_range_button.grid_info()
        self.set_shot_frame_range_button.grid_forget()

        self.open_shot_folder_button = Button(self.main_area_shot, text = "Open shot folder", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 16, height = 1, command = self.openFolderCommand)
        self.open_shot_folder_button.grid(row = 0, column = 5)
        self.open_shot_folder_button.pi = self.open_shot_folder_button.grid_info()
        self.open_shot_folder_button.grid_forget()

        self.var_check_show_last = IntVar()
        shot_show_last_only_button = Checkbutton(self.main_area_shot, text = "Show only last versions", variable = self.var_check_show_last, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleLastVersions)
        shot_show_last_only_button.grid(row = 0, column = 6, sticky = E)

        ## SHOT STATE ##
        self.shot_state_line = Frame(self.main_area_shot, bg = self.main_color, bd = 0)
        self.shot_state_line.grid(row = 1, column = 0, columnspan = 7, sticky = W + E, pady = 10)

        self.shot_state_line.columnconfigure(0, pad = 10, minsize = 75)
        self.shot_state_line.columnconfigure(1, pad = 10, minsize = 100)
        self.shot_state_line.columnconfigure(2, pad = 50)
        self.shot_state_line.columnconfigure(7, pad = 50)

        self.priority_shot_label = Label(self.shot_state_line, text = "Priority : ", bg = self.main_color, fg = self.text_color, height = 1, anchor = NW, font = "Helvetica 9 bold")
        self.priority_shot_label.grid(row = 0, column = 0, sticky = E)
        self.priority_shot_label.pi = self.priority_shot_label.grid_info()
        self.priority_shot_label.grid_forget()

        self.var_shot_priority = StringVar(self.shot_state_line)
        self.var_shot_priority.set("Low")

        self.priority_shot_menu = OptionMenu(self.shot_state_line, self.var_shot_priority, "Low", "Medium", "High", "Urgent", command = self.priorityShotCommand)
        self.priority_shot_menu.config(bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, bd = 0, width = 10, highlightthickness = 0)
        self.priority_shot_menu.grid(row = 0, column = 1, sticky = W)
        self.priority_shot_menu.pi = self.priority_shot_menu.grid_info()
        self.priority_shot_menu.grid_forget()

        self.downgrade_shot_button = Button(self.shot_state_line, text = "Downgrade shot", state = DISABLED, bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 14, height = 1, command = self.downgradeShotCommand)
        self.downgrade_shot_button.grid(row = 0, column = 2)
        self.downgrade_shot_button.pi = self.downgrade_shot_button.grid_info()
        self.downgrade_shot_button.grid_forget()

        self.layout_label = Label(self.shot_state_line, text = "Layout", bg = "#66CEFF", height = 1, anchor = NW, font = "Helvetica 9 bold", pady = 5, padx = 15)
        self.layout_label.grid(row = 0, column = 3)
        self.layout_label.pi = self.layout_label.grid_info()
        self.layout_label.grid_forget()
        
        self.blocking_label = Label(self.shot_state_line, text = "Blocking", bg = "#999999", height = 1, anchor = NW, font = "Helvetica 9 bold", pady = 5, padx = 15)
        self.blocking_label.grid(row = 0, column = 4)
        self.blocking_label.pi = self.blocking_label.grid_info()
        self.blocking_label.grid_forget()
        
        self.splining_label = Label(self.shot_state_line, text = "Splining", bg = "#999999", height = 1, anchor = NW, font = "Helvetica 9 bold", pady = 5, padx = 15)
        self.splining_label.grid(row = 0, column = 5)
        self.splining_label.pi = self.splining_label.grid_info()
        self.splining_label.grid_forget()

        self.rendering_label = Label(self.shot_state_line, text = "Rendering", bg = "#999999", height = 1, anchor = NW, font = "Helvetica 9 bold", pady = 5, padx = 15)
        self.rendering_label.grid(row = 0, column = 6)
        self.rendering_label.pi = self.rendering_label.grid_info()
        self.rendering_label.grid_forget()

        self.upgrade_shot_button = Button(self.shot_state_line, text = "Upgrade shot", bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 13, height = 1, command = self.upgradeShotCommand)
        self.upgrade_shot_button.grid(row = 0, column = 7)
        self.upgrade_shot_button.pi = self.upgrade_shot_button.grid_info()
        self.upgrade_shot_button.grid_forget()

        self.var_shot_done = IntVar()
        self.done_shot_button = Checkbutton(self.shot_state_line, text = "Shot done", variable = self.var_shot_done, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleShotDone)
        self.done_shot_button.grid(row = 0, column = 8)
        self.done_shot_button.pi = self.done_shot_button.grid_info()
        self.done_shot_button.grid_forget()

        ## PICTURES ##
        self.pictures_shot = Frame(self.main_area_shot, bg = self.second_color, bd = 0)
        self.pictures_shot.grid(row = 2, column = 0, columnspan = 7, sticky = N + S + W + E, pady = 20)

        self.pictures_shot.columnconfigure(0, weight = 1, minsize = 550)
        self.pictures_shot.columnconfigure(1, weight = 1, minsize = 550)

        self.prev_pict_label = Label(self.pictures_shot, text = "Previous shot", bg = self.second_color, fg = self.text_color, height = 1, anchor = N, font = "Helvetica 11")
        self.prev_pict_label.grid(row = 0, column = 0, pady = 10)
        self.prev_pict_label.pi = self.prev_pict_label.grid_info()

        self.shot_prev_pict_caneva = Canvas(self.pictures_shot, bg = self.second_color, bd = 0, highlightthickness = 0)
        self.shot_prev_pict_caneva.grid(row = 1, column = 0, pady = 20)
        self.shot_prev_pict_caneva.pi = self.shot_prev_pict_caneva.grid_info()
        self.shot_prev_pict_caneva.grid_forget()
        self.shot_prev_gifdict = {}

        this_pict_label = Label(self.pictures_shot, text = "This shot", bg = self.second_color, fg = self.text_color, height = 1, anchor = N, font = "Helvetica 11")
        this_pict_label.grid(row = 0, column = 1, pady = 10)

        self.shot_pict_caneva = Canvas(self.pictures_shot, bg = self.second_color, bd = 0, highlightthickness = 0)
        self.shot_pict_caneva.grid(row = 1, column = 1, pady = 20)
        self.shot_pict_caneva.pi = self.shot_pict_caneva.grid_info()
        self.shot_pict_caneva.grid_forget()
        self.shot_gifdict = {}

        ## SHOT VERSION ACTIONS ##
        self.shot_actions_line = Frame(self.main_area_shot, bg = self.main_color, bd = 0)
        self.shot_actions_line.grid(row = 3, column = 0, columnspan = 7, sticky = W + E, pady = 10)

        self.shot_actions_line.columnconfigure(0, pad = 10)
        self.shot_actions_line.columnconfigure(1, pad = 10, weight = 1)
        self.shot_actions_line.columnconfigure(2, pad = 10)

        self.open_shot_layout_button = Button(self.shot_actions_line, text = "Open selected version ", bg = self.button_color1, activebackground = self.over_button_color1, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 19, height = 1, command = self.openShotCommand)
        self.open_shot_layout_button.grid(row = 0, column = 1, sticky = N)
        self.open_shot_layout_button.pi = self.open_shot_layout_button.grid_info()
        self.open_shot_layout_button.grid_forget()

        ## SHOT VERSION INFOS ##
        self.shot_version_management_line = Frame(self.main_area_shot, bg = self.second_color, bd = 0)
        self.shot_version_management_line.grid(row = 4, column = 0, columnspan = 7, sticky = W + E, pady = 10)

        self.shot_version_management_line.columnconfigure(0, pad = 10)
        self.shot_version_management_line.columnconfigure(1, pad = 10, weight = 1)
        self.shot_version_management_line.columnconfigure(2, pad = 10)

        shot_version_comment_label = Label(self.shot_version_management_line, text = "Version comment :", bg = self.second_color, fg = self.text_color, height = 1, pady = 10, anchor = NW, font = "Helvetica 9 bold")
        shot_version_comment_label.grid(row = 0, column = 1)

        self.var_shot_version_comment = StringVar()
        self.var_shot_version_comment.set("No comment")
        shot_version_comment = Message(self.shot_version_management_line, textvariable = self.var_shot_version_comment, bg = self.second_color, fg = self.text_color, pady = 10, width = 750)
        shot_version_comment.grid(row = 1, column = 1, sticky = N)

        ## PATHS ##
        self.shot_paths_line = Frame(self.main_area_shot, bg = self.main_color, bd = 0)
        self.shot_paths_line.grid(row = 5, column = 0, columnspan = 7, sticky = W + E, pady = 10, padx = 20)

        self.shot_paths_line.columnconfigure(0, pad = 10, weight = 1)

        maya_file_path_label = Label()

        self.var_selection_path_label = StringVar()
        shot_path_label = Entry(self.shot_paths_line, textvariable = self.var_selection_path_label, relief = FLAT, state = "readonly", readonlybackground = self.main_color, fg = self.text_color)
        shot_path_label.grid(row = 0, column = 0, sticky = W + E, pady = [0, 5])

        self.var_selection_abc_path_label = StringVar()
        shot_abc_path_label = Entry(self.shot_paths_line, textvariable = self.var_selection_abc_path_label, relief = FLAT, state = "readonly", readonlybackground = self.main_color, fg = self.text_color)
        shot_abc_path_label.grid(row = 1, column = 0, sticky = W + E, pady = 5)

        ###############################################################################################################

        ## // ASSETS MAIN FRAME \\ ##
        self.main_area_asset = Frame(main_area, bg = self.main_color, bd = 0)
        self.main_area_asset.grid(row = 0, column = 0, sticky = N + S + W + E)
        self.main_area_asset.pi = self.main_area_asset.grid_info()
        self.main_area_asset.grid_forget()

        self.main_area_asset.columnconfigure(0, pad = 10, minsize = 40)
        self.main_area_asset.columnconfigure(1, pad = 10)
        self.main_area_asset.columnconfigure(2, pad = 10, minsize = 50)
        self.main_area_asset.columnconfigure(3, pad = 10)
        self.main_area_asset.columnconfigure(4, pad = 10)
        self.main_area_asset.columnconfigure(5, pad = 10, weight = 2)
        self.main_area_asset.columnconfigure(6, pad = 10)

        self.main_area_asset.rowconfigure(0, pad = 20, minsize = 75)
        self.main_area_asset.rowconfigure(1, pad = 5, minsize = 75)
        self.main_area_asset.rowconfigure(2, pad = 5, minsize = 410)
        self.main_area_asset.rowconfigure(3, pad = 5, minsize = 50)

        self.var_asset_label = StringVar()
        self.var_asset_label.set("NO ASSET SELECTED")
        shot_nb_label = Label(self.main_area_asset, textvariable = self.var_asset_label, bg = self.main_color, fg = self.text_color, height = 1, anchor = NW, font = "Helvetica 11 bold")
        shot_nb_label.grid(row = 0, column = 1)

        self.delete_asset_button_img = PhotoImage(file = "img/red_cross.gif")
        self.delete_asset_button = Button(self.main_area_asset, image = self.delete_asset_button_img, bg = self.main_color, activebackground = self.main_color, fg = self.text_color, cursor = "hand2", bd = 0, command = self.deleteAssetCommand)
        self.delete_asset_button.grid(row = 0, column = 2)
        self.delete_asset_button.pi = self.delete_asset_button.grid_info()
        self.delete_asset_button.grid_forget()

        self.rename_asset_button = Button(self.main_area_asset, text = "Rename asset", bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 12, height = 1, command = self.renameAssetCommand)
        self.rename_asset_button.grid(row = 0, column = 3)
        self.rename_asset_button.pi = self.rename_asset_button.grid_info()
        self.rename_asset_button.grid_forget()

        self.set_asset_button = Button(self.main_area_asset, text = "Set asset", bg = self.button_color1, activebackground = self.over_button_color1, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 8, height = 1, command = self.setAssetCommand)
        self.set_asset_button.grid(row = 0, column = 4)
        self.set_asset_button.pi = self.set_asset_button.grid_info()
        self.set_asset_button.grid_forget()

        self.open_asset_folder_button = Button(self.main_area_asset, text = "Open asset folder", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 16, height = 1, command = self.openFolderCommand)
        self.open_asset_folder_button.grid(row = 0, column = 5)
        self.open_asset_folder_button.pi = self.open_asset_folder_button.grid_info()
        self.open_asset_folder_button.grid_forget()

        asset_show_last_only_button = Checkbutton(self.main_area_asset, text = "Show only last versions", variable = self.var_check_show_last, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleLastVersions)
        asset_show_last_only_button.grid(row = 0, column = 6, sticky = E)

        ## ASSET STATE ##
        self.asset_state_line = Frame(self.main_area_asset, bg = self.main_color, bd = 0)
        self.asset_state_line.grid(row = 1, column = 0, columnspan = 7, sticky = W + E, pady = 10)

        self.asset_state_line.columnconfigure(0, pad = 10, minsize = 75)
        self.asset_state_line.columnconfigure(1, pad = 10, minsize = 100)
        self.asset_state_line.columnconfigure(2, pad = 10)

        self.priority_asset_label = Label(self.asset_state_line, text = "Priority : ", bg = self.main_color, fg = self.text_color, height = 1, anchor = NW, font = "Helvetica 9 bold")
        self.priority_asset_label.grid(row = 0, column = 0, sticky = E)
        self.priority_asset_label.pi = self.priority_asset_label.grid_info()
        self.priority_asset_label.grid_forget()

        self.var_asset_priority = StringVar(self.asset_state_line)
        self.var_asset_priority.set("Low")

        self.priority_asset_menu = OptionMenu(self.asset_state_line, self.var_asset_priority, "Low", "Medium", "High", "Urgent", command = self.priorityAssetCommand)
        self.priority_asset_menu.config(bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, bd = 0, width = 10, highlightthickness = 0)
        self.priority_asset_menu.grid(row = 0, column = 1, sticky = W)
        self.priority_asset_menu.pi = self.priority_asset_menu.grid_info()
        self.priority_asset_menu.grid_forget()

        self.var_asset_modeling_done = IntVar()
        self.modeling_done_asset_button = Checkbutton(self.asset_state_line, text = "Modeling done", variable = self.var_asset_modeling_done, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleAssetModelingDone)
        self.modeling_done_asset_button.grid(row = 0, column = 2)
        self.modeling_done_asset_button.pi = self.modeling_done_asset_button.grid_info()
        self.modeling_done_asset_button.grid_forget()

        self.var_asset_rig_done = IntVar()
        self.rig_done_asset_button = Checkbutton(self.asset_state_line, text = "Rig done", variable = self.var_asset_rig_done, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleAssetRigDone)
        self.rig_done_asset_button.grid(row = 0, column = 3)
        self.rig_done_asset_button.pi = self.rig_done_asset_button.grid_info()
        self.rig_done_asset_button.grid_forget()

        self.var_asset_lookdev_done = IntVar()
        self.lookdev_done_asset_button = Checkbutton(self.asset_state_line, text = "Lookdev done", variable = self.var_asset_lookdev_done, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleAssetLookdevDone)
        self.lookdev_done_asset_button.grid(row = 0, column = 4)
        self.lookdev_done_asset_button.pi = self.lookdev_done_asset_button.grid_info()
        self.lookdev_done_asset_button.grid_forget()

        self.var_asset_done = IntVar()
        self.done_asset_button = Checkbutton(self.asset_state_line, text = "Asset done", variable = self.var_asset_done, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleAssetDone)
        self.done_asset_button.grid(row = 0, column = 5)
        self.done_asset_button.pi = self.done_asset_button.grid_info()
        self.done_asset_button.grid_forget()

        ## PICTURES ##
        pictures_asset = Frame(self.main_area_asset, bg = self.second_color, bd = 0)
        pictures_asset.grid(row = 2, column = 0, columnspan = 7, sticky = N + S + W + E, pady = 20)

        pictures_asset.columnconfigure(0, weight = 1, minsize = 550)

        pict_label = Label(pictures_asset, text = "This asset", bg = self.second_color, fg = self.text_color, height = 1, anchor = N, font = "Helvetica 11")
        pict_label.grid(row = 0, column = 0, pady = 10)

        self.asset_pict_caneva = Canvas(pictures_asset, bg = self.second_color, bd = 0, highlightthickness = 0)
        self.asset_pict_caneva.grid(row = 1, column = 0, pady = 20)
        self.asset_pict_caneva.pi = self.asset_pict_caneva.grid_info()
        self.asset_pict_caneva.grid_forget()
        self.asset_gifdict = {}

        ## ASSET VERSION ACTIONS ##
        self.asset_actions_line = Frame(self.main_area_asset, bg = self.main_color, bd = 0)
        self.asset_actions_line.grid(row = 3, column = 0, columnspan = 7, sticky = W + E, pady = 10)

        self.asset_actions_line.columnconfigure(0, pad = 10)
        self.asset_actions_line.columnconfigure(1, pad = 10, weight = 1)
        self.asset_actions_line.columnconfigure(2, pad = 10)

        self.open_asset_button = Button(self.asset_actions_line, text = "Open selected version", bg = self.button_color1, activebackground = self.over_button_color1, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 19, height = 1, command = self.openAssetCommand)
        self.open_asset_button.grid(row = 0, column = 1, sticky = N)
        self.open_asset_button.pi = self.open_asset_button.grid_info()
        self.open_asset_button.grid_forget()

        ## ASSET VERSION INFOS ##
        self.asset_version_management_line = Frame(self.main_area_asset, bg = self.second_color, bd = 0)
        self.asset_version_management_line.grid(row = 4, column = 0, columnspan = 7, sticky = W + E, pady = 10)

        self.asset_version_management_line.columnconfigure(0, pad = 10)
        self.asset_version_management_line.columnconfigure(1, pad = 10, weight = 1)
        self.asset_version_management_line.columnconfigure(2, pad = 10)

        shot_version_comment_label = Label(self.asset_version_management_line, text = "Version comment :", bg = self.second_color, fg = self.text_color, height = 1, pady = 10, anchor = NW, font = "Helvetica 9 bold")
        shot_version_comment_label.grid(row = 0, column = 1)

        self.var_asset_version_comment_label = StringVar()
        self.var_asset_version_comment_label.set("No comment")
        asset_version_comment_label = Message(self.asset_version_management_line, textvariable = self.var_asset_version_comment_label, bg = self.second_color, fg = self.text_color, pady = 10, width = 750)
        asset_version_comment_label.grid(row = 1, column = 1, sticky = N)

        ## PATHS ##
        self.asset_paths_line = Frame(self.main_area_asset, bg = self.main_color, bd = 0)
        self.asset_paths_line.grid(row = 5, column = 0, columnspan = 7, sticky = W + E, pady = 10, padx = 20)

        self.asset_paths_line.columnconfigure(0, pad = 10, weight = 1)

        maya_file_path_label = Label()

        asset_path_label = Entry(self.asset_paths_line, textvariable = self.var_selection_path_label, relief = FLAT, state = "readonly", readonlybackground = self.main_color, fg = self.text_color)
        asset_path_label.grid(row = 0, column = 0, sticky = W + E)

        ###############################################################################################################

        ## SHOTS PREVIEW ##
        self.main_area_preview = Frame(main_area, bg = self.main_color, bd = 0, width = 100, height = 100)
        self.main_area_preview.grid(row = 0, column = 0, sticky = N + W + E)
        self.main_area_preview.pi = self.main_area_preview.grid_info()
        self.main_area_preview.grid_forget()

        self.preview_canva_scroll = Canvas(self.main_area_preview, bg = self.main_color, bd = 0, highlightthickness = 0, yscrollincrement = 20)

        self.shots_preview_list = Frame(self.preview_canva_scroll, bg = self.main_color, bd = 0, width = 1000, height = 300)
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

        pw_main.add(main_area)
        pw_main.paneconfigure(main_area, minsize = 1100)

        ###############################################################################################################

        right_side_bar = Frame(pw_main, bg = self.main_color)

        ## VERSIONS ##
        versions_label = Label(right_side_bar, text = "Versions", bg = self.main_color, fg = self.text_color, font = "Helvetica 10 bold")
        versions_label.pack(fill = X, pady = 10)

        self.version_list = Listbox(right_side_bar, bg = self.list_color, selectbackground = self.second_color, bd = 0, highlightthickness = 0, width = 50, height = 70, exportselection = False)
        self.version_list.pack(fill = X, pady = 10)
        self.version_list.bind("<<ListboxSelect>>", self.versionlistCommand)

        pw_main.add(right_side_bar)
        pw_main.update()
        pw_main.sash_place(1, 1650, 0)

    def newProjectCommand(self):
        self.current_sequence = 1

        directory = {"dir":""}

        dialog = lambda: NewProjectDialog.NewProjectDialog(self.parent, (directory, "dir"))
        self.wait_window(dialog().top)

        if directory["dir"]:
            self.current_project = Project(directory["dir"])
            self.current_sequence = self.current_project.getCurrentSequence()

            Resources.writeAtLine("save/options.spi", directory["dir"], 3)

            self.add_shot_button.config(state = NORMAL)
            self.add_asset_button.config(state = NORMAL)
            self.shots_preview_button.config(state = NORMAL)
            self.custom_button.config(state = NORMAL)

            self.parent.title("Super Pipe || " + self.current_project.getDirectory())

            self.asset_list.configure(selectmode = "browse")

            self.updateShotListView()
            self.updateAssetListView()

    def setProjectCommand(self):
        directory = filedialog.askdirectory(title = "New project", mustexist  = False)

        self.parent.config(cursor = "wait")
        self.parent.update()

        if directory:
            if path.isdir(directory):
                self.current_project = Project(directory)

                if self.current_project.isValid():

                    Resources.writeAtLine("save/options.spi", directory, 3)

                    self.current_sequence = self.current_project.getCurrentSequence()

                    self.add_shot_button.config(state = NORMAL)
                    self.add_asset_button.config(state = NORMAL)
                    self.shots_preview_button.config(state = NORMAL)
                    self.custom_button.config(state = NORMAL)

                    self.parent.title("Super Pipe || " + self.current_project.getDirectory())

                    self.asset_list.configure(selectmode = "browse")

                    self.updateShotListView()
                    self.updateAssetListView()
                else:
                    dialog = lambda: OkDialog.OkDialog(self.parent, "Set project", "\"" + directory + "\" is not a project folder")
                    self.wait_window(dialog().top)
            else:
                dialog = lambda: OkDialog.OkDialog(self.parent, "Set project", "\"" + directory + "\" is not a project folder")
                self.wait_window(dialog().top)

        self.parent.config(cursor = "")

    def updateProjectCommand(self):
        directory = filedialog.askdirectory(title = "New project", mustexist  = False)

        self.parent.config(cursor = "wait")
        self.parent.update()

        if directory:
            if path.isdir(directory):
                for cat in listdir(directory + "/04_asset/"):
                    for asset in listdir(directory + "/04_asset/" + cat):
                        if asset != "backup":
                            if not path.isdir(directory + "/04_asset/" + cat + "/" + asset + "/superpipe"):
                                print(directory + "/04_asset/" + cat + "/" + asset + "/data")
                                rename(directory + "/04_asset/" + cat + "/" + asset + "/data", directory + "/04_asset/" + cat + "/" + asset + "/superpipe")
                                mkdir(directory + "/04_asset/" + cat + "/" + asset + "/data")

                for shot in listdir(directory + "/05_shot/"):
                    if shot != "backup":
                        if not path.isdir(directory + "/05_shot/" + shot + "/superpipe"):
                            print(directory + "/05_shot/" + shot + "/data")
                            rename(directory + "/05_shot/" + shot + "/data", directory + "/05_shot/" + shot + "/superpipe")
                            mkdir(directory + "/05_shot/" + shot + "/data")

        self.parent.config(cursor = "")

    def setShotCommand(self):
        selected_line = self.shot_list.curselection()[0]
        selected_shot = self.shot_list.get(selected_line)

        shot = self.current_project.getSelection()
        shot.setShot(self.current_project.getResolution())

        self.set_shot_button.grid_forget()
        self.frame_range_entry.grid(self.frame_range_entry.pi)
        self.set_shot_frame_range_button.grid(self.set_shot_frame_range_button.pi)
        self.open_shot_layout_button.grid(self.open_shot_layout_button.pi)

        self.downgrade_shot_button.grid(self.downgrade_shot_button.pi)

        self.layout_label.grid(self.layout_label.pi)
        self.blocking_label.grid(self.blocking_label.pi)
        self.splining_label.grid(self.splining_label.pi)
        self.rendering_label.grid(self.rendering_label.pi)

        self.upgrade_shot_button.grid(self.upgrade_shot_button.pi)
        self.done_shot_button.grid(self.done_shot_button.pi)

        self.updateVersionListView(shot = shot)
        self.version_list.select_set(0)

        selected_line = self.version_list.curselection()[0]
        self.var_selection_path_label.set(self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.get(selected_line))

        self.frame_range_entry.delete(0, len(self.frame_range_entry.get()))
        self.frame_range_entry.insert(0, self.current_project.getSelection().getFrameRange())

        self.versionlistCommand(None)

    def setAssetCommand(self):
        selected_asset = self.asset_list.focus()

        asset = self.current_project.getSelection()
        asset.setAsset()

        self.set_asset_button.grid_forget()
        self.open_asset_button.grid(self.open_asset_button.pi)
        self.open_asset_folder_button.grid(self.open_asset_folder_button.pi)
        self.modeling_done_asset_button.grid(self.modeling_done_asset_button.pi)
        self.rig_done_asset_button.grid(self.rig_done_asset_button.pi)
        self.lookdev_done_asset_button.grid(self.lookdev_done_asset_button.pi)
        self.done_asset_button.grid(self.done_asset_button.pi)

        self.updateVersionListView(asset = asset)
        self.version_list.select_set(0)

        self.versionlistCommand(None)

    def deleteShotCommand(self):
        selected_line = self.shot_list.curselection()[0]
        selected_shot = self.shot_list.get(selected_line)

        yesno = {"result" : ""}

        dialog = lambda: YesNoDialog.YesNoDialog(self.parent, "Delete shot", "Delete shot \"" + selected_shot + "\" ?", (yesno, "result"))
        self.wait_window(dialog().top)

        if yesno["result"] == "yes":
            self.current_project.removeShot(selected_shot)

            self.updateShotListView()

            self.clearMainFrame("shot")

            self.updateVersionListView()

    def deleteAssetCommand(self):
        selected_asset = self.asset_list.focus()

        yesno = {"result" : ""}

        dialog = lambda: YesNoDialog.YesNoDialog(self.parent, "Delete asset", "Delete asset \"" + selected_asset + "\" from \"" + self.asset_list.parent(selected_asset).upper() + "\" category ?", (yesno, "result"))
        self.wait_window(dialog().top)

        if yesno["result"] == "yes":
            cur_item = selected_asset
            path_array = []

            is_parent = True

            while is_parent:
                if self.asset_list.parent(cur_item):
                    cur_item = self.asset_list.parent(cur_item)
                    path_array.insert(0, cur_item)
                else:
                    is_parent = False

            self.current_project.removeAsset(selected_asset, "/" + "/".join(path_array))

            self.updateAssetListView()

            self.clearMainFrame("asset")

            self.updateVersionListView()

    def addShotCommand(self):
        sequence = {"seq": -1}

        dialog = lambda: NewShotDialog.NewShotDialog(self.parent, (sequence, "seq"))
        self.wait_window(dialog().top)

        if sequence["seq"] >= 0:
            self.current_sequence += sequence["seq"]
            self.current_project.createShot(self.current_sequence)
            self.updateShotListView()
            self.shot_list.select_set(END)
            self.shotlistCommand(None)

    def addAssetCommand(self):
        asset = {"cat": None, "name" : None, "software" : None}

        dialog = lambda: NewAssetDialog.NewAssetDialog(self.parent, (asset, "cat", "name", "software"))
        self.wait_window(dialog().top)

        if asset["cat"] and asset["name"] and asset["software"]:
            if self.current_project.createAsset(asset["name"], "/" + Resources.getCategoryName(asset["cat"]), Resources.getSoftwareName(asset["software"])):
                self.updateAssetListView()

                self.asset_list.item(Resources.getCategoryName(asset["cat"]), open = True)

                self.asset_list.selection_set(asset["name"])
                self.asset_list.focus_set()
                self.asset_list.focus(asset["name"])
                self.assetListCommand(None)
            else:
                dialog = lambda: OkDialog.OkDialog(self.parent, "Asset already exists", "The asset \"" + asset["name"] + "\" already exists")
                self.wait_window(dialog().top)

    def shotlistCommand(self, e):
        if self.shot_list.size() != 0:
            selected_line = self.shot_list.curselection()[0]
            selected_shot = self.shot_list.get(selected_line)
            self.var_shot_nb_label.set(selected_shot.replace("s", "SEQUENCE ").replace("p", " SHOT "))

            if selected_line == 0 and selected_line == self.shot_list.size() - 1:
                self.prev_pict_label.grid(self.prev_pict_label.pi)
                self.shot_prev_pict_caneva.grid(self.shot_prev_pict_caneva.pi)
                self.up_button.grid_forget()
                self.down_button.grid_forget()
            elif selected_line == 0:
                self.prev_pict_label.grid_forget()
                self.shot_prev_pict_caneva.grid_forget()
                self.up_button.grid_forget()
                self.down_button.grid(self.down_button.pi)
            elif selected_line == self.shot_list.size() - 1:
                self.prev_pict_label.grid(self.prev_pict_label.pi)
                self.shot_prev_pict_caneva.grid(self.shot_prev_pict_caneva.pi)
                self.down_button.grid_forget()
                self.up_button.grid(self.up_button.pi)
            else:
                self.prev_pict_label.grid(self.prev_pict_label.pi)
                self.shot_prev_pict_caneva.grid(self.shot_prev_pict_caneva.pi)
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

            self.var_shot_done.set(int(Resources.readLine(shot.getDirectory() + "/superpipe/shot_data.spi", 1)))
            self.var_shot_priority.set(Resources.readLine(shot.getDirectory() + "/superpipe/shot_data.spi", 2))

            self.priority_shot_label.grid(self.priority_shot_label.pi)
            self.priority_shot_menu.grid(self.priority_shot_menu.pi)
            self.open_shot_folder_button.grid(self.open_shot_folder_button.pi)

            if shot.isSet():
                self.set_shot_button.grid_forget()
                self.frame_range_entry.grid(self.frame_range_entry.pi)
                self.set_shot_frame_range_button.grid(self.set_shot_frame_range_button.pi)
                self.open_shot_layout_button.grid(self.open_shot_layout_button.pi)

                self.downgrade_shot_button.grid(self.downgrade_shot_button.pi)

                self.layout_label.grid(self.layout_label.pi)
                self.blocking_label.grid(self.blocking_label.pi)
                self.splining_label.grid(self.splining_label.pi)
                self.rendering_label.grid(self.rendering_label.pi)

                self.upgrade_shot_button.grid(self.upgrade_shot_button.pi)
                self.done_shot_button.grid(self.done_shot_button.pi)

                self.frame_range_entry.delete(0, len(self.frame_range_entry.get()))
                self.frame_range_entry.insert(0, self.current_project.getSelection().getFrameRange())

                if shot.getStep() == "Layout":
                    self.blocking_label.config(bg = "#999999")
                    self.splining_label.config(bg = "#999999")
                    self.rendering_label.config(bg = "#999999")
                    self.upgrade_shot_button.config(state = NORMAL)
                    self.downgrade_shot_button.config(state = DISABLED)
                elif shot.getStep() == "Blocking":
                    self.blocking_label.config(bg = "#66CEFF")
                    self.splining_label.config(bg = "#999999")
                    self.rendering_label.config(bg = "#999999")
                    self.upgrade_shot_button.config(state = NORMAL)
                    self.downgrade_shot_button.config(state = NORMAL)
                elif shot.getStep() == "Splining":
                    self.blocking_label.config(bg = "#66CEFF")
                    self.splining_label.config(bg = "#66CEFF")
                    self.rendering_label.config(bg = "#999999")
                    self.upgrade_shot_button.config(state = NORMAL)
                    self.downgrade_shot_button.config(state = NORMAL)
                elif shot.getStep() == "Rendering":
                    self.blocking_label.config(bg = "#66CEFF")
                    self.splining_label.config(bg = "#66CEFF")
                    self.rendering_label.config(bg = "#66CEFF")
                    self.upgrade_shot_button.config(state = DISABLED)
                    self.downgrade_shot_button.config(state = NORMAL)

                pict_path = shot.getDirectory() + "/images/screenshots/" + self.version_list.get(self.version_list.curselection()[0]).strip(".ma") + ".gif"

                selected_line = self.version_list.curselection()[0]
                self.var_selection_path_label.set(self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.get(selected_line))

                if path.isfile(self.current_project.getSelection().getDirectory() + "/cache/alembic/" + self.version_list.get(selected_line).strip(".ma") + ".abc"):
                    self.var_selection_abc_path_label.set(self.current_project.getSelection().getDirectory() + "/cache/alembic/" + self.version_list.get(selected_line).strip(".ma") + ".abc")
                else:
                    self.var_selection_abc_path_label.set("")

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
                self.frame_range_entry.grid_forget()
                self.set_shot_frame_range_button.grid_forget()
                self.open_shot_layout_button.grid_forget()

                self.downgrade_shot_button.grid_forget()

                self.layout_label.grid_forget()
                self.blocking_label.grid_forget()
                self.splining_label.grid_forget()
                self.rendering_label.grid_forget()

                self.upgrade_shot_button.grid_forget()
                self.done_shot_button.grid_forget()

                self.shot_pict_caneva.grid_forget()

                self.var_selection_path_label.set("")
                self.var_selection_abc_path_label.set("")

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

            categories = ["character", "fx", "props", "set"]

            if not self.asset_list.get_children(self.asset_list.focus()) and not self.asset_list.focus() in categories:
                selected_asset = self.asset_list.focus()

                cur_item = selected_asset
                path_array = []

                is_parent = True

                while is_parent:
                    if self.asset_list.parent(cur_item):
                        cur_item = self.asset_list.parent(cur_item)
                        path_array.insert(0, cur_item)
                    else:
                        is_parent = False

                self.current_project.setSelection(asset_name = selected_asset, second_path = "/" + "/".join(path_array))
                asset = self.current_project.getSelection()

                self.var_asset_label.set("ASSET " + self.asset_list.focus().upper())
                self.delete_asset_button.grid(self.delete_asset_button.pi)
                self.rename_asset_button.grid(self.rename_asset_button.pi)

                self.priority_asset_label.grid(self.priority_asset_label.pi)
                self.priority_asset_menu.grid(self.priority_asset_menu.pi)

                self.updateVersionListView(asset = asset)
                self.version_list.select_set(0)

                self.var_asset_priority.set(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 1))
                self.var_asset_modeling_done.set(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 2)))
                self.var_asset_rig_done.set(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 3)))
                self.var_asset_lookdev_done.set(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 4)))
                self.var_asset_done.set(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 5)))

                if asset:
                    if asset.isSet():
                        self.set_asset_button.grid_forget()
                        self.open_asset_button.grid(self.open_asset_button.pi)
                        self.open_asset_folder_button.grid(self.open_asset_folder_button.pi)

                        selected_line = self.version_list.curselection()[0]
                        self.var_selection_path_label.set(self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.get(selected_line))

                        self.modeling_done_asset_button.grid(self.modeling_done_asset_button.pi)
                        self.rig_done_asset_button.grid(self.rig_done_asset_button.pi)
                        self.lookdev_done_asset_button.grid(self.lookdev_done_asset_button.pi)
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
                        self.open_asset_folder_button.grid_forget()
                        self.var_selection_path_label.set("")
                        self.asset_pict_caneva.grid_forget()
                        self.modeling_done_asset_button.grid_forget()
                        self.rig_done_asset_button.grid_forget()
                        self.lookdev_done_asset_button.grid_forget()
                        self.done_asset_button.grid_forget()

            else:
                self.var_asset_label.set("NO ASSET SELECTED")
                self.var_selection_path_label.set("")
                self.delete_asset_button.grid_forget()
                self.rename_asset_button.grid_forget()
                self.set_asset_button.grid_forget()
                self.open_asset_button.grid_forget()
                self.open_asset_folder_button.grid_forget()
                self.version_list.delete(0, END)
                self.asset_pict_caneva.grid_forget()
                self.priority_asset_label.grid_forget()
                self.priority_asset_menu.grid_forget()
                self.modeling_done_asset_button.grid_forget()
                self.rig_done_asset_button.grid_forget()
                self.lookdev_done_asset_button.grid_forget()
                self.done_asset_button.grid_forget()

    def versionlistCommand(self, e):
        if self.version_list.size() != 0:
            self.open_asset_button.grid(self.open_asset_button.pi)
            self.open_asset_folder_button.grid(self.open_asset_folder_button.pi)

            selected_line = self.version_list.curselection()[0]
            selected_version = self.version_list.get(selected_line)

            if path.isfile(self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version):
                self.var_selection_path_label.set(self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version)
            else:
                self.var_selection_path_label.set(self.current_project.getSelection().getDirectory() + "/scenes/edits/" + selected_version)

            pict_path = self.current_project.getSelection().getDirectory() + "/images/screenshots/" + selected_version.strip(".ma") + ".gif"

            if self.current_project.getSelectionType() == "shot":
                self.var_shot_version_comment.set(self.current_project.getSelection().getComment(selected_version))

                if path.isfile(pict_path):
                    pict = PhotoImage(file = pict_path)

                    self.shot_gifdict[pict_path] = pict

                    self.shot_pict_caneva.grid(self.shot_pict_caneva.pi)
                    self.shot_pict_caneva.create_image(0, 0, anchor = N + W, image = pict)
                    self.shot_pict_caneva.config(height = pict.height(), width = pict.width())
                else:
                    self.shot_pict_caneva.grid_forget()

            elif self.current_project.getSelectionType() == "asset":
                self.var_asset_version_comment_label.set(self.current_project.getSelection().getComment(selected_version))

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
            dialog = lambda: OkDialog.OkDialog(self.parent, "Maya path", "Check Maya path in Edit > Preferences")
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
            dialog = lambda: OkDialog.OkDialog(self.parent, "Maya path", "Check Maya path in Edit > Preferences")
            self.wait_window(dialog().top)

    def renameAssetCommand(self):
        asset_name = {"name" : None}

        dialog = lambda: RenameAssetDialog.RenameAssetDialog(self.parent, (asset_name, "name"))
        self.wait_window(dialog().top)

        if asset_name["name"]:
            self.parent.config(cursor = "wait")
            self.parent.update()

            asset = self.current_project.getSelection()
            if asset.renameAsset(asset_name["name"]):
                self.current_project.updateAssetList()
                self.updateAssetListView()

                self.asset_list.selection_set(asset_name["name"])
                self.asset_list.focus_set()
                self.asset_list.focus(asset_name["name"])
                self.assetListCommand(None)
            else:
                dialog = lambda: OkDialog.OkDialog(self.parent, "Error", "The asset \"" + asset_name["name"] + "\" already exists !")
                self.wait_window(dialog().top)
            
            self.parent.config(cursor = "")

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
            elif cur_shot.getPriority() == "High":
                self.shot_list.itemconfig(shot[0] - 1, bg = "#EFB462", selectbackground = "#997646")
            elif cur_shot.getPriority() == "Medium":
                self.shot_list.itemconfig(shot[0] - 1, bg = "#F4E255", selectbackground = "#9B9145")
            
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
                cur_asset = Asset(self.current_project.getDirectory(), asset[1], asset[0])

                asset_subfolders = asset[1].split("/")

                for i in range(len(asset_subfolders)):
                    if not self.asset_list.exists(asset_subfolders[i].lower()):
                        if i > 0:
                            self.asset_list.insert(asset_subfolders[i - 1].lower(), END, asset_subfolders[i].lower(), text = asset_subfolders[i].upper(), tags = ("folder"))

                if cur_asset.isDone():
                    self.asset_list.insert(asset_subfolders[-1].lower(), END, asset[0], text = asset[0], tags = ("done"))
                elif cur_asset.getPriority() == "Urgent":
                    self.asset_list.insert(asset_subfolders[-1].lower(), END, asset[0], text = asset[0], tags = ("urgent"))
                elif cur_asset.getPriority() == "High":
                    self.asset_list.insert(asset_subfolders[-1].lower(), END, asset[0], text = asset[0], tags = ("high"))
                elif cur_asset.getPriority() == "Medium":
                    self.asset_list.insert(asset_subfolders[-1].lower(), END, asset[0], text = asset[0], tags = ("medium"))
                else:
                    self.asset_list.insert(asset_subfolders[-1].lower(), END, asset[0], text = asset[0])

    def updateVersionListView(self, shot = None, asset = None):
        self.version_list.delete(0, END)

        if shot:
            shot_versions = shot.getVersionsList(self.var_check_show_last.get())

            if shot_versions:
                for shot_version in shot_versions:
                    self.version_list.insert(END, shot_version[1])

        elif asset:
            asset_versions = asset.getVersionsList(self.var_check_show_last.get())

            if asset_versions:
                for asset_version in asset_versions:
                    self.version_list.insert(END, asset_version[1])

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
        self.current_project.getSelection().setDone(self.var_shot_done.get())
        self.updateShotListView()
        self.shot_list.select_set(selected_shot)

    def toggleAssetModelingDone(self):
        selected_asset = self.asset_list.focus()
        self.current_project.getSelection().setModelingDone(self.var_asset_modeling_done.get())
        self.updateAssetListView()
        self.asset_list.selection_set(selected_asset)
        self.asset_list.focus_set()
        self.asset_list.focus(selected_asset)
        self.asset_list.see(selected_asset)

    def toggleAssetRigDone(self):
        selected_asset = self.asset_list.focus()
        self.current_project.getSelection().setRigDone(self.var_asset_rig_done.get())
        self.updateAssetListView()
        self.asset_list.selection_set(selected_asset)
        self.asset_list.focus_set()
        self.asset_list.focus(selected_asset)
        self.asset_list.see(selected_asset)

    def toggleAssetLookdevDone(self):
        selected_asset = self.asset_list.focus()
        self.current_project.getSelection().setLookdevDone(self.var_asset_lookdev_done.get())
        self.updateAssetListView()
        self.asset_list.selection_set(selected_asset)
        self.asset_list.focus_set()
        self.asset_list.focus(selected_asset)
        self.asset_list.see(selected_asset)

    def toggleAssetDone(self):
        selected_asset = self.asset_list.focus()
        self.current_project.getSelection().setDone(self.var_asset_done.get())
        self.updateAssetListView()
        self.asset_list.selection_set(selected_asset)
        self.asset_list.focus_set()
        self.asset_list.focus(selected_asset)
        self.asset_list.see(selected_asset)

    def priorityShotCommand(self, priority):
        selected_shot = self.shot_list.curselection()[0]
        self.current_project.getSelection().setPriority(priority)
        self.updateShotListView()
        self.shot_list.select_set(selected_shot)

    def priorityAssetCommand(self, priority):
        selected_asset = self.asset_list.focus()
        self.current_project.getSelection().setPriority(priority)
        self.updateAssetListView()
        self.asset_list.selection_set(selected_asset)
        self.asset_list.focus_set()
        self.asset_list.focus(selected_asset)

    def shotsPreviewCommand(self):
        self.parent.config(cursor = "wait")
        self.parent.update()

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
                    all_shots_preview.append([cur_shot.getShotNb(), cur_shot.getShotName(), max(all_picts_path_array, key = path.getmtime)])
                else:
                    all_shots_preview.append([cur_shot.getShotNb(), cur_shot.getShotName(), "img/img_not_available.gif"])

        for nb, name, img in all_shots_preview:
            shot_preview_caneva = Canvas(self.shots_preview_list, bg = self.second_color, bd = 0, highlightthickness = 0)

            pict = PhotoImage(file = img)

            self.preview_gifdict[nb] = pict

            shot_preview_label = Label(self.shots_preview_list, text = name, bg = self.main_color, fg = self.text_color)
            shot_preview_label.grid(row = int((nb - 1)/5) * 2, column = (nb - 1) % 5, pady = (10, 5))

            shot_preview_caneva.create_image(0, 0, anchor = N + W, image = pict)
            shot_preview_caneva.config(height = pict.height(), width = pict.width())

            shot_preview_caneva.grid(row = (int((nb - 1)/5) * 2) + 1, column = (nb - 1) % 5, pady = (0, 10))
            shot_preview_caneva.bind("<MouseWheel>", self.wheelScrollCommand)

        self.parent.config(cursor = "")

    def upgradeShotCommand(self):
        selected_shot = self.shot_list.curselection()[0]
        self.current_project.getSelection().upgrade()

        if self.current_project.getSelection().getStep() == "Layout":
            self.downgrade_shot_button.config(state = DISABLED)
        elif self.current_project.getSelection().getStep() == "Rendering":
            self.upgrade_shot_button.config(state = DISABLED)

        self.shotlistCommand(None)

    def downgradeShotCommand(self):
        yesno = {"result" : ""}

        dialog = lambda: YesNoDialog.YesNoDialog(self.parent, "Downgrade shot", "Are you sure you want to downgrade the shot \"" + self.current_project.getSelection().getShotName() + "\" ?", (yesno, "result"))
        self.wait_window(dialog().top)

        if yesno["result"] == "yes":
            selected_shot = self.shot_list.curselection()[0]
            self.current_project.getSelection().downgrade()

            if self.current_project.getSelection().getStep() == "Layout":
                self.downgrade_shot_button.config(state = DISABLED)
            elif self.current_project.getSelection().getStep() == "Rendering":
                self.upgrade_shot_button.config(state = DISABLED)

            self.shotlistCommand(None)

    def setShotFrameRangeCommand(self):
        self.current_project.getSelection().setFrameRange(int(self.frame_range_entry.get()))

    def openFolderCommand(self):
        subprocess.Popen("%s, \"%s\"" % ("explorer /root", self.current_project.getSelection().getDirectory().replace("/", "\\") + "\\"))

    ###############################################################################################################

    def validateFrameRangeEntry(self, P, S):
        valid = S.isnumeric() and len(P) < 6

        if not valid:
            self.bell()

        return valid

    def editCustomLinkCommand(self):
        if not path.isfile(self.current_project.getDirectory() + "/project_option.spi"):
            with open(self.current_project.getDirectory() + "/project_option.spi", "w") as f:
                f.write("www.google.fr\n")
            f.close()

        link = {"link" : None}

        dialog = lambda: EditCustomLinkDialog.EditCustomLinkDialog(self.parent, self.current_project.getDirectory() + "/project_option.spi", (link, "link"))
        self.wait_window(dialog().top)

        if link["link"]:
            Resources.writeAtLine(self.current_project.getDirectory() + "/project_option.spi", link["link"], 1)

    def customButtonCommand(self):
        if not path.isfile(self.current_project.getDirectory() + "/project_option.spi"):
            with open(self.current_project.getDirectory() + "/project_option.spi", "w") as f:
                f.write("www.google.fr\n")
            f.close()

        base_url = Resources.readLine(self.current_project.getDirectory() + "/project_option.spi", 1)

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
            self.open_shot_folder_button.grid_forget()
            self.priority_shot_menu.grid_forget()
            self.priority_shot_label.grid_forget()
            self.downgrade_shot_button.grid_forget()
            self.layout_label.grid_forget()
            self.blocking_label.grid_forget()
            self.splining_label.grid_forget()
            self.rendering_label.grid_forget()
            self.upgrade_shot_button.grid_forget()
            self.done_shot_button.grid_forget()
        elif type == "asset":
            self.var_asset_label.set("NO ASSET SELECTED")
            self.delete_asset_button.grid_forget()
            self.rename_asset_button.grid_forget()
            self.set_asset_button.grid_forget()
            self.var_selection_path_label.set("")
            self.asset_pict_caneva.grid_forget()
            self.open_asset_button.grid_forget()
            self.open_asset_folder_button.grid_forget()
            self.priority_asset_menu.grid_forget()
            self.priority_asset_label.grid_forget()
            self.modeling_done_asset_button.grid_forget()
            self.rig_done_asset_button.grid_forget()
            self.lookdev_done_asset_button.grid_forget()
            self.done_asset_button.grid_forget()

    def cleanBackupsCommand(self):
        settings = {"res" : ""}

        dialog = lambda: ManageBackupDialog.ManageBackupDialog(self.parent, self.current_project, (settings, "res"))
        self.wait_window(dialog().top)

        if settings["res"]:            
            self.current_project.setResolution(settings["res"])

    def cleanStudentCommand(self):
        self.parent.config(cursor = "wait")
        self.parent.update()

        yesno = {"result" : ""}

        dialog = lambda: YesNoDialog.YesNoDialog(self.parent, "Clean student versions", "Make all your files easy to save again ?", (yesno, "result"))
        self.wait_window(dialog().top)

        if yesno["result"] == "yes":
            self.current_project.removeAllStudentVersions()

        self.parent.config(cursor = "")

    def projectSettingsCommand(self):
        settings = {"res" : ""}

        dialog = lambda: ProjectSettingsDialog.ProjectSettingsDialog(self.parent, self.current_project, (settings, "res"))
        self.wait_window(dialog().top)

        if settings["res"]:            
            self.current_project.setResolution(settings["res"])

    def preferencesCommand(self):
        preferences = {"maya_path" : "", "nuke_path" : ""}

        dialog = lambda: PreferencesDialog.PreferencesDialog(self.parent, (preferences, "maya_path", "nuke_path"))
        self.wait_window(dialog().top)

        if preferences["maya_path"] and preferences["nuke_path"]:
            self.maya_path = preferences["maya_path"]
            self.nuke_path = preferences["nuke_path"]

            Resources.writeAtLine("save/options.spi", preferences["maya_path"], 1)
            Resources.writeAtLine("save/options.spi", preferences["nuke_path"], 2)

    def about(self):
        dialog = lambda: OkDialog.OkDialog(self.parent, "Credits", "Super Pipe\nPipeline manager\n(C) Lucas Boutrot", padding = 20)
        self.wait_window(dialog().top)

    def refresh(self, e):
        if self.version_list.curselection():
            selected_version = self.version_list.curselection()[0]
            
            if self.current_project.getSelectionType() == "shot":
                self.updateVersionListView(shot = self.current_project.getSelection())
            elif self.current_project.getSelectionType() == "asset":
                self.updateVersionListView(asset = self.current_project.getSelection())

            self.version_list.select_set(selected_version)

            self.versionlistCommand(None)

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
