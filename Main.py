#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

#EXTERNAL LIBRARIES : pillow, watchdog, numpy, opencv

from NewProjectDialog import *
from Shot import *
from Project import *
from Resources import *
from ListsObserver import *
from tkinter import *
from tkinter import filedialog, ttk
from os import path, mkdir
from urllib.parse import urlsplit
from PIL import ImageTk
# from watchdog.observers import Observer
from CustomSlider import *
from CustomVideoPlayer import *
import PIL
import NewShotDialog
import NewAssetDialog
import RenameAssetDialog
import ProjectSettingsDialog
import PreferencesDialog
import ManageBackupsDialog
import YesNoDialog
import OkDialog
import subprocess
import webbrowser
# import queue

try:
    from SuperLicenseManager import *
    from licensed_content.StatisticsView import *
except Exception as e:
    print("No license version")
    print(str(e))

class SuperPipe(Frame):
    def __init__(self, parent):
        try:
            license_manager = SuperLicenseManager()
            self.valid_license = license_manager.checkLicense()
        except:
            self.valid_license = False

        if not path.isfile("save/options.spi"):
            with open("save/options.spi", "w") as f:
                f.write("C:/Program Files/Autodesk/Maya2017/bin/maya.exe\ntheme_default\nC:/Program Files/Houdini/houdini.exe\nC:/Program Files/Blender/blender.exe\nC:/Program Files/VLC/vlc.exe\n\n")
            f.close()

        ## THEME COLORS ##
        self.theme = Resources.readLine("save/options.spi", 2)
        self.main_color = Resources.readLine("save/themes/" + self.theme + ".spi", 1)
        self.second_color = Resources.readLine("save/themes/" + self.theme + ".spi", 2)
        self.list_color = Resources.readLine("save/themes/" + self.theme + ".spi", 3)
        self.button_color1 = Resources.readLine("save/themes/" + self.theme + ".spi", 4)
        self.over_button_color1 = Resources.readLine("save/themes/" + self.theme + ".spi", 5)
        self.button_color2 = Resources.readLine("save/themes/" + self.theme + ".spi", 6)
        self.over_button_color2 = Resources.readLine("save/themes/" + self.theme + ".spi", 7)
        self.separator_color = Resources.readLine("save/themes/" + self.theme + ".spi", 8)
        self.text_color = Resources.readLine("save/themes/" + self.theme + ".spi", 9)
        self.done_color = Resources.readLine("save/themes/" + self.theme + ".spi", 12)
        self.urgent_color = Resources.readLine("save/themes/" + self.theme + ".spi", 13)
        self.high_color = Resources.readLine("save/themes/" + self.theme + ".spi", 14)
        self.medium_color = Resources.readLine("save/themes/" + self.theme + ".spi", 15)
        self.done_select_color = Resources.readLine("save/themes/" + self.theme + ".spi", 16)
        self.urgent_select_color = Resources.readLine("save/themes/" + self.theme + ".spi", 17)
        self.high_select_color = Resources.readLine("save/themes/" + self.theme + ".spi", 18)
        self.medium_select_color = Resources.readLine("save/themes/" + self.theme + ".spi", 19)

        Frame.__init__(self, parent, bg = self.main_color)

        self.parent = parent

        self.parent.config(cursor = "wait")
        self.parent.update()

        self.current_project = None
        self.version_mode = True

        self.parent.protocol("WM_DELETE_WINDOW", self.exitCommand)

        self.maya_path = Resources.readLine("save/options.spi", 3)
        self.houdini_path = Resources.readLine("save/options.spi", 4)
        self.blender_path = Resources.readLine("save/options.spi", 5)
        self.vlc_path = Resources.readLine("save/options.spi", 6)

        self.initUI()

        project_directory = Resources.readLine("save/options.spi", 1)

        if project_directory:
            if path.isdir(project_directory):
                self.current_project = Project(project_directory)
                self.add_shot_button.config(state = NORMAL)
                self.add_asset_button.config(state = NORMAL)
                self.shots_preview_button.config(state = NORMAL)
                self.custom_button.config(state = NORMAL)

                self.parent.title("Super Pipe || " + self.current_project.getDirectory())

                self.asset_list.configure(selectmode = "browse")

                self.menu_project.entryconfig(0, state = NORMAL)
                self.menu_project.entryconfig(1, state = NORMAL)
                self.menu_project.entryconfig(3, state = NORMAL)
                self.menu_project.entryconfig(4, state = NORMAL)
                self.menu_project.entryconfig(6, state = NORMAL)

                self.updateShotListView()
                self.updateAssetListView()

        if self.current_project:
            self.var_home_page_title.set("THE PROJECT \"" + self.current_project.getName() + "\" IS SET")
            try:
                self.statistics_view.set(self.current_project)
            except:
                print("IMPORT ERROR")
            # event_handler = ListsObserver(self.shot_list, self.current_project.getDirectory() + "/05_shot/")
            # self.observer = Observer()
            # self.observer.schedule(event_handler, path = self.current_project.getDirectory() + "/05_shot/", recursive = False)
            # self.observer.start()

        self.parent.config(cursor = "")

        if not self.valid_license:
            dialog = lambda: OkDialog.OkDialog(self.parent, "License error", "Do you have license ? Or it may be expired :(")
            self.wait_window(dialog().top)

    def initUI(self):
        self.parent["bg"] = self.main_color
        self.parent.title("Super Pipe")
        self.pack(fill = "both", expand = True)

        self.parent.bind("<F5>", self.refresh)
        self.parent.bind("<Control-n>", self.newProjectCommand)
        self.parent.bind("<Control-o>", self.setProjectCommand)
        self.parent.bind("<Control-p>", self.preferencesCommand)
        self.parent.bind("<Control-a>", self.addAssetCommand)
        self.parent.bind("<Control-s>", self.addShotCommand)
        self.parent.bind("<s>", self.projectStatisticsCommand)

        menu_bar = Menu(self.parent)

        menu_file = Menu(menu_bar, tearoff = 0)
        menu_file.add_command(label = "New project", command = self.newProjectCommand, accelerator = "Ctrl+N")
        menu_file.add_command(label = "Set project", command = self.setProjectCommand, accelerator = "Ctrl+O")
        menu_file.add_separator()
        # menu_file.add_command(label = "Update project", command = self.updateProjectCommand)
        # menu_file.add_separator()
        menu_file.add_command(label = "Quit", command = self.parent.destroy, accelerator = "Alt+F4")
        menu_bar.add_cascade(label = "File", menu = menu_file)

        menu_edit = Menu(menu_bar, tearoff = 0)
        menu_edit.add_command(label = "Preferences", command = self.preferencesCommand, accelerator = "Ctrl+P")
        menu_bar.add_cascade(label = "Edit", menu = menu_edit)

        self.menu_project = Menu(menu_bar, tearoff = 0)
        self.menu_project.add_command(label = "Add asset", state = DISABLED, command = self.addAssetCommand, accelerator = "Ctrl+A")
        self.menu_project.add_command(label = "Add shot", state = DISABLED, command = self.addShotCommand, accelerator = "Ctrl+S")
        self.menu_project.add_separator()
        self.menu_project.add_command(label = "Project settings", state = DISABLED, command = self.projectSettingsCommand)
        self.menu_project.add_command(label = "Project statistics", state = DISABLED, command = self.projectStatisticsCommand)
        self.menu_project.add_separator()
        self.menu_project.add_command(label = "Clean backups", state = DISABLED, command = self.cleanBackupsCommand)
        menu_bar.add_cascade(label = "Project", menu = self.menu_project)

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

        self.var_asset_filter = StringVar()
        self.asset_filter_entry = Entry(top_left_side_bar, textvariable = self.var_asset_filter, relief = FLAT, bg = self.list_color, fg = self.text_color, width = 50, bd = 5, validate = "key", validatecommand = (self.register(self.validateAssetFilterEntry), '%P'))
        self.asset_filter_entry.pack(fill = X, pady = (0, 10), padx = 20)

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

        ## // NO PROJECT MAIN FRAME \\##
        self.main_area_home_page = Frame(main_area, bg = self.main_color, bd = 0)
        self.main_area_home_page.grid(row = 0, column = 0, sticky = N + S + W + E)
        self.main_area_home_page.pi = self.main_area_home_page.grid_info()

        self.var_home_page_title = StringVar()
        self.var_home_page_title.set("PLEASE SET AN EXISTING PROJECT, OR CREATE A NEW ONE")
        home_page_label = Label(self.main_area_home_page, textvariable = self.var_home_page_title, bg = self.main_color, fg = self.text_color, height = 1, justify = CENTER, font = "Helvetica 15 bold")
        home_page_label.pack(expand = True, fill = BOTH, side = BOTTOM)

        ###############################################################################################################

        ## // SHOTS MAIN FRAME \\ ##
        self.main_area_shot = Frame(main_area, bg = self.main_color, bd = 0)
        self.main_area_shot.grid(row = 0, column = 0, sticky = N + S + W + E)
        self.main_area_shot.pi = self.main_area_shot.grid_info()
        self.main_area_shot.grid_forget()

        self.main_area_shot.columnconfigure(0, pad = 10, minsize = 40)
        self.main_area_shot.columnconfigure(1, pad = 10)
        self.main_area_shot.columnconfigure(2, pad = 10, minsize = 50)
        self.main_area_shot.columnconfigure(3, pad = 10)
        self.main_area_shot.columnconfigure(4, pad = 10)
        self.main_area_shot.columnconfigure(5, pad = 10, weight = 2)
        self.main_area_shot.columnconfigure(6, pad = 10)

        self.main_area_shot.rowconfigure(0, pad = 20, minsize = 75)
        self.main_area_shot.rowconfigure(1, pad = 5, minsize = 75)
        self.main_area_shot.rowconfigure(2, pad = 5, minsize = 75)
        self.main_area_shot.rowconfigure(3, pad = 5, minsize = 410)
        self.main_area_shot.rowconfigure(4, pad = 5, minsize = 50)

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

        self.frame_range_entry = Entry(self.main_area_shot, relief = FLAT, bg = self.button_color2, bd = 5, width = 6, justify = CENTER, validate = "key", validatecommand = (self.register(self.validateFrameRangeEntry), '%P', '%S'))
        self.frame_range_entry.grid(row = 0, column = 3)
        self.frame_range_entry.pi = self.frame_range_entry.grid_info()
        self.frame_range_entry.grid_forget()

        self.frame_range_entry.bind("<Return>", self.frameRangeReturnClick)

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

        ## SHOT DESCRIPTION ##
        self.shot_description_line = Frame(self.main_area_shot, bg = self.second_color, bd = 0)
        self.shot_description_line.grid(row = 1, column = 0, columnspan = 7, sticky = W + E, pady = 10)

        self.shot_description_line.columnconfigure(0, pad = 10)
        self.shot_description_line.columnconfigure(1, pad = 10, weight = 1)
        self.shot_description_line.columnconfigure(2, pad = 10)

        shot_description_label = Label(self.shot_description_line, text = "Shot description :", bg = self.second_color, fg = self.text_color, height = 1, pady = 10, anchor = NW, font = "Helvetica 9 bold")
        shot_description_label.grid(row = 0, column = 1)

        self.var_shot_description = StringVar()
        self.shot_description_entry = Entry(self.shot_description_line, textvariable = self.var_shot_description, state = "readonly", readonlybackground = self.main_color, relief = FLAT, bg = self.main_color, fg = self.text_color, width = 750, bd = 5, validate = "key", validatecommand = (self.register(self.validateDescriptionEntry), '%P'))
        self.shot_description_entry.grid(row = 1, column = 1, sticky = N, pady = (0, 20), padx = 100)

        ## SHOT STATE ##
        self.shot_state_line = Frame(self.main_area_shot, bg = self.main_color, bd = 0)
        self.shot_state_line.grid(row = 2, column = 0, columnspan = 7, sticky = W + E, pady = 10)

        self.shot_state_line.columnconfigure(0, pad = 10, minsize = 75)
        self.shot_state_line.columnconfigure(1, pad = 10, minsize = 100)
        self.shot_state_line.columnconfigure(2, pad = 50)
        self.shot_state_line.columnconfigure(4, pad = 50)

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

        self.step_slider = CustomSlider(self.shot_state_line, width = 500, height = 20, steps = ("Layout", "Blocking", "Splining", "Rendering"), bg = self.button_color2, fg = self.button_color1, txt = self.text_color, grid = self.separator_color)
        self.step_slider.grid(row = 0, column = 3)
        self.step_slider.pi = self.step_slider.grid_info()
        self.step_slider.grid_forget()
        self.step_slider.bind("<ButtonRelease-1>", self.customSliderCommand)

        self.upgrade_shot_button = Button(self.shot_state_line, text = "Upgrade shot", bg = self.button_color2, activebackground = self.over_button_color2, activeforeground = self.text_color, fg = self.text_color, bd = 0, width = 13, height = 1, command = self.upgradeShotCommand)
        self.upgrade_shot_button.grid(row = 0, column = 4)
        self.upgrade_shot_button.pi = self.upgrade_shot_button.grid_info()
        self.upgrade_shot_button.grid_forget()

        self.var_shot_done = IntVar()
        self.done_shot_button = Checkbutton(self.shot_state_line, text = "Shot done", variable = self.var_shot_done, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleShotDone)
        self.done_shot_button.grid(row = 0, column = 5)
        self.done_shot_button.pi = self.done_shot_button.grid_info()
        self.done_shot_button.grid_forget()

        ## SHOT PICTURES ##
        self.pictures_shot = Frame(self.main_area_shot, bg = self.second_color, bd = 0)
        self.pictures_shot.grid(row = 3, column = 0, columnspan = 7, sticky = N + S + W + E, pady = 20)
        self.pictures_shot.pi = self.pictures_shot.grid_info()

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

        ## SHOT PLAYBLAST PICTURES ##
        self.playblast_pictures_shot = Frame(self.main_area_shot, bg = self.second_color, bd = 0)
        self.playblast_pictures_shot.grid(row = 3, column = 0, columnspan = 7, sticky = N + S + W + E, pady = 20)
        self.playblast_pictures_shot.pi = self.playblast_pictures_shot.grid_info()
        self.playblast_pictures_shot.grid_forget()

        self.playblast_pictures_shot.columnconfigure(0, weight = 1, minsize = 550)

        playblast_pict_label = Label(self.playblast_pictures_shot, text = "This playblast", bg = self.second_color, fg = self.text_color, height = 1, anchor = N, font = "Helvetica 11")
        playblast_pict_label.grid(row = 0, column = 0, pady = 10)

        self.playblast_player = CustomVideoPlayer(self.playblast_pictures_shot, "test.mov", 512, self.list_color)
        self.playblast_player.grid(row = 1, column = 0, pady = 20)

        ## SHOT VERSION ACTIONS ##
        self.shot_actions_line = Frame(self.main_area_shot, bg = self.main_color, bd = 0)
        self.shot_actions_line.grid(row = 4, column = 0, columnspan = 7, sticky = W + E, pady = 10)

        self.shot_actions_line.columnconfigure(0, pad = 10)
        self.shot_actions_line.columnconfigure(1, pad = 10, weight = 1)
        self.shot_actions_line.columnconfigure(2, pad = 10)

        self.open_shot_button = Button(self.shot_actions_line, text = "Open selected version ", bg = self.button_color1, activebackground = self.over_button_color1, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 19, height = 1, command = self.openShotCommand)
        self.open_shot_button.grid(row = 0, column = 1, sticky = N)
        self.open_shot_button.pi = self.open_shot_button.grid_info()
        self.open_shot_button.grid_forget()

        ## SHOT VERSION INFOS ##
        self.shot_version_management_line = Frame(self.main_area_shot, bg = self.second_color, bd = 0)
        self.shot_version_management_line.grid(row = 5, column = 0, columnspan = 7, sticky = W + E, pady = 10)

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
        self.shot_paths_line.grid(row = 6, column = 0, columnspan = 7, sticky = W + E, pady = 10, padx = 20)

        self.shot_paths_line.columnconfigure(0, pad = 10, weight = 1)

        file_path_label = Label()

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

        ## ASSET PICTURES ##
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

        ## ASSET PLAYBLAST PICTURES ##
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

        file_path_label = Label()

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

        scrollbar = ttk.Scrollbar(self.main_area_preview, orient = "vertical", command = self.preview_canva_scroll.yview)
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

        try:
            self.statistics_view = StatisticsView(main_area)
            self.statistics_view.grid(row = 0, column = 0, sticky = N + S + W + E)
            self.statistics_view.pi = self.statistics_view.grid_info()
            self.statistics_view.grid_forget()
        except:
            print("LICENSE ERROR")

        ###############################################################################################################

        right_side_bar = Frame(pw_main, bg = self.main_color)

        ## VERSIONS ##
        self.toggle_versions_playblasts_button = Button(right_side_bar, text = "Show playblasts", bg = self.button_color2, activebackground = self.over_button_color2, fg = self.text_color, activeforeground = self.text_color, bd = 0, width = 19, height = 1, command = self.toggleVersionsPlayblastsCommand)
        self.toggle_versions_playblasts_button.pack(pady = 10)

        self.var_versions_label = StringVar()
        self.var_versions_label.set("Versions")

        versions_label = Label(right_side_bar, textvariable = self.var_versions_label, bg = self.main_color, fg = self.text_color, font = "Helvetica 10 bold", width = 200)
        versions_label.pack(fill = NONE, pady = 10)

        display_buttons = Frame(right_side_bar, bg = self.main_color)
        display_buttons.pack(fill = X)

        self.asset_display_buttons = Frame(display_buttons, bg = self.main_color)
        self.asset_display_buttons.pack(fill = X, pady = 10, padx = 20)
        self.asset_display_buttons.pi = self.asset_display_buttons.pack_info()

        self.asset_display_buttons.columnconfigure(0, weight = 1)
        self.asset_display_buttons.columnconfigure(1, weight = 1)

        self.var_asset_display_modeling = IntVar()
        self.display_modeling_asset_button = Checkbutton(self.asset_display_buttons, text = "Display modeling", variable = self.var_asset_display_modeling, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleAssetDisplay)
        self.display_modeling_asset_button.grid(row = 0, column = 0, sticky = W)
        self.display_modeling_asset_button.select()

        self.var_asset_display_rigging = IntVar()
        self.display_rigging_asset_button = Checkbutton(self.asset_display_buttons, text = "Display rigging", variable = self.var_asset_display_rigging, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleAssetDisplay)
        self.display_rigging_asset_button.grid(row = 0, column = 1, sticky = W)
        self.display_rigging_asset_button.select()

        self.var_asset_display_lookdev = IntVar()
        self.display_lookdev_asset_button = Checkbutton(self.asset_display_buttons, text = "Display lookdev", variable = self.var_asset_display_lookdev, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleAssetDisplay)
        self.display_lookdev_asset_button.grid(row = 1, column = 0, sticky = W)
        self.display_lookdev_asset_button.select()

        self.var_asset_display_other = IntVar()
        self.display_other_asset_button = Checkbutton(self.asset_display_buttons, text = "Display other", variable = self.var_asset_display_other, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleAssetDisplay)
        self.display_other_asset_button.grid(row = 1, column = 1, sticky = W)
        self.display_other_asset_button.select()

        self.shot_display_buttons = Frame(display_buttons, bg = self.main_color)
        self.shot_display_buttons.pack(fill = X, pady = 10, padx = 20)
        self.shot_display_buttons.pi = self.shot_display_buttons.pack_info()
        self.shot_display_buttons.pack_forget()

        self.shot_display_buttons.columnconfigure(0, weight = 1)
        self.shot_display_buttons.columnconfigure(1, weight = 1)

        self.var_shot_display_layout = IntVar()
        self.display_layout_shot_button = Checkbutton(self.shot_display_buttons, text = "Display layout", variable = self.var_shot_display_layout, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleShotDisplay)
        self.display_layout_shot_button.grid(row = 0, column = 0, sticky = W)
        self.display_layout_shot_button.select()

        self.var_shot_display_blocking = IntVar()
        self.display_blocking_shot_button = Checkbutton(self.shot_display_buttons, text = "Display blocking", variable = self.var_shot_display_blocking, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleShotDisplay)
        self.display_blocking_shot_button.grid(row = 0, column = 1, sticky = W)
        self.display_blocking_shot_button.select()

        self.var_shot_display_splining = IntVar()
        self.display_splining_shot_button = Checkbutton(self.shot_display_buttons, text = "Display splining", variable = self.var_shot_display_splining, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleShotDisplay)
        self.display_splining_shot_button.grid(row = 1, column = 0, sticky = W)
        self.display_splining_shot_button.select()

        self.var_shot_display_rendering = IntVar()
        self.display_rendering_shot_button = Checkbutton(self.shot_display_buttons, text = "Display rendering", variable = self.var_shot_display_rendering, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleShotDisplay)
        self.display_rendering_shot_button.grid(row = 1, column = 1, sticky = W)
        self.display_rendering_shot_button.select()

        self.var_shot_display_other = IntVar()
        self.display_other_shot_button = Checkbutton(self.shot_display_buttons, text = "Display other", variable = self.var_shot_display_other, bg = self.main_color, activeforeground = self.text_color, fg = self.text_color, activebackground = self.main_color, selectcolor = self.second_color, command = self.toggleShotDisplay)
        self.display_other_shot_button.grid(row = 2, column = 0, sticky = W)
        self.display_other_shot_button.select()

        self.version_list = Listbox(right_side_bar, bg = self.list_color, selectbackground = self.second_color, bd = 0, highlightthickness = 0, width = 50, height = 70, exportselection = False)
        self.version_list.pack(fill = X, pady = 10)
        self.version_list.bind("<<ListboxSelect>>", self.versionlistCommand)

        pw_main.add(right_side_bar)
        pw_main.update()
        pw_main.sash_place(1, 1550, 0)

    def newProjectCommand(self, e = None):
        directory = {"dir":""}

        dialog = lambda: NewProjectDialog.NewProjectDialog(self.parent, (directory, "dir"))
        self.wait_window(dialog().top)

        if directory["dir"]:
            self.current_project = Project(directory["dir"])

            Resources.writeAtLine("save/options.spi", directory["dir"], 1)

            self.add_shot_button.config(state = NORMAL)
            self.add_asset_button.config(state = NORMAL)
            self.shots_preview_button.config(state = NORMAL)
            self.custom_button.config(state = NORMAL)

            self.parent.title("Super Pipe || " + self.current_project.getDirectory())

            self.asset_list.configure(selectmode = "browse")

            self.menu_project.entryconfig(0, state = NORMAL)
            self.menu_project.entryconfig(1, state = NORMAL)
            self.menu_project.entryconfig(3, state = NORMAL)
            self.menu_project.entryconfig(5, state = NORMAL)

            self.updateShotListView()
            self.updateAssetListView()

    def setProjectCommand(self, e = None):
        directory = filedialog.askdirectory(title = "New project", mustexist  = False)

        self.parent.config(cursor = "wait")
        self.parent.update()

        if directory:
            if path.isdir(directory):
                self.current_project = Project(directory)

                if self.current_project.isValid():

                    Resources.writeAtLine("save/options.spi", directory, 1)

                    self.add_shot_button.config(state = NORMAL)
                    self.add_asset_button.config(state = NORMAL)
                    self.shots_preview_button.config(state = NORMAL)
                    self.custom_button.config(state = NORMAL)

                    self.parent.title("Super Pipe || " + self.current_project.getDirectory())

                    self.asset_list.configure(selectmode = "browse")

                    self.menu_project.entryconfig(0, state = NORMAL)
                    self.menu_project.entryconfig(1, state = NORMAL)
                    self.menu_project.entryconfig(3, state = NORMAL)
                    self.menu_project.entryconfig(5, state = NORMAL)


                    self.var_home_page_title.set("THE PROJECT \"" + self.current_project.getName() + "\" IS SET")

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
                                rename(directory + "/04_asset/" + cat + "/" + asset + "/data", directory + "/04_asset/" + cat + "/" + asset + "/superpipe")
                                mkdir(directory + "/04_asset/" + cat + "/" + asset + "/data")

                for shot in listdir(directory + "/05_shot/"):
                    if shot != "backup":
                        if not path.isdir(directory + "/05_shot/" + shot + "/superpipe"):
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
        self.open_shot_button.grid(self.open_shot_button.pi)

        self.downgrade_shot_button.grid(self.downgrade_shot_button.pi)

        self.step_slider.setCurrentStep("Layout")
        self.step_slider.grid(self.step_slider.pi)

        self.upgrade_shot_button.grid(self.upgrade_shot_button.pi)
        self.done_shot_button.grid(self.done_shot_button.pi)

        self.updateVersionListView(shot = shot)
        self.version_list.select_set(0)

        selected_line = self.version_list.curselection()[0]

        temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.get(selected_line)

        self.var_selection_path_label.set(temp_path.replace("/", "\\"))

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

    def addShotCommand(self, e = None):
        if len(self.current_project.getShotList()) >= 99:
            dialog = lambda: OkDialog.OkDialog(self.parent, "No more shots", "Sorry ! Superpipe does not handle more than 99 shots at the moment")
            self.wait_window(dialog().top)

        else:
            sequence = {"seq": 0}

            dialog = lambda: NewShotDialog.NewShotDialog(self.parent, self.current_project, (sequence, "seq"))
            self.wait_window(dialog().top)

            if sequence["seq"]:
                shot_nb = self.current_project.createShot(sequence["seq"])
                self.updateShotListView()
                self.shot_list.select_set(shot_nb - 1)
                self.shotlistCommand()

    def addAssetCommand(self, e = None):
        asset = {"cat": None, "name" : None, "software" : None}

        dialog = lambda: NewAssetDialog.NewAssetDialog(self.parent, self.current_project, (asset, "cat", "name", "software"))
        self.wait_window(dialog().top)

        if asset["cat"] and asset["name"] and asset["software"]:
            if self.current_project.createAsset(asset["name"], asset["cat"], Resources.getSoftwareName(asset["software"])):
                self.updateAssetListView()

                self.asset_list.item(Resources.getCategoryName(asset["cat"]), open = True)

                self.asset_list.selection_set(asset["name"])
                self.asset_list.focus_set()
                self.asset_list.focus(asset["name"])
                self.assetListCommand(None)
            else:
                dialog = lambda: OkDialog.OkDialog(self.parent, "Asset already exists", "The asset \"" + asset["name"] + "\" already exists")
                self.wait_window(dialog().top)

    def shotlistCommand(self, e = None):
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
            if self.valid_license:
                self.statistics_view.grid_forget()

            self.asset_list.selection_remove(self.asset_list.focus())

            self.delete_shot_button.grid(self.delete_shot_button.pi)

            self.current_project.setSelection(shot_name = selected_shot)
            shot = self.current_project.getSelection()

            if Shot.validShot(shot.getDirectory()):
                self.updateVersionListView(shot = shot)
                self.version_list.select_set(0)
                self.var_shot_version_comment.set(self.current_project.getSelection().getComment(self.version_list.get(0)))

                self.var_shot_done.set(int(Resources.readLine(shot.getDirectory() + "/superpipe/shot_data.spi", 1)))
                self.var_shot_priority.set(Resources.readLine(shot.getDirectory() + "/superpipe/shot_data.spi", 2))

                self.priority_shot_label.grid(self.priority_shot_label.pi)
                self.priority_shot_menu.grid(self.priority_shot_menu.pi)
                self.open_shot_folder_button.grid(self.open_shot_folder_button.pi)

                shot_description = Resources.readLine(shot.getDirectory() + "/superpipe/shot_data.spi", 6)
                if shot_description:
                    self.var_shot_description.set(shot_description)
                else:
                    self.var_shot_description.set("")

                self.shot_description_entry.config(state = NORMAL)

                if shot.isSet():
                    self.set_shot_button.grid_forget()
                    self.frame_range_entry.grid(self.frame_range_entry.pi)
                    self.set_shot_frame_range_button.grid(self.set_shot_frame_range_button.pi)
                    self.open_shot_button.grid(self.open_shot_button.pi)

                    self.downgrade_shot_button.grid(self.downgrade_shot_button.pi)

                    self.step_slider.setCurrentStep(shot.getStep())
                    if shot.isDone():
                        self.step_slider.setPercentage(100)
                        self.step_slider.setActive(active = False)
                    else:
                        self.step_slider.setPercentage(int(Resources.readLine(shot.getDirectory() + "/superpipe/shot_data.spi", 7)))
                        self.step_slider.setActive(active = True)
                    self.step_slider.grid(self.step_slider.pi)

                    self.upgrade_shot_button.grid(self.upgrade_shot_button.pi)
                    self.done_shot_button.grid(self.done_shot_button.pi)

                    self.frame_range_entry.delete(0, len(self.frame_range_entry.get()))
                    self.frame_range_entry.insert(0, self.current_project.getSelection().getFrameRange())

                    if shot.getStep() == "Layout":
                        self.upgrade_shot_button.config(state = NORMAL)
                        self.downgrade_shot_button.config(state = DISABLED)
                    elif shot.getStep() == "Blocking":
                        self.upgrade_shot_button.config(state = NORMAL)
                        self.downgrade_shot_button.config(state = NORMAL)
                    elif shot.getStep() == "Splining":
                        self.upgrade_shot_button.config(state = NORMAL)
                        self.downgrade_shot_button.config(state = NORMAL)
                    elif shot.getStep() == "Rendering":
                        self.upgrade_shot_button.config(state = DISABLED)
                        self.downgrade_shot_button.config(state = NORMAL)

                    selected_line = self.version_list.curselection()[0]
                    if self.current_project.getSelectionType() == "shot":
                        temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.get(selected_line)
                    elif self.current_project.getSelection().getSoftware() == "maya":
                        temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.get(selected_line)
                    elif self.current_project.getSelection().getSoftware() == "houdini":
                        temp_path = self.current_project.getSelection().getDirectory() + "/" + self.version_list.get(selected_line)

                    self.var_selection_path_label.set(temp_path.replace("/", "\\"))

                    temp_path = self.current_project.getSelection().getDirectory() + "/cache/alembic/" + path.splitext(self.version_list.get(selected_line))[0] + ".abc"

                    if not path.isfile(temp_path):
                        temp_path = ""

                    self.var_selection_abc_path_label.set(temp_path.replace("/", "\\"))

                    if self.version_mode:
                        pict_path = shot.getDirectory() + "/images/screenshots/" + path.splitext(self.version_list.get(self.version_list.curselection()[0]))[0] + ".jpg"

                        if path.isfile(pict_path):
                            pict = ImageTk.PhotoImage(file = pict_path)

                            self.shot_gifdict[pict_path] = pict

                            self.shot_pict_caneva.grid(self.shot_pict_caneva.pi)
                            self.shot_pict_caneva.create_image(0, 0, anchor = N + W, image = pict)
                            self.shot_pict_caneva.config(height = pict.height(), width = pict.width())

                        else:
                            self.shot_pict_caneva.grid_forget()

                    else:
                        selected_line = self.version_list.curselection()[0]
                        selected_shot_version = self.version_list.get(selected_line)

                        playblast_file = shot.getDirectory() + "/movies/" + selected_shot_version

                        self.playblast_player.updateVideo(playblast_file)

                else:
                    self.set_shot_button.grid(self.set_shot_button.pi)
                    self.frame_range_entry.grid_forget()
                    self.set_shot_frame_range_button.grid_forget()
                    self.open_shot_button.grid_forget()

                    self.downgrade_shot_button.grid_forget()

                    self.step_slider.grid_forget()

                    self.upgrade_shot_button.grid_forget()
                    self.done_shot_button.grid_forget()

                    self.shot_pict_caneva.grid_forget()

                    self.var_selection_path_label.set("")
                    self.var_selection_abc_path_label.set("")

                prev_pict_path = ""

                prev_shot_nb = shot.getShotNb() - 1

                if prev_shot_nb > 0:
                    for shot_dir in listdir(self.current_project.getDirectory() + "/05_shot/"):
                        if re.match(r"s[0-9][0-9]p[0-9][0-9]", shot_dir):
                            if int(shot_dir[-2:]) == prev_shot_nb:
                                all_picts_path = self.current_project.getDirectory() + "/05_shot/" + shot_dir + "/images/screenshots/"

                                if Shot.validShot(self.current_project.getDirectory() + "/05_shot/" + shot_dir):
                                    if path.isdir(all_picts_path):
                                        all_picts_path_array = []

                                        for f in listdir(all_picts_path):
                                            if ".jpg" in f:
                                                all_picts_path_array.append(all_picts_path + f)

                                        if all_picts_path_array:
                                            prev_pict_path = max(all_picts_path_array, key = path.getmtime)

                                    else:
                                        mkdir(all_picts_path)

                if path.isfile(prev_pict_path):
                    pict = ImageTk.PhotoImage(file = prev_pict_path)

                    self.shot_prev_gifdict[prev_pict_path] = pict

                    self.shot_prev_pict_caneva.grid(self.shot_prev_pict_caneva.pi)
                    self.shot_prev_pict_caneva.create_image(0, 0, anchor = N + W, image = pict)
                    self.shot_prev_pict_caneva.config(height = pict.height(), width = pict.width())
                else:
                    self.shot_prev_pict_caneva.grid_forget()

            else:
                dialog = lambda: OkDialog.OkDialog(self.parent, "Error", "The shot \"" + shot.getShotName() + "\" is not available !")
                self.wait_window(dialog().top)

    def assetListCommand(self, e):
        if self.current_project:
            if self.asset_list.focus():
                self.main_area_asset.grid(self.main_area_asset.pi)
                self.main_area_shot.grid_forget()
                self.main_area_preview.grid_forget()
                if self.valid_license:
                    self.statistics_view.grid_forget()

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

                    if path.isdir(asset.getDirectory()):
                        self.var_asset_label.set("ASSET " + self.asset_list.focus().upper())
                        self.delete_asset_button.grid(self.delete_asset_button.pi)
                        self.rename_asset_button.grid(self.rename_asset_button.pi)

                        self.priority_asset_label.grid(self.priority_asset_label.pi)
                        self.priority_asset_menu.grid(self.priority_asset_menu.pi)

                        self.updateVersionListView(asset = asset)
                        self.version_list.select_set(0)
                        self.var_asset_version_comment_label.set(self.current_project.getSelection().getComment(self.version_list.get(0)))

                        self.var_asset_priority.set(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 1))
                        self.var_asset_modeling_done.set(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 2)))
                        self.var_asset_rig_done.set(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 3)))
                        self.var_asset_lookdev_done.set(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 4)))
                        self.var_asset_done.set(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 5)))

                        if self.version_mode:
                            if asset:
                                if asset.isSet():
                                    self.set_asset_button.grid_forget()
                                    self.open_asset_button.grid(self.open_asset_button.pi)
                                    self.open_asset_folder_button.grid(self.open_asset_folder_button.pi)

                                    selected_line = self.version_list.curselection()[0]
                                    if asset.getSoftware() == "maya":
                                        temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.get(selected_line)
                                    elif asset.getSoftware() == "houdini":
                                        temp_path = self.current_project.getSelection().getDirectory() + "/" + self.version_list.get(selected_line)

                                    self.var_selection_path_label.set(temp_path.replace("/", "\\"))

                                    self.modeling_done_asset_button.grid(self.modeling_done_asset_button.pi)
                                    self.rig_done_asset_button.grid(self.rig_done_asset_button.pi)
                                    self.lookdev_done_asset_button.grid(self.lookdev_done_asset_button.pi)
                                    self.done_asset_button.grid(self.done_asset_button.pi)

                                    pict_path = asset.getDirectory() + "/images/screenshots/" + path.splitext(self.version_list.get(self.version_list.curselection()[0]))[0] + ".jpg"

                                    if path.isfile(pict_path):
                                        pict = ImageTk.PhotoImage(file = pict_path)

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
                        dialog = lambda: OkDialog.OkDialog(self.parent, "Error", "The asset \"" + asset.getAssetName() + "\" is not available !")
                        self.wait_window(dialog().top)

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
        if self.version_list.size():
            self.open_asset_button.grid(self.open_asset_button.pi)
            self.open_asset_folder_button.grid(self.open_asset_folder_button.pi)

            selected_line = self.version_list.curselection()[0]
            selected_version = self.version_list.get(selected_line)

            if path.isfile(self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version):
                if self.current_project.getSelectionType() == "shot":
                    temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version
                elif self.current_project.getSelection().getSoftware() == "maya":
                    temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version
                elif self.current_project.getSelection().getSoftware() == "houdini":
                    temp_path = self.current_project.getSelection().getDirectory() + "/" + selected_version
            else:
                temp_path = self.current_project.getSelection().getDirectory() + "/scenes/edits/" + selected_version

            self.var_selection_path_label.set(temp_path.replace("/", "\\"))

            pict_path = self.current_project.getSelection().getDirectory() + "/images/screenshots/" + path.splitext(selected_version)[0] + ".jpg"

            if self.current_project.getSelectionType() == "shot":
                if self.version_mode:
                    self.var_shot_version_comment.set(self.current_project.getSelection().getComment(selected_version))

                    if path.isfile(pict_path):
                        pict = ImageTk.PhotoImage(file = pict_path)

                        self.shot_gifdict[pict_path] = pict

                        self.shot_pict_caneva.grid(self.shot_pict_caneva.pi)
                        self.shot_pict_caneva.create_image(0, 0, anchor = N + W, image = pict)
                        self.shot_pict_caneva.config(height = pict.height(), width = pict.width())
                    else:
                        self.shot_pict_caneva.grid_forget()
                else:
                    shot = self.current_project.getSelection()

                    selected_line = self.version_list.curselection()[0]
                    selected_shot_version = self.version_list.get(selected_line)

                    playblast_file = shot.getDirectory() + "/movies/" + selected_shot_version

                    self.playblast_player.updateVideo(playblast_file)

            elif self.current_project.getSelectionType() == "asset":
                self.var_asset_version_comment_label.set(self.current_project.getSelection().getComment(selected_version))

                if path.isfile(pict_path):
                    pict = ImageTk.PhotoImage(file = pict_path)

                    self.asset_gifdict[pict_path] = pict

                    self.asset_pict_caneva.grid(self.asset_pict_caneva.pi)
                    self.asset_pict_caneva.create_image(0, 0, anchor = N + W, image = pict)
                    self.asset_pict_caneva.config(height = pict.height(), width = pict.width())
                else:
                    self.asset_pict_caneva.grid_forget()

    def openShotCommand(self):
        if self.version_list.size(): 
            selected_line = self.version_list.curselection()[0]
            selected_shot_version = self.version_list.get(selected_line)

            shot = self.current_project.getSelection()

            if self.version_mode:
                try:
                    if path.isfile(shot.getDirectory() + "/scenes/" + selected_shot_version):
                        maya_file = shot.getDirectory() + "/scenes/" + selected_shot_version
                    else:
                        maya_file = shot.getDirectory() + "/scenes/edits/" + selected_shot_version

                    maya_args = [self.maya_path, "-file", maya_file, "-proj", shot.getDirectory()]
                    subprocess.Popen(maya_args)
                except:
                    dialog = lambda: OkDialog.OkDialog(self.parent, "Maya path", "Check Maya path in Edit > Preferences")
                    self.wait_window(dialog().top)
            else:
                try:
                    playblast_file = shot.getDirectory() + "/movies/" + selected_shot_version
                    subprocess.Popen("%s %s" % (self.vlc_path, playblast_file.replace("/", "\\")))
                except:
                    dialog = lambda: OkDialog.OkDialog(self.parent, "VLC path", "Check VLC path in Edit > Preferences")
                    self.wait_window(dialog().top)

    def openAssetCommand(self):
        if self.version_list.size(): 
            selected_line = self.version_list.curselection()[0]
            selected_asset_version = self.version_list.get(selected_line)

            asset = self.current_project.getSelection()

            if self.version_mode:
                if asset.getSoftware() == "maya":
                    try:
                        if path.isfile(asset.getDirectory() + "/scenes/" + selected_asset_version):
                            maya_file = asset.getDirectory() + "/scenes/" + selected_asset_version
                        else:
                            maya_file = asset.getDirectory() + "/scenes/edits/" + selected_asset_version

                        maya_args = [self.maya_path, "-file", maya_file, "-proj", asset.getDirectory()]
                        subprocess.Popen(maya_args)
                    except:
                        dialog = lambda: OkDialog.OkDialog(self.parent, "Maya path", "Check Maya path in Edit > Preferences")
                        self.wait_window(dialog().top)

                elif asset.getSoftware() == "houdini":
                    try:
                        if path.isfile(asset.getDirectory() + "/" + selected_asset_version):
                            houdini_file = asset.getDirectory() + "/" + selected_asset_version
                        else:
                            houdini_file = asset.getDirectory() + "/backup/" + selected_asset_version

                        subprocess.Popen("%s %s" % (self.houdini_path, houdini_file))
                    except:
                        dialog = lambda: OkDialog.OkDialog(self.parent, "Houdini path", "Check Houdini path in Edit > Preferences")
                        self.wait_window(dialog().top)

                elif asset.getSoftware() == "blender":
                    try:
                        if path.isfile(asset.getDirectory() + "/" + selected_asset_version):
                            blender_file = asset.getDirectory() + "/" + selected_asset_version
                        else:
                            blender_file = asset.getDirectory() + "/backup/" + selected_asset_version

                        subprocess.Popen("%s %s" % (self.blender_path, blender_file))
                    except:
                        dialog = lambda: OkDialog.OkDialog(self.parent, "Blender path", "Check Blender path in Edit > Preferences")
                        self.wait_window(dialog().top)
            else:
                try:
                    playblast_file = asset.getDirectory() + "/movies/" + selected_asset_version
                    subprocess.Popen("%s %s" % (self.vlc_path, playblast_file.replace("/", "\\")))
                except:
                    dialog = lambda: OkDialog.OkDialog(self.parent, "VLC path", "Check VLC path in Edit > Preferences")
                    self.wait_window(dialog().top)

    def renameAssetCommand(self):
        asset_name = {"name" : None}

        dialog = lambda: RenameAssetDialog.RenameAssetDialog(self.parent, (asset_name, "name"))
        self.wait_window(dialog().top)

        valid_name = True

        if asset_name["name"]:
            if asset_name["name"] == "superpipe":
                valid_name = False
            else:
                for check_asset in self.current_project.getAssetList():
                    if asset_name["name"] == check_asset[0]:
                        valid_name = False
                        break

        if valid_name:
            self.parent.config(cursor = "wait")
            self.parent.update()

            asset = self.current_project.getSelection()
            asset.renameAsset(asset_name["name"])

            self.current_project.updateAssetList()
            self.updateAssetListView()

            self.asset_list.selection_set(asset_name["name"])
            self.asset_list.focus_set()
            self.asset_list.focus(asset_name["name"])
            self.assetListCommand(None)

            self.parent.config(cursor = "")
        else:
            dialog = lambda: OkDialog.OkDialog(self.parent, "Error", "The asset \"" + asset_name["name"] + "\" already exists !")
            self.wait_window(dialog().top)

    def updateShotListView(self):
        self.shot_list.delete(0, END)

        shots = self.current_project.getShotList()

        for shot in shots:
            if path.isdir(self.current_project.getDirectory() + "/05_shot/" + shot[1] + "/superpipe"):
                self.shot_list.insert(shot[0], shot[1])

                cur_shot = Shot(self.current_project.getDirectory(), shot[1])

                if cur_shot.isDone():
                    self.shot_list.itemconfig(shot[0] - 1, bg = self.done_color, selectbackground = self.done_select_color)
                elif cur_shot.getPriority() == "Urgent":
                    self.shot_list.itemconfig(shot[0] - 1, bg = self.urgent_color, selectbackground = self.urgent_select_color)
                elif cur_shot.getPriority() == "High":
                    self.shot_list.itemconfig(shot[0] - 1, bg = self.high_color, selectbackground = self.high_select_color)
                elif cur_shot.getPriority() == "Medium":
                    self.shot_list.itemconfig(shot[0] - 1, bg = self.medium_color, selectbackground = self.medium_select_color)

            else:
                dialog = lambda: OkDialog.OkDialog(self.parent, "ERROR", "The shot " + shot[1] + " has a problem !", padding = 20)
                self.wait_window(dialog().top)
            
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
                if path.isdir(self.current_project.getDirectory() + "/04_asset" + asset[1] + "/" + asset[0] + "/superpipe"):
                    cur_asset = Asset(self.current_project.getDirectory(), asset[1], asset[0])

                    asset_subfolders = asset[1].split("/")

                    for i in range(len(asset_subfolders)):
                        if not self.asset_list.exists(asset_subfolders[i].lower()):
                            if i > 0:
                                self.asset_list.insert(asset_subfolders[i - 1].lower(), END, asset_subfolders[i].lower(), text = asset_subfolders[i].upper(), tags = ("folder"))

                    if self.asset_list.exists(asset[0]):
                        dialog = lambda: OkDialog.OkDialog(self.parent, "ERROR", "The asset \"" + asset[1].upper() + "/" + asset[0] + "\" already exists !", padding = 20)
                        self.wait_window(dialog().top)
                    else:
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
                else:
                    dialog = lambda: OkDialog.OkDialog(self.parent, "ERROR", "The asset \"" + asset[0] + "\" has a problem !", padding = 20)
                    self.wait_window(dialog().top)

    def updateVersionListView(self, shot = None, asset = None):
        self.version_list.delete(0, END)

        if shot:
            if self.version_mode:
                shot_versions = shot.getVersionsList(self.var_check_show_last.get(), self.var_shot_display_layout.get(), self.var_shot_display_blocking.get(), self.var_shot_display_splining.get(), self.var_shot_display_rendering.get(), self.var_shot_display_other.get())

                if shot_versions:
                    for shot_version in shot_versions:
                        self.version_list.insert(END, shot_version[1])

                self.asset_display_buttons.pack_forget()
                self.shot_display_buttons.pack(self.shot_display_buttons.pi)

            else:
                shot_playblasts = shot.getPlayblastsList()

                if shot_playblasts:
                    for shot_playblast in shot_playblasts:
                        self.version_list.insert(END, shot_playblast[1])

        elif asset:
            if self.version_mode:
                asset_versions = asset.getVersionsList(self.var_check_show_last.get(), self.var_asset_display_modeling.get(), self.var_asset_display_rigging.get(), self.var_asset_display_lookdev.get(), self.var_asset_display_other.get())

                if asset_versions:
                    for asset_version in asset_versions:
                        self.version_list.insert(END, asset_version[1])

                self.shot_display_buttons.pack_forget()
                self.asset_display_buttons.pack(self.asset_display_buttons.pi)

            else:
                asset_playblasts = asset.getPlayblastsList()

                if asset_playblasts:
                    for asset_playblast in asset_playblasts:
                        self.version_list.insert(END, asset_playblast[1])

    def moveShotUpCommand(self):
        self.parent.config(cursor = "wait")
        self.parent.update()

        loc = self.shot_list.yview()[0]

        self.up_button.config(state = DISABLED)
        self.down_button.config(state = DISABLED)

        self.current_project.moveShotUp(self.current_project.getSelection().getShotName())

        new_selection = self.shot_list.curselection()[0] + 1
        self.updateShotListView()
        self.shot_list.select_set(new_selection)

        self.shotlistCommand()

        self.up_button.config(state = NORMAL)
        self.down_button.config(state = NORMAL)

        self.shot_list.yview_moveto(loc)

        self.parent.config(cursor = "")

    def moveShotDownCommand(self):
        self.parent.config(cursor = "wait")
        self.parent.update()

        loc = self.shot_list.yview()[0]

        self.up_button.config(state = DISABLED)
        self.down_button.config(state = DISABLED)

        self.current_project.moveShotDown(self.current_project.getSelection().getShotName())

        new_selection = self.shot_list.curselection()[0] - 1
        self.updateShotListView()
        self.shot_list.select_set(new_selection)

        self.shotlistCommand()

        self.up_button.config(state = NORMAL)
        self.down_button.config(state = NORMAL)

        self.shot_list.yview_moveto(loc)

        self.parent.config(cursor = "")

    def toggleLastVersions(self):
        if self.current_project.getSelectionType() == "shot":
            self.updateVersionListView(shot = self.current_project.getSelection())
        elif self.current_project.getSelectionType() == "asset":
            if self.asset_list.focus() not in ["character", "fx", "props", "set"]:
                self.updateVersionListView(asset = self.current_project.getSelection())

        self.version_list.select_set(0)

    def toggleShotDone(self):
        loc = self.shot_list.yview()[0]
        selected_shot = self.shot_list.curselection()[0]
        self.current_project.getSelection().setDone(self.var_shot_done.get())
        if self.var_shot_done.get():
            self.step_slider.setPercentage(100)
        self.step_slider.setActive(not self.var_shot_done.get())
        self.updateShotListView()
        self.shot_list.select_set(selected_shot)
        self.shot_list.yview_moveto(loc)

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
        loc = self.shot_list.yview()[0]
        selected_shot = self.shot_list.curselection()[0]
        self.current_project.getSelection().setPriority(priority)
        self.updateShotListView()
        self.shot_list.select_set(selected_shot)
        self.shot_list.yview_moveto(loc)

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

        self.main_area_preview.grid(self.main_area_preview.pi)
        self.main_area_shot.grid_forget()
        self.main_area_asset.grid_forget()
        if self.valid_license:
            self.statistics_view.grid_forget()

        self.asset_list.selection_remove(self.asset_list.focus())
        self.shot_list.selection_clear(0, END)

        self.version_list.delete(0, END)

        all_shots_preview = []

        for shot_dir in listdir(self.current_project.getDirectory() + "/05_shot/"):
            if re.match(r"s[0-9][0-9]p[0-9][0-9]", shot_dir):
                all_picts_path = self.current_project.getDirectory() + "/05_shot/" + shot_dir + "/images/screenshots/"

                all_picts_path_array = []

                for f in listdir(all_picts_path):
                    if path.splitext(f)[1] == ".jpg" or path.splitext(f)[1] == ".gif":
                        all_picts_path_array.append(all_picts_path + f)

                cur_shot = Shot(self.current_project.getDirectory(), shot_dir)

                if all_picts_path_array:
                    all_shots_preview.append([cur_shot.getShotNb(), cur_shot.getShotName(), max(all_picts_path_array, key = path.getmtime)])
                else:
                    all_shots_preview.append([cur_shot.getShotNb(), cur_shot.getShotName(), "img/img_not_available.jpg"])

        for nb, name, img in all_shots_preview:
            shot_preview_caneva = Canvas(self.shots_preview_list, bg = self.main_color, bd = 0, highlightthickness = 0)

            to_edit_pict = PIL.Image.open(img)

            edited_pict = Resources.resizeImage(to_edit_pict, 256)

            pict = ImageTk.PhotoImage(edited_pict)

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

        self.shotlistCommand()

        self.step_slider.nextStep()

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

            self.shotlistCommand()

            self.step_slider.previousStep()

    def setShotFrameRangeCommand(self):
        self.current_project.getSelection().setFrameRange(int(self.frame_range_entry.get()))

    def openFolderCommand(self):
        subprocess.Popen("%s, \"%s\"" % ("explorer /root", self.current_project.getSelection().getDirectory().replace("/", "\\") + "\\"))

    ###############################################################################################################

    def toggleAssetDisplay(self):
        self.updateVersionListView(asset = self.current_project.getSelection())

    def toggleShotDisplay(self):
        self.updateVersionListView(shot = self.current_project.getSelection())

    def toggleVersionsPlayblastsCommand(self):
        self.version_mode = not self.version_mode

        if self.version_mode:
            self.toggle_versions_playblasts_button.config(text = "Show playblasts")
            self.var_versions_label.set("Versions")
            self.open_shot_button.config(text = "Open selected version")
            self.open_asset_button.config(text = "Open selected version")
            self.playblast_pictures_shot.grid_forget()
            self.pictures_shot.grid(self.pictures_shot.pi)
        else:
            self.toggle_versions_playblasts_button.config(text = "Show versions")
            self.var_versions_label.set("Playblasts")
            self.open_shot_button.config(text = "Open selected playblast")
            self.open_asset_button.config(text = "Open selected playblast")
            self.playblast_pictures_shot.grid(self.playblast_pictures_shot.pi)
            self.pictures_shot.grid_forget()

        if self.current_project.getSelectionType() == "shot":
            self.updateVersionListView(shot = self.current_project.getSelection())
        elif self.current_project.getSelectionType() == "asset":
            self.updateVersionListView(asset = self.current_project.getSelection())

        self.version_list.select_set(0)

    def validateFrameRangeEntry(self, P, S):
        valid = S.isnumeric() and len(P) < 6

        if not valid:
            self.bell()

        return valid

    def validateDescriptionEntry(self, P):
        if self.current_project:
            Resources.writeAtLine(self.current_project.getSelection().getDirectory() + "/superpipe/shot_data.spi", P, 6)

        return True

    def validateAssetFilterEntry(self, P):
        if P:
            filtered_asset_list = self.current_project.filterAssetList(P)

            for item in self.asset_list.get_children(""):
                self.asset_list.delete(item)

            for filtered_asset in filtered_asset_list:
                asset_subfolders = filtered_asset[1].split("/")

                for i in range(len(asset_subfolders)):
                    if not self.asset_list.exists(asset_subfolders[i].lower()):
                        if i > 0:
                            self.asset_list.insert(asset_subfolders[i - 1].lower(), END, asset_subfolders[i].lower(), text = asset_subfolders[i].upper(), tags = ("folder"))

                self.asset_list.insert(asset_subfolders[-1].lower(), END, filtered_asset[0], text = filtered_asset[0])

                self.asset_list.see(filtered_asset[0])

        else:
            for item in self.asset_list.get_children(""):
                self.asset_list.delete(item)

            self.asset_list.insert("", 1, "character", text = "CHARACTER")
            self.asset_list.insert("", 2, "fx", text = "FX")
            self.asset_list.insert("", 3, "props", text = "PROPS")
            self.asset_list.insert("", 4, "set", text = "SET")

            self.updateAssetListView()

        return True

    def customSliderCommand(self, e):
        Resources.writeAtLine(self.current_project.getSelection().getDirectory() + "/superpipe/shot_data.spi", str(self.step_slider.getPercentage()), 7)

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
            self.open_shot_button.grid_forget()
            self.open_shot_folder_button.grid_forget()
            self.priority_shot_menu.grid_forget()
            self.priority_shot_label.grid_forget()
            self.downgrade_shot_button.grid_forget()
            self.step_slider.grid_forget()
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

        dialog = lambda: ManageBackupsDialog.ManageBackupsDialog(self.parent, self.current_project, (settings, "res"))
        self.wait_window(dialog().top)

        if settings["res"]:            
            self.current_project.setResolution(settings["res"])

    def projectSettingsCommand(self):
        settings = {"res" : ""}

        dialog = lambda: ProjectSettingsDialog.ProjectSettingsDialog(self.parent, self.current_project, (settings, "res"))
        self.wait_window(dialog().top)

        if settings["res"]:            
            self.current_project.setResolution(settings["res"])

    def projectStatisticsCommand(self, e = None):
        self.statistics_view.update()
        self.statistics_view.grid(self.statistics_view.pi)
        self.main_area_asset.grid_forget()
        self.main_area_shot.grid_forget()
        self.main_area_preview.grid_forget()

    def preferencesCommand(self, e = None):
        if not path.isfile(self.current_project.getDirectory() + "/project_option.spi"):
            with open(self.current_project.getDirectory() + "/project_option.spi", "w") as f:
                f.write("www.google.fr\n")
            f.close()

        preferences = {"link" : None, "maya_path" : "", "houdini_path" : "", "blender_path" : "", "vlc_path" : "", "theme" : ""}

        dialog = lambda: PreferencesDialog.PreferencesDialog(self.parent, self.current_project.getDirectory() + "/project_option.spi", (preferences, "link", "maya_path", "houdini_path", "blender_path", "vlc_path", "theme"))
        self.wait_window(dialog().top)

        if preferences["link"] and preferences["maya_path"] and preferences["houdini_path"] and preferences["blender_path"] and preferences["vlc_path"] and preferences["theme"]:
            self.maya_path = preferences["maya_path"]
            self.houdini_path = preferences["houdini_path"]
            self.blender_path = preferences["blender_path"]
            self.vlc_path = preferences["vlc_path"]
            self.theme = preferences["theme"]

            Resources.writeAtLine(self.current_project.getDirectory() + "/project_option.spi", preferences["link"], 1)
            Resources.writeAtLine("save/options.spi", preferences["theme"], 2)
            Resources.writeAtLine("save/options.spi", preferences["maya_path"], 3)
            Resources.writeAtLine("save/options.spi", preferences["houdini_path"], 4)
            Resources.writeAtLine("save/options.spi", preferences["blender_path"], 5)
            Resources.writeAtLine("save/options.spi", preferences["vlc_path"], 6)

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

    def frameRangeReturnClick(self, e):
        self.setShotFrameRangeCommand()
        self.set_shot_frame_range_button.focus_set()

    def scrollCommand(self, e):
        self.preview_canva_scroll.configure(scrollregion = self.preview_canva_scroll.bbox("all"), width = 2000, height = self.parent.winfo_height())

    def wheelScrollCommand(self, e):
        self.preview_canva_scroll.yview_scroll(int(-1 * e.delta/120), "units")

    def exitCommand(self):
        self.parent.destroy()

def main():
    root = Tk()
    root.geometry("1280x720")
    root.state("zoomed")
    app = SuperPipe(root)
    root.iconbitmap("img/icon.ico")
    root.mainloop()

if __name__ == "__main__":
    main()
