#!/usr/bin/env python
# -*- coding: utf-8 -*-

#EXTERNAL LIBRARIES : pyside2, pillow, watchdog, numpy, opencv-python

from NewProjectDialogPySide import *
from Shot import *
from Project import *
from Resources import *
from ListsObserver import *
from tkinter import *
from tkinter import filedialog, ttk
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import *
from os import path, mkdir
from urllib.parse import urlsplit
from PIL import ImageTk
# from watchdog.observers import Observer
from CustomSlider import *
from CustomVideoPlayer import *
from StatisticsView import *

import sys
import PIL
import Theme
import NewShotDialog
from NewAssetDialogPySide import *
from NewShotDialogPySide import *
import RenameAssetDialog
import ProjectSettingsDialog
from PreferencesDialogPySide import *
import ManageBackupsDialog
import YesNoDialog
import OkDialog
import subprocess
import webbrowser
# import queue


class SuperPipePyside(QMainWindow):
	def __init__(self, app):
		if not path.isfile("save/options.spi"):
			with open("save/options.spi", "w") as f:
				f.write("\ntheme_default\nC:/Program Files/Autodesk/Maya2017/bin/maya.exe\nC:/Program Files/Houdini/houdini.exe\nC:/Program Files/Blender/blender.exe\nC:/Program Files/VLC/vlc.exe\n\n")
			f.close()

		super(SuperPipePyside, self).__init__()

		self.app = app

		self.app.setStyle('Fusion')

		default_palette = QPalette()
		dark_palette = QPalette()
		dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.WindowText, Qt.white)
		dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
		dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
		dark_palette.setColor(QPalette.ToolTipText, Qt.white)
		dark_palette.setColor(QPalette.Text, Qt.white)
		dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ButtonText, Qt.white)
		dark_palette.setColor(QPalette.BrightText, Qt.red)
		dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.HighlightedText, Qt.black)

		self.app.setPalette(dark_palette)

		# self.parent = parent

		self.app.setOverrideCursor(Qt.WaitCursor)
		# self.parent.update()

		self.current_project = None
		self.version_mode = True

		# self.parent.protocol("WM_DELETE_WINDOW", self.exitCommand)

		self.maya_path = Resources.readLine("save/options.spi", 3)
		self.houdini_path = Resources.readLine("save/options.spi", 4)
		self.blender_path = Resources.readLine("save/options.spi", 5)
		self.vlc_path = Resources.readLine("save/options.spi", 6)

		self.initUI()

		project_directory = Resources.readLine("save/options.spi", 1)

		if project_directory:
			if path.isdir(project_directory):
				self.current_project = Project(project_directory)
				self.add_shot_button.setEnabled(True)
				self.add_asset_button.setEnabled(True)
				self.shots_preview_button.setEnabled(True)
				self.custom_button.setEnabled(True)

				self.setWindowTitle("Super Pipe || " + self.current_project.getDirectory())

				# self.asset_list.configure(selectmode = "browse")

				self.add_asset_action.setEnabled(True)
				self.add_shot_action.setEnabled(True)
				self.project_settings_action.setEnabled(True)
				if self.current_project.getShotList():
					self.project_statistics_action.setEnabled(True)
				else:
					self.project_statistics_action.setEnabled(False)
				self.clean_backups_action.setEnabled(True)

				self.updateShotListView()
				self.updateAssetListView()

		if self.current_project:
			self.home_page_title_label.setText("THE PROJECT \"" + self.current_project.getName() + "\" IS SET")
			# self.statistics_view.set(self.current_project)
			# event_handler = ListsObserver(self.shot_list, self.current_project.getDirectory() + "/05_shot/")
			# self.observer = Observer()
			# self.observer.schedule(event_handler, path = self.current_project.getDirectory() + "/05_shot/", recursive = False)
			# self.observer.start()

		self.app.restoreOverrideCursor()


	def initUI(self):
		self.setWindowIcon(QIcon("img/icon.ico"))
		self.setWindowTitle("Super Pipe")

		######################
		#### MENU ACTIONS ####
		######################

		## File menu actions ##
		new_project_action = QAction("New project", self)
		new_project_action.setShortcut("Ctrl+N")
		new_project_action.triggered.connect(self.newProjectCommand)

		set_project_action = QAction("Set project", self)
		set_project_action.setShortcut("Ctrl+O")
		set_project_action.triggered.connect(self.setProjectCommand)

		exit_action = QAction("Quit", self)
		exit_action.setShortcut("Alt+F4")
		exit_action.triggered.connect(self.close)

		## Edit menu actions ##
		preferences_action = QAction("Preferences", self)
		preferences_action.setShortcut("Ctrl+P")
		preferences_action.triggered.connect(self.preferencesCommand)

		## Project menu actions ##
		self.add_asset_action = QAction("Add asset", self)
		self.add_asset_action.setShortcut("Ctrl+A")
		self.add_asset_action.triggered.connect(self.addAssetCommand)

		self.add_shot_action = QAction("Add shot", self)
		self.add_shot_action.setShortcut("Ctrl+S")
		self.add_shot_action.triggered.connect(self.addShotCommand)

		self.project_settings_action = QAction("Project settings", self)
		self.project_settings_action.triggered.connect(self.projectSettingsCommand)

		self.project_statistics_action = QAction("Project statistics", self)
		self.project_statistics_action.triggered.connect(self.projectStatisticsCommand)

		self.clean_backups_action = QAction("Clean backups", self)
		self.clean_backups_action.triggered.connect(self.cleanBackupsCommand)

		## Help menu actions ##
		about_action = QAction("About", self)
		about_action.triggered.connect(self.about)

		###############################################################################################################

		##################
		#### MENU BAR ####
		##################
		menu_bar = self.menuBar()

		file_menu = menu_bar.addMenu("File")
		file_menu.addAction(new_project_action)
		file_menu.addAction(set_project_action)
		file_menu.addSeparator()
		file_menu.addAction(exit_action)

		edit_menu = menu_bar.addMenu("Edit")
		edit_menu.addAction(preferences_action)

		project_menu = menu_bar.addMenu("Project")
		project_menu.addAction(self.add_asset_action)
		project_menu.addAction(self.add_shot_action)
		project_menu.addSeparator()
		project_menu.addAction(self.project_settings_action)
		project_menu.addAction(self.project_statistics_action)
		project_menu.addSeparator()
		project_menu.addAction(self.clean_backups_action)

		help_menu = menu_bar.addMenu("Help")
		help_menu.addAction(about_action)

		###############################################################################################################

		##################################
		##################################
		#### CREATE LAYOUTS & WIDGETS ####
		##################################
		##################################

		main_widget = QWidget()

		main_layout = QHBoxLayout()


		#################
		## LEFT COLUMN ##
		#################
		sidebar_left_widget = QWidget()
		sidebar_left_layout = QVBoxLayout()

		## // HEADER \\ ##
		sidebar_left_header_layout = QHBoxLayout()

		self.add_asset_button = QPushButton("Add asset")
		self.add_asset_button.clicked.connect(self.addAssetCommand)
		self.add_shot_button = QPushButton("Add shot")
		self.add_shot_button.clicked.connect(self.addShotCommand)

		sidebar_left_header_layout.addWidget(self.add_asset_button)
		sidebar_left_header_layout.addWidget(self.add_shot_button)

		sidebar_left_layout.addLayout(sidebar_left_header_layout)
 
		## // ASSET PART \\ ##
		sidebar_assets_layout = QVBoxLayout()

		asset_label = QLabel("Assets", alignment=Qt.AlignHCenter)
		asset_filter_entry = QLineEdit()
		self.asset_list = QTreeWidget()
		self.asset_list.setHeaderHidden(True)
		self.asset_list.currentItemChanged.connect(self.assetListCommand)
		self.categories = {"character":QTreeWidgetItem(["CHARACTER"]), "fx":QTreeWidgetItem(["FX"]), "props":QTreeWidgetItem(["PROPS"]), "set":QTreeWidgetItem(["SET"])}
		for cat in self.categories:
			self.asset_list.addTopLevelItem(self.categories[cat])

		sidebar_assets_layout.addWidget(asset_label)
		sidebar_assets_layout.addWidget(asset_filter_entry)
		sidebar_assets_layout.addWidget(self.asset_list)

		sidebar_left_layout.addLayout(sidebar_assets_layout)

		## // SHOT PART \\ ##
		sidebar_shots_layout = QVBoxLayout()

		shot_label = QLabel("Shots", alignment=Qt.AlignHCenter)
		self.shot_list = QListWidget()
		self.shot_list.clicked.connect(self.shotlistCommand)

		sidebar_shots_layout.addWidget(shot_label, alignment=Qt.AlignHCenter)
		sidebar_shots_layout.addWidget(self.shot_list)

		sidebar_left_layout.addLayout(sidebar_shots_layout)

		## // FOOTER \\ ##
		sidebar_left_footer_layout = QVBoxLayout()

		self.shots_preview_button = QPushButton("Shots preview")
		self.shots_preview_button.clicked.connect(self.shotsPreviewCommand)
		self.custom_button = QPushButton("Custom link")
		self.custom_button.clicked.connect(self.customButtonCommand)

		sidebar_left_footer_layout.addWidget(self.shots_preview_button)
		sidebar_left_footer_layout.addWidget(self.custom_button)

		sidebar_left_layout.addLayout(sidebar_left_footer_layout)

		## Finalize left column layout ##
		sidebar_left_widget.setLayout(sidebar_left_layout)
		sidebar_left_widget.setMaximumWidth(300)

		####################
		## CENTRAL COLUMN ##
		####################
		center_layout = QVBoxLayout()

		## // DEFAULT HOME PAGE \\ ##
		main_home_page_layout = QVBoxLayout()

		self.home_page_title_label = QLabel("PLEASE SET AN EXISTING PROJECT, OR CREATE A NEW ONE")
		main_home_page_layout.addWidget(self.home_page_title_label)
		self.main_home_page_widget = QWidget()
		self.main_home_page_widget.setLayout(main_home_page_layout)

		center_layout.addWidget(self.main_home_page_widget)

		## // ASSET PAGE \\ ##
		main_asset_layout = QVBoxLayout()

		## Asset general ##
		asset_general_layout = QHBoxLayout()

		self.asset_label = QLabel("NO ASSET SELECTED")
		self.delete_asset_button = QPushButton("Delete")
		self.delete_asset_button.clicked.connect(self.deleteAssetCommand)
		self.rename_asset_button = QPushButton("Rename asset")
		self.rename_asset_button.clicked.connect(self.renameAssetCommand)
		self.set_asset_button = QPushButton("Set asset")
		self.set_asset_button.clicked.connect(self.setAssetCommand)
		self.open_asset_folder_button = QPushButton("Open asset folder")
		self.open_asset_folder_button.clicked.connect(self.openFolderCommand)
		self.asset_show_last_only_button = QCheckBox("Show only last versions")
		self.asset_show_last_only_button.clicked.connect(self.toggleLastVersions)

		asset_general_layout.addWidget(self.asset_label)
		asset_general_layout.addWidget(self.delete_asset_button)
		asset_general_layout.addWidget(self.rename_asset_button)
		asset_general_layout.addWidget(self.set_asset_button)
		asset_general_layout.addWidget(self.open_asset_folder_button)
		asset_general_layout.addWidget(self.asset_show_last_only_button)

		main_asset_layout.addLayout(asset_general_layout)

		## Asset state ##
		asset_state_line_layout = QHBoxLayout()

		self.priority_asset_label = QLabel("Priority :")
		self.priority_asset_menu = QComboBox()
		self.priority_asset_menu.addItems(["Low", "Medium", "High", "Urgent"])
		self.priority_asset_menu.currentIndexChanged.connect(self.priorityAssetCommand)
		self.modeling_done_asset_button = QCheckBox("Modeling done")
		self.modeling_done_asset_button.clicked.connect(self.toggleAssetModelingDone)
		self.rig_done_asset_button = QCheckBox("Rig done")
		self.rig_done_asset_button.clicked.connect(self.toggleAssetRigDone)
		self.lookdev_done_asset_button = QCheckBox("Lookdev done")
		self.lookdev_done_asset_button.clicked.connect(self.toggleAssetLookdevDone)
		self.done_asset_button = QCheckBox("Asset done")
		self.done_asset_button.clicked.connect(self.toggleAssetDone)

		asset_state_line_layout.addWidget(self.priority_asset_label)
		asset_state_line_layout.addWidget(self.priority_asset_menu)
		asset_state_line_layout.addWidget(self.modeling_done_asset_button)
		asset_state_line_layout.addWidget(self.rig_done_asset_button)
		asset_state_line_layout.addWidget(self.lookdev_done_asset_button)
		asset_state_line_layout.addWidget(self.done_asset_button)

		main_asset_layout.addLayout(asset_state_line_layout)

		## Asset pictures ##
		asset_picture_layout = QVBoxLayout()

		asset_pict_title_label = QLabel("This asset :")

		self.asset_pict_widget = QLabel()

		asset_picture_layout.addWidget(asset_pict_title_label)
		asset_picture_layout.addWidget(self.asset_pict_widget)

		main_asset_layout.addLayout(asset_picture_layout)

		## Asset version actions ##
		asset_actions_layout = QVBoxLayout()

		self.open_asset_button = QPushButton("Open selected version")
		self.open_asset_button.clicked.connect(self.openAssetCommand)

		asset_actions_layout.addWidget(self.open_asset_button)

		main_asset_layout.addLayout(asset_actions_layout)

		## Asset version infos ##
		asset_version_comment_layout = QVBoxLayout()

		asset_version_comment_title_label = QLabel("Version comment :")
		self.asset_version_comment_label = QLabel()

		asset_version_comment_layout.addWidget(asset_version_comment_title_label)
		asset_version_comment_layout.addWidget(self.asset_version_comment_label)

		main_asset_layout.addLayout(asset_version_comment_layout)

		## Asset version paths ##
		asset_paths_layout = QVBoxLayout()

		self.file_path_label = QLabel()

		asset_paths_layout.addWidget(self.file_path_label)

		main_asset_layout.addLayout(asset_paths_layout)

		## Finalize asset layout ##
		self.main_asset_widget = QWidget()
		self.main_asset_widget.setLayout(main_asset_layout)
		self.main_asset_widget.setVisible(False)

		center_layout.addWidget(self.main_asset_widget)

		## // SHOT PAGE \\ ##
		main_shot_layout = QVBoxLayout()

		
		## Shot version actions ##
		shot_actions_layout = QVBoxLayout()

		self.open_shot_button = QPushButton("Open selected version")
		self.open_shot_button.clicked.connect(self.openShotCommand)

		shot_actions_layout.addWidget(self.open_shot_button)

		main_shot_layout.addLayout(asset_actions_layout)

		## Finalize asset layout ##
		self.main_shot_widget = QWidget()
		self.main_shot_widget.setLayout(main_shot_layout)
		self.main_shot_widget.setVisible(False)

		center_layout.addWidget(self.main_shot_widget)

		##################
		## RIGHT COLUMN ##
		##################
		sidebar_right_widget = QWidget()
		sidebar_right_layout = QVBoxLayout()

		## // TOP \\ ##
		sidebar_right_top_layout = QVBoxLayout()
		self.toggle_versions_playblasts_button = QPushButton("Show playblasts")
		self.toggle_versions_playblasts_button.clicked.connect(self.toggleVersionsPlayblastsCommand)
		self.versions_playblasts_label = QLabel("Versions", alignment=Qt.AlignHCenter)

		sidebar_right_top_layout.addWidget(self.toggle_versions_playblasts_button)
		sidebar_right_top_layout.addWidget(self.versions_playblasts_label)

		sidebar_right_layout.addLayout(sidebar_right_top_layout)

		## // MIDDLE \\ ##
		sidebar_right_middle_layout = QVBoxLayout()

		display_checkbox_asset_layout = QGridLayout()

		self.display_modeling_asset_button = QCheckBox("Display modeling")
		self.display_modeling_asset_button.setChecked(True)
		self.display_modeling_asset_button.clicked.connect(self.toggleAssetDisplay)
		self.display_rigging_asset_button = QCheckBox("Display rigging")
		self.display_rigging_asset_button.setChecked(True)
		self.display_rigging_asset_button.clicked.connect(self.toggleAssetDisplay)
		self.display_lookdev_asset_button = QCheckBox("Display lookdev")
		self.display_lookdev_asset_button.setChecked(True)
		self.display_lookdev_asset_button.clicked.connect(self.toggleAssetDisplay)
		self.display_other_asset_button = QCheckBox("Display other")
		self.display_other_asset_button.setChecked(True)
		self.display_other_asset_button.clicked.connect(self.toggleAssetDisplay)
		self.display_checkbox_asset_widget = QWidget()
		self.display_checkbox_asset_widget.setLayout(display_checkbox_asset_layout)

		display_checkbox_asset_layout.addWidget(self.display_modeling_asset_button, 0, 0)
		display_checkbox_asset_layout.addWidget(self.display_rigging_asset_button, 0, 1)
		display_checkbox_asset_layout.addWidget(self.display_lookdev_asset_button, 1, 0)
		display_checkbox_asset_layout.addWidget(self.display_other_asset_button, 1, 1)
		sidebar_right_middle_layout.addWidget(self.display_checkbox_asset_widget)
		
		display_checkbox_shot_layout = QGridLayout()

		self.display_layout_shot_button = QCheckBox("Display layout")
		self.display_layout_shot_button.setChecked(True)
		self.display_layout_shot_button.clicked.connect(self.toggleShotDisplay)
		self.display_blocking_shot_button = QCheckBox("Display blocking")
		self.display_blocking_shot_button.setChecked(True)
		self.display_blocking_shot_button.clicked.connect(self.toggleShotDisplay)
		self.display_splining_shot_button = QCheckBox("Display splining")
		self.display_splining_shot_button.setChecked(True)
		self.display_splining_shot_button.clicked.connect(self.toggleShotDisplay)
		self.display_rendering_shot_button = QCheckBox("Display rendering")
		self.display_rendering_shot_button.setChecked(True)
		self.display_rendering_shot_button.clicked.connect(self.toggleShotDisplay)
		self.display_other_shot_button = QCheckBox("Display other")
		self.display_other_shot_button.setChecked(True)
		self.display_other_shot_button.clicked.connect(self.toggleShotDisplay)
		self.display_checkbox_shot_widget = QWidget()
		self.display_checkbox_shot_widget.setLayout(display_checkbox_shot_layout)
		self.display_checkbox_shot_widget.setVisible(False)

		display_checkbox_shot_layout.addWidget(self.display_layout_shot_button, 0, 0)
		display_checkbox_shot_layout.addWidget(self.display_blocking_shot_button, 0, 1)
		display_checkbox_shot_layout.addWidget(self.display_splining_shot_button, 1, 0)
		display_checkbox_shot_layout.addWidget(self.display_rendering_shot_button, 1, 1)
		display_checkbox_shot_layout.addWidget(self.display_other_shot_button, 2, 1, 1, 2)
		sidebar_right_middle_layout.addWidget(self.display_checkbox_shot_widget)

		sidebar_right_layout.addLayout(sidebar_right_middle_layout)
		
		## // BOTTOM \\ ##
		sidebar_right_bottom_layout = QVBoxLayout()

		self.version_list = QListWidget()
		self.version_list.currentItemChanged.connect(self.versionlistCommand)
		sidebar_right_bottom_layout.addWidget(self.version_list)

		sidebar_right_layout.addLayout(sidebar_right_bottom_layout)

		## Finalize right column layout ##
		sidebar_right_widget.setLayout(sidebar_right_layout)
		sidebar_right_widget.setMaximumWidth(300)
		
		#####################
		## FINALIZE LAYOUT ##
		#####################
		main_layout.addWidget(sidebar_left_widget)
		main_layout.addLayout(center_layout)
		main_layout.addWidget(sidebar_right_widget)

		main_widget.setLayout(main_layout)

		self.setCentralWidget(main_widget)


	def newProjectCommand(self, event = None):
		dialog = NewProjectDialogPySide(self)
		dialog.exec_()
		project = dialog.getData()

		if project:
			self.current_project = Project(project["directory"])

			Resources.writeAtLine("save/options.spi", project["directory"], 1)

			self.add_shot_button.setEnabled(True)
			self.add_asset_button.setEnabled(True)
			self.shots_preview_button.setEnabled(True)
			self.custom_button.setEnabled(True)

			self.setWindowTitle("Super Pipe || " + self.current_project.getDirectory())

			# self.asset_list.configure(selectmode = "browse")

			self.add_asset_action.setEnabled(True)
			self.add_shot_action.setEnabled(True)
			self.project_settings_action.setEnabled(True)
			self.project_statistics_action.setEnabled(False)
			self.clean_backups_action.setEnabled(True)

			self.home_page_title_label.setText("THE PROJECT \"" + self.current_project.getName() + "\" IS SET")

			self.updateShotListView()
			self.updateAssetListView()


	def setProjectCommand(self):
		directory = QFileDialog.getExistingDirectory(caption="Set project")

		self.app.setOverrideCursor(Qt.WaitCursor)

		if directory:
			if path.isdir(directory):
				self.current_project = Project(directory)

				if self.current_project.isValid():

					Resources.writeAtLine("save/options.spi", directory, 1)

					self.add_shot_button.setEnabled(True)
					self.add_asset_button.setEnabled(True)
					self.shots_preview_button.setEnabled(True)
					self.custom_button.setEnabled(True)

					self.setWindowTitle("Super Pipe || " + self.current_project.getDirectory())

					self.add_asset_action.setEnabled(True)
					self.add_shot_action.setEnabled(True)
					self.project_settings_action.setEnabled(True)
					if self.current_project.getShotList():
						self.project_statistics_action.setEnabled(True)
					else:
						self.project_statistics_action.setEnabled(False)
					self.clean_backups_action.setEnabled(True)

					self.home_page_title_label.setText("THE PROJECT \"" + self.current_project.getName() + "\" IS SET")

					self.updateShotListView()
					self.updateAssetListView()
				else:
					self.dialog("Set project", QMessageBox.Warning, "\"" + directory + "\" is not a project folder")
			else:
				self.dialog("Set project", QMessageBox.Warning, "\"" + directory + "\" is not a project folder")

		self.app.restoreOverrideCursor()


	def updateProjectCommand(self):
		directory = filedialog.askdirectory(title = "New project", mustexist  = False)

		self.app.setOverrideCursor(Qt.WaitCursor)

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

		self.app.restoreOverrideCursor()


	def setShotCommand(self):
		shot = self.current_project.getSelection()
		shot.setShot(self.current_project.getResolution())

		self.set_shot_button.setVisible(False)
		self.frame_range_entry.setVisible(True)
		self.set_shot_frame_range_button.setVisible(True)
		self.open_shot_button.setVisible(True)

		self.downgrade_shot_button.setVisible(True)

		self.step_slider.setCurrentStep("Layout")
		self.step_slider.setVisible(True)

		self.upgrade_shot_button.setVisible(True)
		self.done_shot_button.setVisible(True)

		self.updateVersionListView(shot = shot)
		self.version_list.setCurrentRow(0)

		temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.currentItem().text()

		self.toto_file_path_label.setText(temp_path.replace("/", "\\"))

		self.frame_range_entry.delete(0, len(self.frame_range_entry.get()))
		self.frame_range_entry.insert(0, self.current_project.getSelection().getFrameRange())

		self.versionlistCommand()


	def setAssetCommand(self):
		asset = self.current_project.getSelection()
		asset.setAsset()

		self.set_asset_button.setVisible(False)
		self.open_asset_button.setVisible(True)
		self.open_asset_folder_button.setVisible(True)
		self.modeling_done_asset_button.setVisible(True)
		self.rig_done_asset_button.setVisible(True)
		self.lookdev_done_asset_button.setVisible(True)
		self.done_asset_button.setVisible(True)

		self.updateVersionListView(asset = asset)
		self.version_list.setCurrentRow(0)

		self.versionlistCommand()


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
		self.project_statistics_action.setEnabled(True)

		if len(self.current_project.getShotList()) >= 999:
			self.dialog("No more shots", QMessageBox.Warning, "Sorry, Superpipe does not handle more than 999 shots at the moment !")

		else:
			dialog = NewShotDialogPySide(self, self.current_project)
			dialog.exec_()
			sequence = dialog.getData()

			if sequence:
				shot_nb = self.current_project.createShot(sequence["seq"])
				self.updateShotListView()
				self.shot_list.select_set(shot_nb - 1)
				self.shotlistCommand()


	def addAssetCommand(self):
		dialog = NewAssetDialogPySide(self, self.current_project)
		dialog.exec_()
		asset = dialog.getData()

		if asset:
			if self.current_project.createAsset(asset["name"], asset["cat"], asset["software"]):
				self.updateAssetListView()

				created_item = self.asset_list.findItems(asset["name"], Qt.MatchExactly|Qt.MatchRecursive)[0]
				self.asset_list.setCurrentItem(created_item)

				self.assetListCommand()
			else:
				self.dialog("Asset already exists", QMessageBox.Warning, "The asset \"" + asset["name"] + "\" already exists")


	def shotlistCommand(self, event = None):
		if self.shot_list.size() != 0:
			selected_line = self.shot_list.currentRow()
			selected_shot = self.shot_list.currentItem().text()
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

					if event:
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
						self.upgrade_shot_button.setEnabled(True)
						self.downgrade_shot_button.setEnabled(False)
					elif shot.getStep() == "Blocking":
						self.upgrade_shot_button.setEnabled(True)
						self.downgrade_shot_button.setEnabled(True)
					elif shot.getStep() == "Splining":
						self.upgrade_shot_button.setEnabled(True)
						self.downgrade_shot_button.setEnabled(True)
					elif shot.getStep() == "Rendering":
						self.upgrade_shot_button.setEnabled(False)
						self.downgrade_shot_button.setEnabled(True)

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


	def assetListCommand(self):
		if self.current_project:
			selected_asset = self.asset_list.currentItem()
			if selected_asset:
				self.main_home_page_widget.setVisible(False)
				self.main_asset_widget.setVisible(True)
				self.main_shot_widget.setVisible(False)

				self.shot_list.clearSelection()

				categories = ["CHARACTER", "FX", "PROPS", "SET"]

				if selected_asset.childCount() == 0 and selected_asset.text(0) not in categories:
					cur_item = selected_asset
					path_array = []
					is_parent = True

					while is_parent:
						if cur_item.parent():
							cur_item = cur_item.parent()
							path_array.insert(0, cur_item.text(0))
						else:
							is_parent = False

					self.current_project.setSelection(asset_name = selected_asset.text(0), second_path = "/" + "/".join(path_array))
					asset = self.current_project.getSelection()

					if path.isdir(asset.getDirectory()):
						self.asset_label.setText("ASSET " + selected_asset.text(0).upper())
						self.delete_asset_button.setVisible(True)
						self.rename_asset_button.setVisible(True)

						self.priority_asset_label.setVisible(True)
						self.priority_asset_menu.setVisible(True)

						self.updateVersionListView(asset = asset)
						self.version_list.setCurrentRow(0)
						if self.version_list.currentItem():
							self.asset_version_comment_label.setText(self.current_project.getSelection().getComment(self.version_list.currentItem().text()))
						
						self.priority_asset_menu.setCurrentIndex(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 1)))
						self.modeling_done_asset_button.setChecked(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 2)))
						self.rig_done_asset_button.setChecked(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 3)))
						self.lookdev_done_asset_button.setChecked(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 4)))
						self.done_asset_button.setChecked(int(Resources.readLine(asset.getDirectory() + "/superpipe/asset_data.spi", 5)))

						if self.version_mode:
							if asset:
								if asset.isSet():
									self.set_asset_button.setVisible(False)
									self.open_asset_button.setVisible(True)
									self.open_asset_folder_button.setVisible(True)

									selected_version = self.version_list.currentItem()
									if asset.getSoftware() == "maya" or asset.getSoftware() == "blender":
										temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version.text()
									if asset.getSoftware() == "houdini":
										temp_path = self.current_project.getSelection().getDirectory() + "/" + selected_version.text()

									self.file_path_label.setText(temp_path.replace("/", "\\"))

									self.modeling_done_asset_button.setVisible(True)
									self.rig_done_asset_button.setVisible(True)
									self.lookdev_done_asset_button.setVisible(True)
									self.done_asset_button.setVisible(True)

									pict_path = asset.getDirectory() + "/images/screenshots/" + path.splitext(selected_version.text())[0] + ".jpg"

									if path.isfile(pict_path):
										self.asset_pict_widget.setPixmap(QPixmap(pict_path))
										self.asset_pict_widget.setVisible(True)
									else:
										self.asset_pict_widget.setVisible(False)

								else:
									self.set_asset_button.setVisible(True)
									self.open_asset_button.setVisible(False)
									self.open_asset_folder_button.setVisible(False)
									self.file_path_label.setText("")
									self.asset_pict_widget.setVisible(False)
									self.modeling_done_asset_button.setVisible(False)
									self.rig_done_asset_button.setVisible(False)
									self.lookdev_done_asset_button.setVisible(False)
									self.done_asset_button.setVisible(False)

						else:
							dialog("ERROR", QMessageBox.Warning, "The asset \"" + asset.getAssetName() + "\" is not available !")

				else:
					self.asset_label.setText("NO ASSET SELECTED")
					self.file_path_label.setText("")
					self.delete_asset_button.setVisible(False)
					self.rename_asset_button.setVisible(False)
					self.set_asset_button.setVisible(False)
					self.open_asset_button.setVisible(False)
					self.open_asset_folder_button.setVisible(False)
					self.version_list.clear()
					self.asset_pict_widget.setVisible(False)
					self.priority_asset_label.setVisible(False)
					self.priority_asset_menu.setVisible(False)
					self.modeling_done_asset_button.setVisible(False)
					self.rig_done_asset_button.setVisible(False)
					self.lookdev_done_asset_button.setVisible(False)
					self.done_asset_button.setVisible(False)


	def versionlistCommand(self):
		if self.version_list.selectedItems():
			self.open_asset_button.setVisible(True)
			self.open_asset_folder_button.setVisible(True)

			selected_version = self.version_list.currentItem().text()

			if path.isfile(self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version):
				if self.current_project.getSelectionType() == "shot":
					temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version
				elif self.current_project.getSelection().getSoftware() == "maya":
					temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version
				elif self.current_project.getSelection().getSoftware() == "blender":
					temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version
				elif self.current_project.getSelection().getSoftware() == "houdini":
					temp_path = self.current_project.getSelection().getDirectory() + "/" + selected_version
			else:
				temp_path = self.current_project.getSelection().getDirectory() + "/scenes/edits/" + selected_version

			self.file_path_label.setText(temp_path.replace("/", "\\"))

			pict_path = self.current_project.getSelection().getDirectory() + "/images/screenshots/" + path.splitext(selected_version)[0] + ".jpg"

			if self.current_project.getSelectionType() == "shot":
				if self.version_mode:
					self.shot_version_comment_label.setText(self.current_project.getSelection().getComment(selected_version))

					if path.isfile(pict_path):
						self.shot_pict_widget.setPixmap(QPixmap(pict_path))
						self.shot_pict_widget.setVisible(True)
					else:
						self.shot_pict_widget.setVisible(False)

				else:
					shot = self.current_project.getSelection()

					playblast_file = shot.getDirectory() + "/movies/" + selected_version

					# self.playblast_player.updateVideo(playblast_file)

			elif self.current_project.getSelectionType() == "asset":
				self.asset_version_comment_label.setText(self.current_project.getSelection().getComment(selected_version))

				if path.isfile(pict_path):
					self.asset_pict_widget.setPixmap(QPixmap(pict_path))
					self.asset_pict_widget.setVisible(True)
				else:
					self.asset_pict_widget.setVisible(False)


	def openShotCommand(self):
		if self.version_list.size(): 
			selected_line = self.version_list.curselection()[0]
			selected_shot_version = self.version_list.get(selected_line)

			shot = self.current_project.getSelection()

			if self.version_mode:
				if shot.getSoftware() == "maya":
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

				elif shot.getSoftware() == "blender":
					try:
						if path.isfile(shot.getDirectory() + "/scenes/" + selected_shot_version):
							blender_file = shot.getDirectory() + "/scenes/" + selected_shot_version
						else:
							blender_file = shot.getDirectory() + "/scenes/edits/" + selected_shot_version

						subprocess.Popen("%s %s" % (self.blender_path, blender_file))
					except:
						dialog = lambda: OkDialog.OkDialog(self.parent, "Blender path", "Check Blender path in Edit > Preferences")
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
			selected_asset_version = self.version_list.currentItem().text()

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
						if path.isfile(asset.getDirectory() + "/scenes/" + selected_asset_version):
							blender_file = asset.getDirectory() + "/scenes/" + selected_asset_version
						else:
							blender_file = asset.getDirectory() + "/scenes/edits/" + selected_asset_version

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
			self.app.setOverrideCursor(Qt.WaitCursor)
			self.parent.update()

			asset = self.current_project.getSelection()
			asset.renameAsset(asset_name["name"])

			self.current_project.updateAssetList()
			self.updateAssetListView()

			self.asset_list.selection_set(asset_name["name"])
			self.asset_list.focus_set()
			self.asset_list.focus(asset_name["name"])
			self.assetListCommand()

			self.app.restoreOverrideCursor()
		else:
			dialog = lambda: OkDialog.OkDialog(self.parent, "Error", "The asset \"" + asset_name["name"] + "\" already exists !")
			self.wait_window(dialog().top)


	def updateShotListView(self):
		self.shot_list.clear()

		shots = self.current_project.getShotList()

		for shot in shots:
			if path.isdir(self.current_project.getDirectory() + "/05_shot/" + shot[1] + "/superpipe"):
				# self.shot_list.insert(shot[0], shot[1])
				self.shot_list.insertItem(shot[0], shot[1])

				cur_shot = Shot(self.current_project.getDirectory(), shot[1])

				if cur_shot.isDone():
					self.shot_list.itemconfig(shot[0] - 1, bg = self.theme.done_color, selectbackground = self.theme.done_select_color)
				elif cur_shot.getPriority() == "Urgent":
					self.shot_list.itemconfig(shot[0] - 1, bg = self.theme.urgent_color, selectbackground = self.theme.urgent_select_color)
				elif cur_shot.getPriority() == "High":
					self.shot_list.itemconfig(shot[0] - 1, bg = self.theme.high_color, selectbackground = self.theme.high_select_color)
				elif cur_shot.getPriority() == "Medium":
					self.shot_list.itemconfig(shot[0] - 1, bg = self.theme.medium_color, selectbackground = self.theme.medium_select_color)

			else:
				self.dialog("ERROR", QMessageBox.Warning, "The shot " + shot[1] + " has a problem !")


	def updateAssetListView(self):
		for cat in self.categories:
			self.categories[cat].takeChildren()

		assets = self.current_project.getAssetList()

		for asset in assets:
			if asset[0] != "backup":
				if path.isdir(self.current_project.getDirectory() + "/04_asset" + asset[1] + "/" + asset[0] + "/superpipe"):
					cur_asset = Asset(self.current_project.getDirectory(), asset[1], asset[0])

					asset_subfolders = asset[1].strip("/").split("/")
					current_category = self.categories[asset_subfolders[0].lower()]

					for subfolder in asset_subfolders[1:]:
						if not self.asset_list.findItems(subfolder.lower(), Qt.MatchExactly):
							new_item = QTreeWidgetItem([subfolder.lower()])
							current_category.addChild(new_item)
							current_category = new_item

					if self.asset_list.findItems(asset[0], Qt.MatchExactly):
						self.dialog("ERROR", QMessageBox.Warning, "The asset \"" + asset[1].upper() + "/" + asset[0] + "\" already exists !")
					else:
						current_category.addChild(QTreeWidgetItem([asset[0]]))

				else:
					self.dialog("ERROR", QMessageBox.Warning, "The asset \"" + asset[0] + "\" has a problem !")


	def updateVersionListView(self, shot = None, asset = None):
		current_item = self.version_list.currentItem()
		current_item_text = ""
		if current_item:
			current_item_text = current_item.text()

		self.version_list.clear()

		if shot:
			if self.version_mode:
				shot_versions = shot.getVersionsList(self.asset_show_last_only_button.isChecked(), self.display_layout_shot_button.isChecked(), self.display_blocking_shot_button.isChecked(), self.display_splining_shot_button.isChecked(), self.display_rendering_shot_button.isChecked(), self.display_other_shot_button.isChecked())

				if shot_versions:
					for shot_version in shot_versions:
						self.version_list.addItem(shot_version[1])

				self.display_checkbox_asset_widget.setVisible(False)
				self.display_checkbox_shot_widget.setVisible(True)

			else:
				shot_playblasts = shot.getPlayblastsList()

				if shot_playblasts:
					for shot_playblast in shot_playblasts:
						self.version_list.addItem(shot_playblast[1])

		elif asset:
			if self.version_mode:
				asset_versions = asset.getVersionsList(self.asset_show_last_only_button.isChecked(), self.display_modeling_asset_button.isChecked(), self.display_rigging_asset_button.isChecked(), self.display_lookdev_asset_button.isChecked(), self.display_other_asset_button.isChecked())

				if asset_versions:
					for asset_version in asset_versions:
						self.version_list.addItem(asset_version[1])

				self.display_checkbox_shot_widget.setVisible(False)
				self.display_checkbox_asset_widget.setVisible(True)

			else:
				asset_playblasts = asset.getPlayblastsList()

				if asset_playblasts:
					for asset_playblast in asset_playblasts:
						self.version_list.addItem(asset_playblast[1])


		if current_item_text:
			match = self.version_list.findItems(current_item_text, Qt.MatchExactly)
			if match:
				self.version_list.setCurrentItem(match[0])
			else:
				self.version_list.setCurrentRow(0)


	def moveShotUpCommand(self):
		self.app.setOverrideCursor(Qt.WaitCursor)
		self.parent.update()

		loc = self.shot_list.yview()[0]

		self.up_button.setEnabled(False)
		self.down_button.setEnabled(False)

		self.current_project.moveShotUp(self.current_project.getSelection().getShotName())

		new_selection = self.shot_list.curselection()[0] + 1
		self.updateShotListView()
		self.shot_list.select_set(new_selection)

		self.shotlistCommand()

		self.up_button.setEnabled(True)
		self.down_button.setEnabled(True)

		self.shot_list.yview_moveto(loc)

		self.app.restoreOverrideCursor()


	def moveShotDownCommand(self):
		self.app.setOverrideCursor(Qt.WaitCursor)
		self.parent.update()

		loc = self.shot_list.yview()[0]

		self.up_button.setEnabled(False)
		self.down_button.setEnabled(False)

		self.current_project.moveShotDown(self.current_project.getSelection().getShotName())

		new_selection = self.shot_list.curselection()[0] - 1
		self.updateShotListView()
		self.shot_list.select_set(new_selection)

		self.shotlistCommand()

		self.up_button.setEnabled(True)
		self.down_button.setEnabled(True)

		self.shot_list.yview_moveto(loc)

		self.app.restoreOverrideCursor()


	def toggleLastVersions(self):
		if self.current_project.getSelectionType() == "shot":
			self.updateVersionListView(shot = self.current_project.getSelection())
		elif self.current_project.getSelectionType() == "asset":
			if self.asset_list.currentItem().text(0) not in ["CHARACTER", "FX", "PROPS", "SET"]:
				self.updateVersionListView(asset = self.current_project.getSelection())


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
		# selected_asset = self.asset_list.currentItem()
		self.current_project.getSelection().setModelingDone(self.modeling_done_asset_button.isChecked())
		# self.updateAssetListView()
		# self.asset_list.setCurrentItem(selected_asset)
		# self.asset_list.focus_set()
		# self.asset_list.focus(selected_asset)
		# self.asset_list.see(selected_asset)


	def toggleAssetRigDone(self):
		# selected_asset = self.asset_list.currentItem()
		self.current_project.getSelection().setRigDone(self.rig_done_asset_button.isChecked())
		# self.updateAssetListView()
		# self.asset_list.setCurrentItem(selected_asset)
		# self.asset_list.focus_set()
		# self.asset_list.focus(selected_asset)
		# self.asset_list.see(selected_asset)


	def toggleAssetLookdevDone(self):
		# selected_asset = self.asset_list.currentItem()
		self.current_project.getSelection().setLookdevDone(self.lookdev_done_asset_button.isChecked())
		# self.updateAssetListView()
		# self.asset_list.setCurrentItem(selected_asset)
		# self.asset_list.focus_set()
		# self.asset_list.focus(selected_asset)
		# self.asset_list.see(selected_asset)


	def toggleAssetDone(self):
		# selected_asset = self.asset_list.currentItem()
		self.current_project.getSelection().setDone(self.done_asset_button.isChecked())
		# self.updateAssetListView()
		# self.asset_list.setCurrentItem(selected_asset)
		# self.asset_list.focus_set()
		# self.asset_list.focus(selected_asset)
		# self.asset_list.see(selected_asset)


	def priorityShotCommand(self, priority):
		loc = self.shot_list.yview()[0]
		selected_shot = self.shot_list.curselection()[0]
		self.current_project.getSelection().setPriority(priority)
		self.updateShotListView()
		self.shot_list.select_set(selected_shot)
		self.shot_list.yview_moveto(loc)


	def priorityAssetCommand(self):
		# selected_asset = self.asset_list.focus()
		self.current_project.getSelection().setPriority(self.priority_asset_menu.currentIndex())
		self.asset_list.currentItem().setBackground(0, Qt.red)
		# self.updateAssetListView()
		# self.asset_list.selection_set(selected_asset)
		# self.asset_list.focus_set()
		# self.asset_list.focus(selected_asset)


	def shotsPreviewCommand(self):
		self.app.setOverrideCursor(Qt.WaitCursor)
		self.parent.update()

		self.main_area_preview.grid(self.main_area_preview.pi)
		self.main_area_shot.grid_forget()
		self.main_area_asset.grid_forget()
		self.statistics_view.grid_forget()

		self.asset_list.selection_remove(self.asset_list.focus())
		self.shot_list.selection_clear(0, END)

		self.version_list.clear()

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
			shot_preview_caneva = Canvas(self.shots_preview_list, bg = self.theme.main_color, bd = 0, highlightthickness = 0)

			to_edit_pict = PIL.Image.open(img)

			edited_pict = Resources.resizeImage(to_edit_pict, 256)

			pict = ImageTk.PhotoImage(edited_pict)

			self.preview_gifdict[nb] = pict

			shot_preview_label = Label(self.shots_preview_list, text = name, bg = self.theme.main_color, fg = self.theme.text_color)
			shot_preview_label.grid(row = int((nb - 1)/5) * 2, column = (nb - 1) % 5, pady = (10, 5))

			shot_preview_caneva.create_image(0, 0, anchor = N + W, image = pict)
			shot_preview_caneva.config(height = pict.height(), width = pict.width())

			shot_preview_caneva.grid(row = (int((nb - 1)/5) * 2) + 1, column = (nb - 1) % 5, pady = (0, 10))
			shot_preview_caneva.bind("<MouseWheel>", self.wheelScrollCommand)

		self.app.restoreOverrideCursor()


	def upgradeShotCommand(self):
		selected_shot = self.shot_list.curselection()[0]
		if self.current_project.getSelection().upgrade():
			if self.current_project.getSelection().getStep() == "Layout":
				self.downgrade_shot_button.setEnabled(False)
			elif self.current_project.getSelection().getStep() == "Rendering":
				self.upgrade_shot_button.setEnabled(False)

			self.step_slider.nextStep()
			self.customSliderCommand()

			self.shotlistCommand()


	def downgradeShotCommand(self):
		yesno = {"result" : ""}

		dialog = lambda: YesNoDialog.YesNoDialog(self.parent, "Downgrade shot", "Are you sure you want to downgrade the shot \"" + self.current_project.getSelection().getShotName() + "\" ?", (yesno, "result"))
		self.wait_window(dialog().top)

		if yesno["result"] == "yes":
			selected_shot = self.shot_list.curselection()[0]
			self.current_project.getSelection().downgrade()

			if self.current_project.getSelection().getStep() == "Layout":
				self.downgrade_shot_button.setEnabled(False)
			elif self.current_project.getSelection().getStep() == "Rendering":
				self.upgrade_shot_button.setEnabled(False)

			self.step_slider.previousStep()
			self.customSliderCommand()

			self.shotlistCommand()


	def setShotFrameRangeCommand(self):
		self.current_project.getSelection().setFrameRange(int(self.frame_range_entry.get()))


	def openFolderCommand(self):
		subprocess.Popen("%s \"%s\"" % ("explorer", self.current_project.getSelection().getDirectory().replace("/", "\\")))


	def toggleAssetDisplay(self):
		self.updateVersionListView(asset = self.current_project.getSelection())


	def toggleShotDisplay(self):
		self.updateVersionListView(shot = self.current_project.getSelection())


	def toggleVersionsPlayblastsCommand(self):
		self.version_mode = not self.version_mode

		if self.version_mode:
			self.toggle_versions_playblasts_button.setText("Show playblasts")
			self.versions_playblasts_label.setText("Versions")
			self.open_shot_button.setText("Open selected version")
			self.open_asset_button.setText("Open selected version")
			self.playblast_pictures_shot.setVisible(False)
			self.pictures_shot.setVisible(True)
		else:
			self.toggle_versions_playblasts_button.setText("Show versions")
			self.versions_playblasts_label.setText("Playblasts")
			self.open_shot_button.setText("Open selected playblast")
			self.open_asset_button.setText("Open selected playblast")
			self.playblast_pictures_shot.setVisible(True)
			self.pictures_shot.setVisible(False)

		if self.current_project.getSelectionType() == "shot":
			self.updateVersionListView(shot = self.current_project.getSelection())
		elif self.current_project.getSelectionType() == "asset":
			self.updateVersionListView(asset = self.current_project.getSelection())

		self.version_list.setCurrentRow(0)


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


	def customSliderCommand(self, event = None):
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


	def projectStatisticsCommand(self, event = None):
		self.statistics_view.update()
		self.statistics_view.grid(self.statistics_view.pi)
		self.main_area_asset.grid_forget()
		self.main_area_shot.grid_forget()
		self.main_area_preview.grid_forget()


	def preferencesCommand(self, event = None):
		dialog = PreferencesDialogPySide(self)
		dialog.exec_()
		preferences = dialog.getData()

		# if self.current_project:
		# 	if not path.isfile(self.current_project.getDirectory() + "/project_option.spi"):
		# 		with open(self.current_project.getDirectory() + "/project_option.spi", "w") as f:
		# 			f.write("www.google.fr\n")
		# 		f.close()

		# preferences = {"maya_path" : "", "houdini_path" : "", "blender_path" : "", "vlc_path" : "", "default_software" : "", "link" : None, "theme" : ""}

		# if self.current_project:
		# 	dialog = lambda: PreferencesDialog.PreferencesDialog(self.parent, self.current_project.getDirectory() + "/project_option.spi", (preferences, "maya_path", "houdini_path", "blender_path", "vlc_path", "default_software", "link", "theme"))
		# else:
		# 	dialog = lambda: PreferencesDialog.PreferencesDialog(self.parent, "", (preferences, "maya_path", "houdini_path", "blender_path", "vlc_path", "default_software", "link", "theme"))
		# self.wait_window(dialog().top)

		if preferences:
			self.maya_path = preferences["maya_path"]
			self.houdini_path = preferences["houdini_path"]
			self.blender_path = preferences["blender_path"]
			self.vlc_path = preferences["vlc_path"]
			# self.theme = preferences["theme"]

			# self.current_project.default_software = preferences["default_software"]
			# Resources.writeAtLine(self.current_project.getDirectory() + "/project_option.spi", preferences["default_software"], 4)
			# Resources.writeAtLine(self.current_project.getDirectory() + "/project_option.spi", preferences["link"], 1)

			# Resources.writeAtLine("save/options.spi", preferences["theme"], 2)
			Resources.writeAtLine("save/options.spi", preferences["maya_path"], 3)
			Resources.writeAtLine("save/options.spi", preferences["houdini_path"], 4)
			Resources.writeAtLine("save/options.spi", preferences["blender_path"], 5)
			Resources.writeAtLine("save/options.spi", preferences["vlc_path"], 6)


	def about(self):
		dialog = lambda: OkDialog.OkDialog(self.parent, "Credits", "Super Pipe\nPipeline manager\n(C) Lucas Boutrot", padding = 20)
		self.wait_window(dialog().top)


	def refresh(self, event):
		if self.version_list.curselection():
			selected_version = self.version_list.curselection()[0]
			
			if self.current_project.getSelectionType() == "shot":
				self.updateVersionListView(shot = self.current_project.getSelection())
			elif self.current_project.getSelectionType() == "asset":
				self.updateVersionListView(asset = self.current_project.getSelection())

			self.version_list.select_set(selected_version)

			self.versionlistCommand()

	def dialog(self, title, icon, message):
		dialog = QMessageBox()
		dialog.setWindowTitle(title)
		dialog.setIcon(icon)
		dialog.setText(message)
		dialog.exec_()


	def frameRangeReturnClick(self, event):
		self.setShotFrameRangeCommand()
		self.set_shot_frame_range_button.focus_set()


	def scrollCommand(self, event):
		self.preview_canva_scroll.configure(scrollregion = self.preview_canva_scroll.bbox("all"), width = 2000, height = self.parent.winfo_height())


	def wheelScrollCommand(self, event):
		self.preview_canva_scroll.yview_scroll(int(-1 * e.delta/120), "units")


	def exitCommand(self):
		self.parent.destroy()


def main():
	app = QApplication(sys.argv)

	window = SuperPipePyside(app)
	window.showMaximized()

	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
