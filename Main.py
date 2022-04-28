#!/usr/bin/python

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QFile, QTextStream
from PySide6.QtGui import *
from Settings import *
from Project import *
from Resources import *
from ListsObserver import *
from os import path, mkdir, listdir
from pathlib import Path
from urllib.parse import urlsplit
from PIL import ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import sys
import PIL
import subprocess
import webbrowser
import threading

from CustomSlider import *
from CustomVideoPlayer import *
# from StatisticsView import *
from NewProjectDialog import *
from NewAssetDialog import *
from NewShotDialog import *
from RenameAssetDialog import *
from ProjectSettingsDialog import *
from PreferencesDialog import *
from AboutDialog import *
from ManageBackupsDialog import *


class SuperPipe(QMainWindow):
# Class: Main class of Superpipe, containing mostly UI
	def __init__(self, app):
		super(SuperPipe, self).__init__()

		self.settings = Settings("assets/settings.spi")
		self.settings.loadGeneralSettings()

		self.app = app

		file = QFile("./assets/themes/" + self.settings.getSetting("theme") + ".css")
		file.open(QFile.ReadOnly|QFile.Text)
		stream = QTextStream(file)
		self.app.setStyleSheet(stream.readAll())

		self.app.setOverrideCursor(Qt.WaitCursor)

		self.project_observer = None

		self.current_project = None
		self.version_mode = True

		self.maya_path = self.settings.getSetting("maya_path")
		self.houdini_path = self.settings.getSetting("houdini_path")
		self.blender_path = self.settings.getSetting("blender_path")
		self.vlc_path = self.settings.getSetting("video_player_path")

		self.initUI()

		project_directory = self.settings.getSetting("project_dir")

		if project_directory:
			if path.isdir(project_directory):
				self.current_project = Project(project_directory)
				
				self.setWindowTitle(f"Super Pipe || {self.current_project.getDirectory()}")
				
				self.add_shot_button.setEnabled(True)
				self.add_asset_button.setEnabled(True)
				self.shots_preview_button.setEnabled(True)
				self.custom_button.setEnabled(True)
				self.toggle_versions_playblasts_button.setEnabled(True)
				self.display_modeling_asset_button.setEnabled(True)
				self.display_rigging_asset_button.setEnabled(True)
				self.display_lookdev_asset_button.setEnabled(True)
				self.display_other_asset_button.setEnabled(True)
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

			self.startObserverThread()

			# self.statistics_view.set(self.current_project)

		self.app.restoreOverrideCursor()


	def initUI(self):
		app_icon = QIcon()
		app_icon.addFile("assets/img/icon16x16.ico", QSize(16,16))
		app_icon.addFile("assets/img/icon24x24.ico", QSize(32,32))
		app_icon.addFile("assets/img/icon32x32.ico", QSize(24,24))
		app_icon.addFile("assets/img/icon48x48.ico", QSize(48,48))
		app_icon.addFile("assets/img/icon256x256.ico", QSize(256,256))
		self.setWindowIcon(app_icon)
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

		refresh_action = QAction("Refresh", self)
		refresh_action.setShortcut("F5")
		refresh_action.triggered.connect(self.refresh)

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
		self.add_asset_action.setEnabled(False)
		self.add_asset_action.triggered.connect(self.addAssetCommand)

		self.add_shot_action = QAction("Add shot", self)
		self.add_shot_action.setShortcut("Ctrl+S")
		self.add_shot_action.setEnabled(False)
		self.add_shot_action.triggered.connect(self.addShotCommand)

		self.project_settings_action = QAction("Project settings", self)
		self.project_settings_action.setEnabled(False)
		self.project_settings_action.triggered.connect(self.projectSettingsCommand)

		self.project_statistics_action = QAction("Project statistics", self)
		self.project_statistics_action.setEnabled(False)
		self.project_statistics_action.triggered.connect(self.projectStatisticsCommand)

		self.clean_backups_action = QAction("Clean backups", self)
		self.clean_backups_action.setEnabled(False)
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
		file_menu.addAction(refresh_action)
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
		self.add_asset_button.setObjectName("important")
		self.add_asset_button.setEnabled(False)
		self.add_asset_button.clicked.connect(self.addAssetCommand)
		self.add_shot_button = QPushButton("Add shot")
		self.add_shot_button.setObjectName("important")
		self.add_shot_button.setEnabled(False)
		self.add_shot_button.clicked.connect(self.addShotCommand)

		sidebar_left_header_layout.addWidget(self.add_asset_button)
		sidebar_left_header_layout.addWidget(self.add_shot_button)

		sidebar_left_layout.addLayout(sidebar_left_header_layout)
 
		## // ASSET PART \\ ##
		sidebar_assets_layout = QVBoxLayout()

		asset_label = QLabel("Assets", alignment=Qt.AlignHCenter)
		self.asset_filter_textfield = QLineEdit()
		self.asset_filter_textfield.setPlaceholderText("Filter")
		self.asset_filter_textfield.textChanged.connect(self.updateAssetListView)
		self.asset_list = QTreeWidget()
		self.asset_list.setHeaderHidden(True)
		self.asset_list.currentItemChanged.connect(self.assetListCommand)
		self.categories = {"character": QTreeWidgetItem(["CHARACTER"]), "fx": QTreeWidgetItem(["FX"]), "props": QTreeWidgetItem(["PROPS"]), "set": QTreeWidgetItem(["SET"])}
		for cat in self.categories:
			self.asset_list.addTopLevelItem(self.categories[cat])

		sidebar_assets_layout.addWidget(asset_label)
		sidebar_assets_layout.addWidget(self.asset_filter_textfield)
		sidebar_assets_layout.addWidget(self.asset_list)

		sidebar_left_layout.addLayout(sidebar_assets_layout)

		## // SHOT PART \\ ##
		sidebar_shots_layout = QVBoxLayout()

		shot_label = QLabel("Shots", alignment=Qt.AlignHCenter)
		self.shot_list = QListWidget()
		self.shot_list.currentItemChanged.connect(self.shotListCommand)

		sidebar_shots_layout.addWidget(shot_label, alignment=Qt.AlignHCenter)
		sidebar_shots_layout.addWidget(self.shot_list)

		sidebar_left_layout.addLayout(sidebar_shots_layout)

		## // FOOTER \\ ##
		sidebar_left_footer_layout = QVBoxLayout()

		self.shots_preview_button = QPushButton("Shots preview")
		self.shots_preview_button.setEnabled(False)
		self.shots_preview_button.clicked.connect(self.shotsPreviewCommand)
		self.custom_button = QPushButton("Custom link")
		self.custom_button.setEnabled(False)
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

		self.home_page_title_label = QLabel("PLEASE SET AN EXISTING PROJECT, OR CREATE A NEW ONE", alignment=Qt.AlignHCenter)
		main_home_page_layout.addWidget(self.home_page_title_label)
		self.main_home_page_widget = QWidget()
		self.main_home_page_widget.setLayout(main_home_page_layout)

		center_layout.addWidget(self.main_home_page_widget)

		## // ASSET PAGE \\ ##
		main_asset_layout = QVBoxLayout()

		## Asset info ##
		asset_info_layout = QHBoxLayout()

		self.asset_label = QLabel("NO ASSET SELECTED")
		self.asset_label.setFixedHeight(50)
		self.delete_asset_button = QPushButton("")
		self.delete_asset_button.setIcon(QIcon(QPixmap("assets/img/red_cross.gif")))
		self.delete_asset_button.setObjectName("icons")
		self.delete_asset_button.clicked.connect(self.deleteAssetCommand)
		self.rename_asset_button = QPushButton("Rename asset")
		self.rename_asset_button.clicked.connect(self.renameAssetCommand)
		self.set_asset_button = QPushButton("Set asset")
		self.set_asset_button.clicked.connect(self.setAssetCommand)
		self.open_asset_folder_button = QPushButton("Open asset folder")
		self.open_asset_folder_button.clicked.connect(self.openFolderCommand)
		self.asset_show_last_only_button = QCheckBox("Show only last versions")
		self.asset_show_last_only_button.clicked.connect(self.toggleLastVersions)

		asset_info_layout.addWidget(self.asset_label)
		asset_info_layout.addWidget(self.delete_asset_button)
		asset_info_layout.addWidget(self.rename_asset_button)
		asset_info_layout.addWidget(self.set_asset_button)
		asset_info_layout.addStretch(1)
		asset_info_layout.addWidget(self.open_asset_folder_button)
		asset_info_layout.addStretch(1)
		asset_info_layout.addWidget(self.asset_show_last_only_button)

		main_asset_layout.addLayout(asset_info_layout)

		## Asset state ##
		asset_state_line_layout = QHBoxLayout()

		self.priority_asset_label = QLabel("Priority :")
		self.priority_asset_label.setFixedHeight(30)
		self.priority_asset_menu = QComboBox()
		self.priority_asset_menu.addItems(["Low", "Medium", "High", "Urgent"])
		self.priority_asset_menu.currentIndexChanged.connect(self.priorityAssetCommand)
		self.modeling_done_asset_button = QCheckBox("Modeling done")
		self.modeling_done_asset_button.setFixedWidth(140)
		self.modeling_done_asset_button.clicked.connect(self.toggleAssetModelingDone)
		self.rig_done_asset_button = QCheckBox("Rig done")
		self.rig_done_asset_button.setFixedWidth(140)
		self.rig_done_asset_button.clicked.connect(self.toggleAssetRigDone)
		self.lookdev_done_asset_button = QCheckBox("Lookdev done")
		self.lookdev_done_asset_button.setFixedWidth(140)
		self.lookdev_done_asset_button.clicked.connect(self.toggleAssetLookdevDone)
		self.done_asset_button = QCheckBox("Asset done")
		self.done_asset_button.setFixedWidth(140)
		self.done_asset_button.clicked.connect(self.toggleAssetDone)

		asset_state_line_layout.addWidget(self.priority_asset_label)
		asset_state_line_layout.addWidget(self.priority_asset_menu)
		asset_state_line_layout.addStretch(1)
		asset_state_line_layout.addWidget(self.modeling_done_asset_button)
		asset_state_line_layout.addWidget(self.rig_done_asset_button)
		asset_state_line_layout.addWidget(self.lookdev_done_asset_button)
		asset_state_line_layout.addWidget(self.done_asset_button)
		asset_state_line_layout.addStretch(1)

		main_asset_layout.addLayout(asset_state_line_layout)

		## Asset pictures ##
		asset_picture_widget = QWidget()
		asset_picture_widget.setProperty("class", "darker")
		asset_picture_layout = QVBoxLayout()

		self.asset_pict_title_label = QLabel("This asset :", alignment=Qt.AlignHCenter)
		self.asset_pict_title_label.setProperty("class", "darker")
		self.asset_pict_widget = QLabel(alignment=Qt.AlignHCenter)
		self.asset_pict_widget.setProperty("class", "darker")

		asset_picture_layout.addWidget(self.asset_pict_title_label)
		asset_picture_layout.addWidget(self.asset_pict_widget)
		asset_picture_layout.addStretch(1)

		asset_picture_widget.setMinimumHeight(350)
		asset_picture_widget.setLayout(asset_picture_layout)

		main_asset_layout.addWidget(asset_picture_widget)

		## Asset version actions ##
		asset_actions_widget = QWidget()
		asset_actions_layout = QHBoxLayout()

		self.open_asset_button = QPushButton("Open selected version")
		self.open_asset_button.setObjectName("important")
		self.open_asset_button.setMaximumWidth(200)
		self.open_asset_button.clicked.connect(self.openAssetCommand)

		asset_actions_layout.addStretch(1)
		asset_actions_layout.addWidget(self.open_asset_button)
		asset_actions_layout.addStretch(1)

		asset_actions_widget.setMinimumHeight(60)
		asset_actions_widget.setLayout(asset_actions_layout)

		main_asset_layout.addWidget(asset_actions_widget)

		## Asset version infos ##
		asset_version_comment_widget = QWidget()
		asset_version_comment_widget.setProperty("class", "darker")
		asset_version_comment_layout = QVBoxLayout()

		self.asset_version_comment_title_label = QLabel("Version comment :")
		self.asset_version_comment_title_label.setProperty("class", "darker")
		self.asset_version_comment_label = QLabel()
		self.asset_version_comment_label.setProperty("class", "darker")

		asset_version_comment_layout.addWidget(self.asset_version_comment_title_label)
		asset_version_comment_layout.addWidget(self.asset_version_comment_label)

		asset_version_comment_widget.setMinimumHeight(80)
		asset_version_comment_widget.setLayout(asset_version_comment_layout)

		main_asset_layout.addWidget(asset_version_comment_widget)

		## Asset version paths ##
		asset_paths_layout = QVBoxLayout()

		self.asset_file_path_label = QLabel()
		self.asset_file_path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

		asset_paths_layout.addWidget(self.asset_file_path_label)

		main_asset_layout.addLayout(asset_paths_layout)

		main_asset_layout.addStretch(1)

		## Finalize asset layout ##
		self.main_asset_widget = QWidget()
		self.main_asset_widget.setLayout(main_asset_layout)
		self.main_asset_widget.setVisible(False)

		center_layout.addWidget(self.main_asset_widget)

		## // SHOT PAGE \\ ##
		main_shot_layout = QVBoxLayout()

		## Shot info ##
		shot_info_layout = QHBoxLayout()

		dir_button_layout = QVBoxLayout()

		self.up_button = QPushButton("")
		self.up_button.setIcon(QIcon(QPixmap("assets/img/arrow_up.gif")))
		self.up_button.setObjectName("icons")
		self.up_button.clicked.connect(self.moveShotUpCommand)
		self.down_button = QPushButton("")
		self.down_button.setIcon(QIcon(QPixmap("assets/img/arrow_down.gif")))
		self.down_button.setObjectName("icons")
		self.down_button.clicked.connect(self.moveShotDownCommand)
		
		dir_button_layout.addWidget(self.up_button)
		dir_button_layout.addWidget(self.down_button)

		shot_info_layout.addLayout(dir_button_layout)

		self.shot_label = QLabel("NO SHOT SELECTED")
		self.shot_label.setFixedHeight(50)
		self.delete_shot_button = QPushButton("")
		self.delete_shot_button.setIcon(QIcon(QPixmap("assets/img/red_cross.gif")))
		self.delete_shot_button.setObjectName("icons")
		self.delete_shot_button.clicked.connect(self.deleteShotCommand)
		self.set_shot_button = QPushButton("Set shot")
		self.set_shot_button.clicked.connect(self.setShotCommand)
		self.frame_range_textfield = QLineEdit()
		self.frame_range_textfield.returnPressed.connect(self.setShotFrameRangeCommand)
		self.set_shot_frame_range_button = QPushButton("Set frame range")
		self.set_shot_frame_range_button.clicked.connect(self.setShotFrameRangeCommand)
		self.open_shot_folder_button = QPushButton("Open shot folder")
		self.open_shot_folder_button.clicked.connect(self.openFolderCommand)
		self.shot_show_last_only_button = QCheckBox("Show only last versions")
		self.shot_show_last_only_button.clicked.connect(self.toggleLastVersions)

		shot_info_layout.addWidget(self.shot_label)
		shot_info_layout.addWidget(self.delete_shot_button)
		shot_info_layout.addWidget(self.set_shot_button)
		shot_info_layout.addWidget(self.frame_range_textfield)
		shot_info_layout.addWidget(self.set_shot_frame_range_button)
		shot_info_layout.addStretch(1)
		shot_info_layout.addWidget(self.open_shot_folder_button)
		shot_info_layout.addStretch(1)
		shot_info_layout.addWidget(self.shot_show_last_only_button)

		main_shot_layout.addLayout(shot_info_layout)

		## Shot description ##
		shot_description_widget = QWidget()
		shot_description_widget.setProperty("class", "darker")
		shot_description_layout = QVBoxLayout()

		self.shot_description_title_label = QLabel("Shot description :")
		self.shot_description_title_label.setProperty("class", "darker")
		self.shot_description_textfield = QLineEdit()
		self.shot_description_textfield.textChanged.connect(self.shotDescriptionCommand)

		shot_description_layout.addWidget(self.shot_description_title_label)
		shot_description_layout.addWidget(self.shot_description_textfield)

		shot_description_widget.setMinimumHeight(80)
		shot_description_widget.setLayout(shot_description_layout)

		main_shot_layout.addWidget(shot_description_widget)

		## Shot state ##
		shot_state_line_layout = QHBoxLayout()

		self.priority_shot_label = QLabel("Priority :")
		self.priority_shot_label.setFixedHeight(30)
		self.priority_shot_menu = QComboBox()
		self.priority_shot_menu.addItems(["Low", "Medium", "High", "Urgent"])
		self.priority_shot_menu.currentIndexChanged.connect(self.priorityShotCommand)
		self.downgrade_shot_button = QPushButton("Downgrade shot")
		self.downgrade_shot_button.clicked.connect(self.downgradeShotCommand)
		self.step_slider = CustomSlider(width=500, height=20, steps=("Layout", "Blocking", "Splining", "Rendering"))
		self.step_slider.released.connect(self.customSliderCommand)
		self.upgrade_shot_button = QPushButton("Upgrade shot")
		self.upgrade_shot_button.clicked.connect(self.upgradeShotCommand)
		self.done_shot_button = QCheckBox("Shot done")
		self.done_shot_button.clicked.connect(self.toggleShotDone)

		shot_state_line_layout.addWidget(self.priority_shot_label)
		shot_state_line_layout.addWidget(self.priority_shot_menu)
		shot_state_line_layout.addStretch(1)
		shot_state_line_layout.addWidget(self.downgrade_shot_button)
		shot_state_line_layout.addWidget(self.step_slider)
		shot_state_line_layout.addWidget(self.upgrade_shot_button)
		shot_state_line_layout.addWidget(self.done_shot_button)
		shot_state_line_layout.addStretch(1)

		main_shot_layout.addLayout(shot_state_line_layout)

		## Shot pictures ##
		self.shot_pictures_widget = QWidget()
		self.shot_pictures_widget.setProperty("class", "darker")
		shot_pictures_layout = QHBoxLayout()

		shot_prev_picture_layout = QVBoxLayout()
		self.shot_prev_pict_label = QLabel("Previous shot :", alignment=Qt.AlignHCenter)
		self.shot_prev_pict_label.setProperty("class", "darker")
		self.shot_prev_pict_widget = QLabel(alignment=Qt.AlignHCenter)
		self.shot_prev_pict_widget.setProperty("class", "darker")
		shot_prev_picture_layout.addWidget(self.shot_prev_pict_label)
		shot_prev_picture_layout.addWidget(self.shot_prev_pict_widget)
		shot_prev_picture_layout.addStretch(1)
		shot_pictures_layout.addLayout(shot_prev_picture_layout)

		shot_current_picture_layout = QVBoxLayout()
		self.shot_pict_label = QLabel("Current shot :", alignment=Qt.AlignHCenter)
		self.shot_pict_label.setProperty("class", "darker")
		self.shot_pict_widget = QLabel(alignment=Qt.AlignHCenter)
		self.shot_pict_widget.setProperty("class", "darker")
		shot_current_picture_layout.addWidget(self.shot_pict_label)
		shot_current_picture_layout.addWidget(self.shot_pict_widget)
		shot_current_picture_layout.addStretch(1)
		shot_pictures_layout.addLayout(shot_current_picture_layout)

		self.shot_pictures_widget.setMinimumHeight(350)
		self.shot_pictures_widget.setLayout(shot_pictures_layout)

		main_shot_layout.addWidget(self.shot_pictures_widget)

		## Shot playblasts ##
		self.shot_playblasts_widget = QWidget()
		shot_playblasts_layout = QHBoxLayout()

		shot_current_playblast_layout = QVBoxLayout()
		self.shot_playblast_label = QLabel("Current playblast :")
		self.playblast_player = CustomVideoPlayer(512, 288)
		shot_current_playblast_layout.addWidget(self.shot_playblast_label)
		shot_current_playblast_layout.addWidget(self.playblast_player)
		shot_current_playblast_layout.addStretch(1)
		shot_playblasts_layout.addLayout(shot_current_playblast_layout)

		self.shot_playblasts_widget.setLayout(shot_playblasts_layout)
		self.shot_playblasts_widget.setVisible(False)

		main_shot_layout.addWidget(self.shot_playblasts_widget)

		## Shot version actions ##
		shot_actions_widget = QWidget()
		shot_actions_layout = QHBoxLayout()

		self.open_shot_button = QPushButton("Open selected version")
		self.open_shot_button.setObjectName("important")
		self.open_shot_button.setMaximumWidth(200)
		self.open_shot_button.clicked.connect(self.openShotCommand)

		shot_actions_layout.addStretch(1)
		shot_actions_layout.addWidget(self.open_shot_button)
		shot_actions_layout.addStretch(1)

		shot_actions_widget.setMinimumHeight(60)
		shot_actions_widget.setLayout(shot_actions_layout)

		main_shot_layout.addWidget(shot_actions_widget)
		
		## Shot version infos ##
		shot_version_comment_widget = QWidget()
		shot_version_comment_widget.setProperty("class", "darker")
		shot_version_comment_layout = QVBoxLayout()

		self.shot_version_comment_title_label = QLabel("Version comment :")
		self.shot_version_comment_title_label.setProperty("class", "darker")
		self.shot_version_comment_label = QLabel()
		self.shot_version_comment_label.setProperty("class", "darker")

		shot_version_comment_layout.addWidget(self.shot_version_comment_title_label)
		shot_version_comment_layout.addWidget(self.shot_version_comment_label)

		shot_version_comment_widget.setMinimumHeight(80)
		shot_version_comment_widget.setLayout(shot_version_comment_layout)

		main_shot_layout.addWidget(shot_version_comment_widget)

		## Shot version paths ##
		shot_paths_layout = QVBoxLayout()

		self.shot_file_path_label = QLabel()
		self.shot_file_path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
		self.shot_abc_path_label = QLabel()
		self.shot_abc_path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

		shot_paths_layout.addWidget(self.shot_file_path_label)
		shot_paths_layout.addWidget(self.shot_abc_path_label)

		main_shot_layout.addLayout(shot_paths_layout)

		main_shot_layout.addStretch(1)

		## Finalize shot layout ##
		self.main_shot_widget = QWidget()
		self.main_shot_widget.setLayout(main_shot_layout)
		self.main_shot_widget.setVisible(False)

		center_layout.addWidget(self.main_shot_widget)

		## // PREVIEW PAGE \\ ##
		self.main_preview_layout = QVBoxLayout()
		preview_scroll_area = QScrollArea()
		preview_scroll_area.setWidgetResizable(True)
		self.preview_scroll_widget = QWidget()
		self.preview_scroll_layout = QGridLayout()

		self.main_preview_layout.addWidget(preview_scroll_area)
		preview_scroll_area.setWidget(self.preview_scroll_widget)
		self.preview_scroll_widget.setLayout(self.preview_scroll_layout)

		## Finalize preview layout ##
		self.main_preview_widget = QWidget()
		self.main_preview_widget.setLayout(self.main_preview_layout)
		self.main_preview_widget.setVisible(False)

		center_layout.addWidget(self.main_preview_widget)

		##################
		## RIGHT COLUMN ##
		##################
		sidebar_right_widget = QWidget()
		sidebar_right_layout = QVBoxLayout()

		## // TOP \\ ##
		sidebar_right_top_layout = QVBoxLayout()
		self.toggle_versions_playblasts_button = QPushButton("Show playblasts")
		self.toggle_versions_playblasts_button.setEnabled(False)
		self.toggle_versions_playblasts_button.clicked.connect(self.toggleVersionsPlayblastsCommand)
		self.versions_playblasts_label = QLabel("Versions", alignment=Qt.AlignHCenter)

		sidebar_right_top_layout.addWidget(self.toggle_versions_playblasts_button)
		sidebar_right_top_layout.addWidget(self.versions_playblasts_label)

		sidebar_right_layout.addLayout(sidebar_right_top_layout)

		## // MIDDLE \\ ##
		sidebar_right_middle_layout = QVBoxLayout()

		display_checkbox_asset_layout = QGridLayout()

		self.display_modeling_asset_button = QCheckBox("Display modeling")
		self.display_modeling_asset_button.setEnabled(False)
		self.display_modeling_asset_button.setChecked(True)
		self.display_modeling_asset_button.clicked.connect(self.toggleAssetDisplay)
		self.display_rigging_asset_button = QCheckBox("Display rigging")
		self.display_rigging_asset_button.setEnabled(False)
		self.display_rigging_asset_button.setChecked(True)
		self.display_rigging_asset_button.clicked.connect(self.toggleAssetDisplay)
		self.display_lookdev_asset_button = QCheckBox("Display lookdev")
		self.display_lookdev_asset_button.setEnabled(False)
		self.display_lookdev_asset_button.setChecked(True)
		self.display_lookdev_asset_button.clicked.connect(self.toggleAssetDisplay)
		self.display_other_asset_button = QCheckBox("Display other")
		self.display_other_asset_button.setEnabled(False)
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
		self.version_list.itemSelectionChanged.connect(self.versionlistCommand)
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


	def newProjectCommand(self):
		dialog = NewProjectDialog(self)
		dialog.exec()
		project = dialog.getData()

		if project:
			self.current_project = Project(project["directory"])
			self.startObserverThread()

			self.settings.setSetting("project_dir", project["directory"])
			self.settings.saveSettings()

			self.add_shot_button.setEnabled(True)
			self.add_asset_button.setEnabled(True)
			self.shots_preview_button.setEnabled(True)
			self.custom_button.setEnabled(True)
			self.toggle_versions_playblasts_button.setEnabled(True)
			self.display_modeling_asset_button.setEnabled(True)
			self.display_rigging_asset_button.setEnabled(True)
			self.display_lookdev_asset_button.setEnabled(True)
			self.display_other_asset_button.setEnabled(True)

			self.setWindowTitle("Super Pipe || " + self.current_project.getDirectory())

			self.add_asset_action.setEnabled(True)
			self.add_shot_action.setEnabled(True)
			self.project_settings_action.setEnabled(True)
			self.project_statistics_action.setEnabled(False)
			self.clean_backups_action.setEnabled(True)

			self.home_page_title_label.setText("THE PROJECT \"" + self.current_project.getName() + "\" IS SET")

			self.updateShotListView()
			self.updateAssetListView()


	def setProjectCommand(self):
		if self.current_project:
			directory = QFileDialog.getExistingDirectory(caption="Set project", dir=self.current_project.getDirectory() + "/..")
		else:
			directory = QFileDialog.getExistingDirectory(caption="Set project")

		self.app.setOverrideCursor(Qt.WaitCursor)

		if directory:
			if path.isdir(directory):
				self.current_project = Project(directory)
				self.startObserverThread()

				if self.current_project.isValid():
					self.settings.setSetting("project_dir", directory)
					self.settings.saveSettings()

					self.add_shot_button.setEnabled(True)
					self.add_asset_button.setEnabled(True)
					self.shots_preview_button.setEnabled(True)
					self.custom_button.setEnabled(True)
					self.toggle_versions_playblasts_button.setEnabled(True)
					self.display_modeling_asset_button.setEnabled(True)
					self.display_rigging_asset_button.setEnabled(True)
					self.display_lookdev_asset_button.setEnabled(True)
					self.display_other_asset_button.setEnabled(True)

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
					self.dialog("Set project", "W", "\"" + directory + "\" is not a project folder")
			else:
				self.dialog("Set project", "W", "\"" + directory + "\" is not a project folder")

		self.app.restoreOverrideCursor()


	def updateProjectCommand(self):
		directory = filedialog.askdirectory(title="New project", mustexist=False)

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

		temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + self.version_list.currentItem().text()

		self.asset_file_path_label.setText(temp_path.replace("/", "\\"))

		self.versionlistCommand()


	def setShotCommand(self):
		shot = self.current_project.getSelection()
		shot.setShot(self.current_project.getResolution())

		self.set_shot_button.setVisible(False)
		self.frame_range_textfield.setVisible(True)
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

		self.shot_file_path_label.setText(temp_path.replace("/", "\\"))

		self.frame_range_textfield.setText(str(self.current_project.getSelection().getFrameRange()))

		self.versionlistCommand()


	def deleteAssetCommand(self):
		selected_asset = self.asset_list.currentItem()

		yesno = self.dialog("Delete asset", "Q", "Delete asset \"" + selected_asset.text(0) + "\" from \"" + selected_asset.parent().text(0).upper() + "\" category ?")

		if yesno:
			cur_item = selected_asset
			path_array = []

			is_parent = True

			while is_parent:
				if cur_item.parent():
					cur_item = cur_item.parent()
					path_array.insert(0, cur_item.text(0))
				else:
					is_parent = False

			self.current_project.removeAsset(selected_asset.text(0), "/" + "/".join(path_array))

			self.updateAssetListView()

			self.clearMainFrame("asset")

			self.updateVersionListView()


	def deleteShotCommand(self):
		selected_shot = self.shot_list.currentItem().text()

		yesno = self.dialog("Delete shot", "Q", "Delete shot \"" + selected_shot + "\" ?")

		if yesno:
			self.current_project.removeShot(selected_shot)

			self.updateShotListView()

			self.clearMainFrame("shot")

			self.updateVersionListView()


	def addAssetCommand(self):
		dialog = NewAssetDialog(self, self.current_project)
		dialog.exec()
		asset = dialog.getData()

		if asset:
			if self.current_project.createAsset(asset["name"], asset["cat"], asset["software"]):
				self.updateAssetListView()

				created_item = self.asset_list.findItems(asset["name"], Qt.MatchExactly|Qt.MatchRecursive)[0]
				self.asset_list.setCurrentItem(created_item)

				self.assetListCommand()
			else:
				self.dialog("Asset already exists", "W", "The asset \"" + asset["name"] + "\" already exists")


	def addShotCommand(self):
		self.project_statistics_action.setEnabled(True)

		if len(self.current_project.getShotList()) >= 999:
			self.dialog("No more shots", "W", "Sorry, Superpipe does not handle more than 999 shots at the moment !")

		else:
			dialog = NewShotDialog(self, self.current_project)
			dialog.exec()
			sequence = dialog.getData()

			if sequence:
				shot_nb = self.current_project.createShot(sequence["seq"])
				self.updateShotListView()
				self.shot_list.setCurrentRow(shot_nb - 1)
				self.shotListCommand()


	def assetListCommand(self):
		self.shot_list.clearSelection()
		if self.current_project:
			selected_asset = self.asset_list.currentItem()

			if selected_asset:
				self.main_home_page_widget.setVisible(False)
				self.main_shot_widget.setVisible(False)
				self.main_preview_widget.setVisible(False)
				self.main_asset_widget.setVisible(True)

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

					self.current_project.setSelection(asset_name=selected_asset.text(0), second_path="/".join(path_array))
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

						self.priority_asset_menu.setCurrentIndex(asset.getPriority())

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

									self.asset_file_path_label.setText(temp_path.replace("/", "\\"))

									self.modeling_done_asset_button.setVisible(True)
									self.rig_done_asset_button.setVisible(True)
									self.lookdev_done_asset_button.setVisible(True)
									self.done_asset_button.setVisible(True)

									self.modeling_done_asset_button.setChecked(asset.getModelingDone())
									self.rig_done_asset_button.setChecked(asset.getRigDone())
									self.lookdev_done_asset_button.setChecked(asset.getLookdevDone())
									self.done_asset_button.setChecked(asset.getDone())

									self.asset_show_last_only_button.setVisible(True)
									self.asset_pict_title_label.setVisible(True)
									self.asset_version_comment_title_label.setVisible(True)
									self.asset_version_comment_label.setVisible(True)

									pict_path = f"{asset.getPictsPath()}/{path.splitext(selected_version.text())[0]}.jpg"

									if path.isfile(pict_path):
										self.asset_pict_widget.setPixmap(QPixmap(pict_path))
										self.asset_pict_widget.setVisible(True)
									else:
										self.asset_pict_widget.setVisible(False)

								else:
									self.set_asset_button.setVisible(True)
									self.open_asset_button.setVisible(False)
									self.open_asset_folder_button.setVisible(False)
									self.asset_file_path_label.setText("")
									self.asset_pict_widget.setVisible(False)
									self.modeling_done_asset_button.setVisible(False)
									self.rig_done_asset_button.setVisible(False)
									self.lookdev_done_asset_button.setVisible(False)
									self.done_asset_button.setVisible(False)
									self.asset_show_last_only_button.setVisible(False)
									self.asset_pict_title_label.setVisible(False)
									self.asset_version_comment_title_label.setVisible(False)
									self.asset_version_comment_label.setVisible(False)

							else:
								self.dialog("ERROR", "W", "The asset \"" + asset.getAssetName() + "\" is not available !")

				else:
					self.asset_label.setText("NO ASSET SELECTED")
					self.asset_file_path_label.setText("")
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
					self.asset_show_last_only_button.setVisible(False)
					self.asset_pict_title_label.setVisible(False)
					self.asset_version_comment_title_label.setVisible(False)
					self.asset_version_comment_label.setVisible(False)


	def shotListCommand(self):
		self.asset_list.clearSelection()
		if self.shot_list.currentItem():
			if self.shot_list.count() != 0:
				self.main_home_page_widget.setVisible(False)
				self.main_asset_widget.setVisible(False)
				self.main_shot_widget.setVisible(True)

				selected_line = self.shot_list.currentRow()
				selected_shot = self.shot_list.currentItem().text()
				self.shot_label.setText(selected_shot.replace("s", "SEQUENCE ").replace("p", " SHOT "))

				if selected_line == 0 and selected_line == self.shot_list.count() - 1:
					self.shot_prev_pict_label.setVisible(True)
					self.shot_prev_pict_widget.setVisible(True)
					self.up_button.setEnabled(False)
					self.down_button.setEnabled(False)
				elif selected_line == 0:
					self.shot_prev_pict_label.setVisible(False)
					self.shot_prev_pict_widget.setVisible(False)
					self.up_button.setEnabled(True)
					self.down_button.setEnabled(False)
				elif selected_line == self.shot_list.count() - 1:
					self.shot_prev_pict_label.setVisible(True)
					self.shot_prev_pict_widget.setVisible(True)
					self.down_button.setEnabled(True)
					self.up_button.setEnabled(False)
				else:
					self.shot_prev_pict_label.setVisible(True)
					self.shot_prev_pict_widget.setVisible(True)
					self.down_button.setEnabled(True)
					self.up_button.setEnabled(True)

				self.main_shot_widget.setVisible(True)
				self.main_asset_widget.setVisible(False)
				self.main_preview_widget.setVisible(False)
				# self.statistics_view.setVisible(False)

				self.delete_shot_button.setVisible(True)

				self.current_project.setSelection(shot_name=selected_shot)
				shot = self.current_project.getSelection()

				if Shot.validShot(shot.getDirectory()):
					self.updateVersionListView(shot=shot)
					self.version_list.setCurrentRow(0)
					if self.version_list.currentItem():
						self.shot_version_comment_label.setText(self.current_project.getSelection().getComment(self.version_list.currentItem().text()))

					self.done_shot_button.setChecked(shot.getDone())
					self.priority_shot_menu.setCurrentIndex(shot.getPriority())

					self.priority_shot_label.setVisible(True)
					self.priority_shot_menu.setVisible(True)
					self.open_shot_folder_button.setVisible(True)

					shot_description = shot.getDescription()
					if shot_description:
						self.shot_description_textfield.setText(shot_description)
					else:
						self.shot_description_textfield.setText("")

					if shot.isSet():
						self.set_shot_button.setVisible(False)
						self.frame_range_textfield.setVisible(True)
						self.set_shot_frame_range_button.setVisible(True)
						self.open_shot_button.setVisible(True)

						self.downgrade_shot_button.setVisible(True)

						self.step_slider.setCurrentStep(shot.getStep())
						if shot.isDone():
							self.step_slider.setPercentage(100)
							self.step_slider.setActive(False)
						else:
							self.step_slider.setActive(True)
							self.step_slider.setPercentage(shot.getPercentage())
						self.step_slider.setVisible(True)

						self.upgrade_shot_button.setVisible(True)
						self.done_shot_button.setVisible(True)

						self.frame_range_textfield.setText(str(self.current_project.getSelection().getFrameRange()))

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

						if self.version_list.currentItem():
							selected_shot_version = self.version_list.currentItem().text()
							if self.current_project.getSelectionType() == "shot":
								temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_shot_version
							elif self.current_project.getSelection().getSoftware() == "maya":
								temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_shot_version
							elif self.current_project.getSelection().getSoftware() == "houdini":
								temp_path = self.current_project.getSelection().getDirectory() + "/" + selected_shot_version

							self.shot_file_path_label.setText(temp_path.replace("/", "\\"))

							temp_path = self.current_project.getSelection().getDirectory() + "/cache/alembic/" + path.splitext(selected_shot_version)[0] + ".abc"

							if not path.isfile(temp_path):
								temp_path = ""

							self.shot_abc_path_label.setText(temp_path.replace("/", "\\"))

							if self.version_mode:
								pict_path = shot.getDirectory() + "/images/screenshots/" + path.splitext(selected_shot_version)[0] + ".jpg"

								if path.isfile(pict_path):
									self.shot_pict_widget.setPixmap(QPixmap(pict_path))
									self.shot_pict_widget.setVisible(True)

								else:
									self.shot_pict_widget.setVisible(False)

							else:
								playblast_file = shot.getDirectory() + "/movies/" + selected_shot_version

								self.playblast_player.updateVideo(playblast_file)

					else:
						self.set_shot_button.setVisible(True)
						self.frame_range_textfield.setVisible(False)
						self.set_shot_frame_range_button.setVisible(False)
						self.open_shot_button.setVisible(False)

						self.downgrade_shot_button.setVisible(False)

						self.step_slider.setVisible(False)

						self.upgrade_shot_button.setVisible(False)
						self.done_shot_button.setVisible(False)

						self.shot_pict_widget.setVisible(False)

						self.shot_file_path_label.setText("")
						self.shot_abc_path_label.setText("")

					prev_pict_path = ""

					prev_shot_nb = shot.getShotNb() - 1

					if prev_shot_nb > 0:
						for shot_dir in listdir(self.current_project.getDirectory() + "/05_shot/"):
							if re.match(r"s[0-9][0-9]p[0-9][0-9][0-9]", shot_dir):
								if int(shot_dir[-2:]) == prev_shot_nb:
									all_picts_path = self.current_project.getDirectory() + "/05_shot/" + shot_dir + "/images/screenshots/"

									if Shot.validShot(self.current_project.getDirectory() + "/05_shot/" + shot_dir):
										if path.isdir(all_picts_path):
											all_picts_path_array = []

											for f in listdir(all_picts_path):
												if ".jpg" in f:
													all_picts_path_array.append(all_picts_path + f)

											if all_picts_path_array:
												prev_pict_path = max(all_picts_path_array, key=path.getmtime)

										else:
											mkdir(all_picts_path)

					if path.isfile(prev_pict_path):
						self.shot_prev_pict_widget.setPixmap(QPixmap(prev_pict_path))
						self.shot_prev_pict_widget.setVisible(True)
					else:
						self.shot_prev_pict_widget.setVisible(False)

				else:
					self.dialog("Error", "E", "The shot \"" + shot.getShotName() + "\" is not available !")


	def versionlistCommand(self):
		if self.version_list.selectedItems():
			self.open_asset_button.setVisible(True)
			self.open_asset_folder_button.setVisible(True)

			selected_version = self.version_list.currentItem().text()

			temp_path = self.current_project.getSelection().getDirectory() + "/scenes/edits/" + selected_version

			if path.isfile(self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version):
				if self.current_project.getSelectionType() == "shot":
					temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version
				elif self.current_project.getSelection().getSoftware() == "maya":
					temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version
				elif self.current_project.getSelection().getSoftware() == "blender":
					temp_path = self.current_project.getSelection().getDirectory() + "/scenes/" + selected_version
				elif self.current_project.getSelection().getSoftware() == "houdini":
					temp_path = f"{self.current_project.getSelection().getDirectory()}/{selected_version}"

			self.asset_file_path_label.setText(temp_path.replace("/", "\\"))

			pict_path = f"{self.current_project.getSelection().getPictsPath()}/{path.splitext(selected_version)[0]}.jpg"

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

					self.playblast_player.updateVideo(playblast_file)

			elif self.current_project.getSelectionType() == "asset":
				self.asset_version_comment_label.setText(self.current_project.getSelection().getComment(selected_version))

				if path.isfile(pict_path):
					self.asset_pict_widget.setPixmap(QPixmap(pict_path))
					self.asset_pict_widget.setVisible(True)
				else:
					self.asset_pict_widget.setVisible(False)


	def openAssetCommand(self):
		if self.version_list.size(): 
			selected_asset_version = self.version_list.currentItem().text()

			asset = self.current_project.getSelection()

			if self.version_mode:
				if asset.getSoftware() == "maya":
					try:
						maya_file = asset.getDirectory() + "/scenes/edits/" + selected_asset_version
						
						if path.isfile(asset.getDirectory() + "/scenes/" + selected_asset_version):
							maya_file = asset.getDirectory() + "/scenes/" + selected_asset_version

						maya_args = [self.maya_path, "-file", maya_file, "-proj", asset.getDirectory()]
						subprocess.Popen(maya_args)
					except:
						self.dialog("Maya path", "E", "Check Maya path in Edit > Preferences")

				elif asset.getSoftware() == "houdini":
					try:
						houdini_file = asset.getDirectory() + "/backup/" + selected_asset_version

						if path.isfile(asset.getDirectory() + "/" + selected_asset_version):
							houdini_file = asset.getDirectory() + "/" + selected_asset_version

						subprocess.Popen("%s %s" % (self.houdini_path, houdini_file))
					except:
						self.dialog("Houdini path", "E", "Check Houdini path in Edit > Preferences")

				elif asset.getSoftware() == "blender":
					try:
						blender_file = asset.getDirectory() + "/scenes/edits/" + selected_asset_version
						
						if path.isfile(asset.getDirectory() + "/scenes/" + selected_asset_version):
							blender_file = asset.getDirectory() + "/scenes/" + selected_asset_version

						subprocess.Popen("%s %s" % (self.blender_path, blender_file))
					except:
						self.dialog("Blender path", "E", "Check Blender path in Edit > Preferences")
			else:
				try:
					playblast_file = asset.getDirectory() + "/movies/" + selected_asset_version
					subprocess.Popen("%s %s" % (self.vlc_path, playblast_file.replace("/", "\\")))
				except:
					self.dialog("VLC path", "E", "Check VLC path in Edit > Preferences")


	def openShotCommand(self):
		if self.version_list.size():
			selected_shot_version = self.version_list.currentItem().text()

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
						self.dialog("Maya path", "E", "Check Maya path in Edit > Preferences")

				elif shot.getSoftware() == "blender":
					try:
						if path.isfile(shot.getDirectory() + "/scenes/" + selected_shot_version):
							blender_file = shot.getDirectory() + "/scenes/" + selected_shot_version
						else:
							blender_file = shot.getDirectory() + "/scenes/edits/" + selected_shot_version

						subprocess.Popen("%s %s" % (self.blender_path, blender_file))
					except:
						self.dialog("Blender path", "E", "Check Blender path in Edit > Preferences")
			else:
				try:
					playblast_file = shot.getDirectory() + "/movies/" + selected_shot_version
					subprocess.Popen("%s %s" % (self.vlc_path, playblast_file.replace("/", "\\")))
				except:
					self.dialog("VLC path", "E", "Check VLC path in Edit > Preferences")


	def renameAssetCommand(self):
		dialog = RenameAssetDialog(self)
		dialog.exec()
		settings = dialog.getData()

		valid_name = True

		if settings["name"]:
			if settings["name"] == "superpipe":
				valid_name = False
			else:
				if self.current_project.getAssetList().get(settings["name"]):
					valid_name = False

		if valid_name:
			self.app.setOverrideCursor(Qt.WaitCursor)

			asset = self.current_project.getSelection()
			asset.renameAsset(settings["name"])

			self.current_project.updateAssetList()
			self.updateAssetListView()

			renamed_item = self.asset_list.findItems(settings["name"], Qt.MatchExactly|Qt.MatchRecursive)[0]
			self.asset_list.setCurrentItem(renamed_item)

			self.assetListCommand()

			self.app.restoreOverrideCursor()
		else:
			self.dialog("Error", "E", "The asset \"" + settings["name"] + "\" already exists")


	def updateAssetListView(self):
		if self.asset_list.currentItem():
			print("1 : ", self.asset_list.currentItem().text(0))
		if self.asset_filter_textfield.text():
			self.asset_filter_textfield.setStyleSheet("QLineEdit{color: #ffffff;}")
		else:
			self.asset_filter_textfield.setStyleSheet("QLineEdit{color: #888888;}")

		if self.asset_list.currentItem():
			print("2 : ", self.asset_list.currentItem().text(0))
		for cat in self.categories:
			self.categories[cat].takeChildren()

		if self.current_project:
			if self.asset_list.currentItem():
				print("3 : ", self.asset_list.currentItem().text(0))
			assets = self.current_project.filterAssetList(self.asset_filter_textfield.text())

			if self.asset_list.currentItem():
				print("4 : ", self.asset_list.currentItem().text(0))
			for asset in assets:
				if path.isdir(f"{self.current_project.getDirectory()}/04_asset/{asset.getSecondPath()}/{asset.getAssetName()}/superpipe"):
					asset_subfolders = asset.getSecondPath().parts
					current_category = self.categories[asset_subfolders[0].lower()]

					for subfolder in asset_subfolders[1:]:
						if not self.asset_list.findItems(subfolder.upper(), Qt.MatchExactly|Qt.MatchRecursive):
							new_item = QTreeWidgetItem([subfolder.upper()])
							current_category.addChild(new_item)
							current_category = new_item
						else:
							current_category = self.asset_list.findItems(subfolder.upper(), Qt.MatchExactly|Qt.MatchRecursive)[0]

					if self.asset_list.findItems(asset.getAssetName(), Qt.MatchExactly|Qt.MatchRecursive):
						self.dialog("ERROR", "W", "The asset \"" + asset.getSecondPath().upper() + "/" + asset.getAssetName() + "\" already exists !")
					else:
						item = QTreeWidgetItem([asset.getAssetName()])
						priority = asset.getPriority()

						if asset.getDone():
							item.setBackground(0, QBrush(QColor(137, 193, 127)))
						elif priority == 0:
							item.setBackground(0, QBrush())
						elif priority == 1:
							item.setBackground(0, QBrush(QColor(244, 226, 85)))
						elif priority == 2:
							item.setBackground(0, QBrush(QColor(239, 180, 98)))
						elif priority == 3:
							item.setBackground(0, QBrush(QColor(229, 82, 82)))

						current_category.addChild(item)

				else:
					self.dialog("ERROR", "W", "The asset \"" + asset.getAssetName() + "\" has a problem !")
		if self.asset_list.currentItem():
			print("5 : ", self.asset_list.currentItem().text(0))


	def updateShotListView(self):
		self.shot_list.clear()

		shots = self.current_project.getShotList()

		for shot_name in sorted(shots):
			shot = shots[shot_name]
			if path.isdir(f"{self.current_project.getDirectory()}/05_shot/{shot.getShotName()}/superpipe"):
				item = QListWidgetItem(shot.getShotName())
				self.shot_list.insertItem(shot.getShotNb(), item)

				priority = shot.getPriority()

				if shot.isDone():
					item.setBackground(QBrush(QColor(137, 193, 127)))
				elif priority == 1:
					item.setBackground(QBrush(QColor(244, 226, 85)))
				elif priority == 2:
					item.setBackground(QBrush(QColor(239, 180, 98)))
				elif priority == 3:
					item.setBackground(QBrush(QColor(229, 82, 82)))

			else:
				self.dialog("ERROR", "W", "The shot " + shot.getShotName() + " has a problem !")


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

		self.up_button.setEnabled(False)
		self.down_button.setEnabled(False)

		self.current_project.moveShotUp(self.current_project.getSelection().getShotName())

		new_selection = self.shot_list.currentRow() + 1
		self.updateShotListView()
		self.shot_list.setCurrentRow(new_selection)

		self.app.restoreOverrideCursor()


	def moveShotDownCommand(self):
		self.app.setOverrideCursor(Qt.WaitCursor)

		self.up_button.setEnabled(False)
		self.down_button.setEnabled(False)

		self.current_project.moveShotDown(self.current_project.getSelection().getShotName())

		new_selection = self.shot_list.currentRow() - 1
		self.updateShotListView()
		self.shot_list.setCurrentRow(new_selection)

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
		selected_asset = self.asset_list.currentItem()
		self.current_project.getSelection().setModelingDone(self.modeling_done_asset_button.isChecked())
		self.updateAssetListView()
		item = self.asset_list.findItems(selected_asset.text(0), Qt.MatchExactly|Qt.MatchRecursive)[0]
		self.asset_list.setCurrentItem(item)


	def toggleAssetRigDone(self):
		selected_asset = self.asset_list.currentItem()
		self.current_project.getSelection().setRigDone(self.rig_done_asset_button.isChecked())
		self.updateAssetListView()
		item = self.asset_list.findItems(selected_asset.text(0), Qt.MatchExactly|Qt.MatchRecursive)[0]
		self.asset_list.setCurrentItem(item)


	def toggleAssetLookdevDone(self):
		selected_asset = self.asset_list.currentItem()
		self.current_project.getSelection().setLookdevDone(self.lookdev_done_asset_button.isChecked())
		self.updateAssetListView()
		item = self.asset_list.findItems(selected_asset.text(0), Qt.MatchExactly|Qt.MatchRecursive)[0]
		self.asset_list.setCurrentItem(item)


	def toggleAssetDone(self):
		selected_asset = self.asset_list.currentItem()
		self.current_project.getSelection().setDone(self.done_asset_button.isChecked())
		self.priorityAssetCommand()
		self.updateAssetListView()
		item = self.asset_list.findItems(selected_asset.text(0), Qt.MatchExactly|Qt.MatchRecursive)[0]
		self.asset_list.setCurrentItem(item)


	def priorityAssetCommand(self):
		priority = self.priority_asset_menu.currentIndex()

		self.current_project.getSelection().setPriority(priority)
		if self.current_project.getSelection().getDone():
			self.asset_list.currentItem().setBackground(0, QBrush(QColor(137, 193, 127)))
		elif priority == 0:
			self.asset_list.currentItem().setBackground(0, QBrush())
		elif priority == 1:
			self.asset_list.currentItem().setBackground(0, QBrush(QColor(244, 226, 85)))
		elif priority == 2:
			self.asset_list.currentItem().setBackground(0, QBrush(QColor(239, 180, 98)))
		elif priority == 3:
			self.asset_list.currentItem().setBackground(0, QBrush(QColor(229, 82, 82)))


	def priorityShotCommand(self, priority):
		priority = self.priority_shot_menu.currentIndex()

		self.current_project.getSelection().setPriority(priority)
		if self.current_project.getSelection().getDone():
			self.shot_list.currentItem().setBackground(QBrush(QColor(137, 193, 127)))
		elif priority == 0:
			self.shot_list.currentItem().setBackground(QBrush())
		elif priority == 1:
			self.shot_list.currentItem().setBackground(QBrush(QColor(244, 226, 85)))
		elif priority == 2:
			self.shot_list.currentItem().setBackground(QBrush(QColor(239, 180, 98)))
		elif priority == 3:
			self.shot_list.currentItem().setBackground(QBrush(QColor(229, 82, 82)))


	def shotsPreviewCommand(self):
		self.app.setOverrideCursor(Qt.WaitCursor)

		self.main_home_page_widget.setVisible(False)
		self.main_preview_widget.setVisible(True)
		self.main_shot_widget.setVisible(False)
		self.main_asset_widget.setVisible(False)

		self.shot_list.clearSelection()
		self.asset_list.clearSelection()
		self.version_list.clearSelection()

		all_shots_preview = []

		i = 0
		for shot in self.current_project.getShotList().values():
			all_picts_path = shot.getPictsPath()

			all_picts_path_array = []

			for f in listdir(all_picts_path):
				if path.splitext(f)[1] == ".jpg" or path.splitext(f)[1] == ".gif":
					all_picts_path_array.append(all_picts_path + f)

			img = "assets/img/img_not_available.jpg"
			if all_picts_path_array:
				img = max(all_picts_path_array, key=path.getmtime)

			shot_name_widget = QLabel(shot.getShotName(), alignment=Qt.AlignHCenter)
			shot_preview_widget = QLabel(alignment=Qt.AlignHCenter)
			preview_pixmap = QPixmap(img)
			shot_preview_widget.setPixmap(preview_pixmap.scaledToWidth(230))

			self.preview_scroll_layout.addWidget(shot_name_widget, int(i/5) * 2, i % 5)
			self.preview_scroll_layout.addWidget(shot_preview_widget, int(i/5) * 2, i % 5)
			i += 1

		self.app.restoreOverrideCursor()


	def upgradeShotCommand(self):
		if self.current_project.getSelection().upgrade():
			if self.current_project.getSelection().getStep() == "Layout":
				self.downgrade_shot_button.setEnabled(False)
			elif self.current_project.getSelection().getStep() == "Rendering":
				self.upgrade_shot_button.setEnabled(False)

			self.step_slider.nextStep()
			self.customSliderCommand()

			self.shotListCommand()


	def downgradeShotCommand(self):
		yesno = self.dialog("Downgrade shot", "Q", "Are you sure you want to downgrade the shot \"" + self.current_project.getSelection().getShotName() + "\" ?")

		if yesno:
			self.current_project.getSelection().downgrade()

			if self.current_project.getSelection().getStep() == "Layout":
				self.downgrade_shot_button.setEnabled(False)
			elif self.current_project.getSelection().getStep() == "Rendering":
				self.upgrade_shot_button.setEnabled(False)

			self.step_slider.previousStep()
			self.customSliderCommand()

			self.shotListCommand()


	def setShotFrameRangeCommand(self):
		self.current_project.getSelection().setFrameRange(int(self.frame_range_textfield.text()))


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
			self.shot_playblasts_widget.setVisible(False)
			self.shot_pictures_widget.setVisible(True)
		else:
			self.toggle_versions_playblasts_button.setText("Show versions")
			self.versions_playblasts_label.setText("Playblasts")
			self.open_shot_button.setText("Open selected playblast")
			self.open_asset_button.setText("Open selected playblast")
			self.shot_playblasts_widget.setVisible(True)
			self.shot_pictures_widget.setVisible(False)

		if self.current_project.getSelectionType() == "shot":
			self.updateVersionListView(shot = self.current_project.getSelection())
		elif self.current_project.getSelectionType() == "asset":
			self.updateVersionListView(asset = self.current_project.getSelection())

		self.version_list.setCurrentRow(0)


	def shotDescriptionCommand(self):
		self.current_project.getSelection().setDescription(self.shot_description_textfield.text())


	def customSliderCommand(self):
		self.current_project.getSelection().setPercentage(self.step_slider.getPercentage())


	def customButtonCommand(self):
		base_url = self.current_project.getCustomLink()

		if base_url:
			webbrowser.open(base_url)


	def clearMainFrame(self, area_type):
		if area_type == "asset":
			self.asset_label.setText("NO ASSET SELECTED")
			self.delete_asset_button.setVisible(False)
			self.rename_asset_button.setVisible(False)
			self.set_asset_button.setVisible(False)
			self.asset_file_path_label.setText("")
			self.asset_pict_widget.setVisible(False)
			self.open_asset_button.setVisible(False)
			self.open_asset_folder_button.setVisible(False)
			self.priority_asset_menu.setVisible(False)
			self.priority_asset_label.setVisible(False)
			self.modeling_done_asset_button.setVisible(False)
			self.rig_done_asset_button.setVisible(False)
			self.lookdev_done_asset_button.setVisible(False)
			self.done_asset_button.setVisible(False)
		elif area_type == "shot":
			self.shot_label.setText("NO SHOT SELECTED")
			self.up_button.setVisible(False)
			self.down_button.setVisible(False)
			self.delete_shot_button.setVisible(False)
			self.set_shot_button.setVisible(False)
			self.shot_file_path_label.setText("")
			self.shot_pictures_widget.setVisible(False)
			self.open_shot_button.setVisible(False)
			self.open_shot_folder_button.setVisible(False)
			self.priority_shot_menu.setVisible(False)
			self.priority_shot_label.setVisible(False)
			self.downgrade_shot_button.setVisible(False)
			self.step_slider.setVisible(False)
			self.upgrade_shot_button.setVisible(False)
			self.done_shot_button.setVisible(False)


	def cleanBackupsCommand(self):
		dialog = ManageBackupsDialog(self, self.current_project)
		dialog.exec()


	def projectSettingsCommand(self):
		dialog = ProjectSettingsDialog(self, self.current_project)
		dialog.exec()
		settings = dialog.getData()

		if settings:
			self.current_project.setResolution(settings["res"])
			self.current_project.setDefaultSoftware(settings["software"])
			self.current_project.setCustomLink(settings["custom_link"])


	def projectStatisticsCommand(self):
		self.statistics_view.update()
		self.statistics_view.grid(self.statistics_view.pi)
		self.main_area_asset.grid_forget()
		self.main_area_shot.grid_forget()
		self.main_area_preview.grid_forget()


	def preferencesCommand(self):
		dialog = PreferencesDialog(self)
		dialog.exec()
		preferences = dialog.getData()

		if preferences:
			self.maya_path = preferences["maya_path"]
			self.houdini_path = preferences["houdini_path"]
			self.blender_path = preferences["blender_path"]
			self.vlc_path = preferences["vlc_path"]

			self.settings.setSetting("maya_path", preferences["maya_path"])
			self.settings.setSetting("houdini_path", preferences["houdini_path"])
			self.settings.setSetting("blender_path", preferences["blender_path"])
			self.settings.setSetting("video_player_path", preferences["vlc_path"])
			self.settings.setSetting("theme", preferences["theme"])
			self.settings.saveSettings()

			file = QFile("./assets/themes/" + preferences["theme"] + ".css")
			file.open(QFile.ReadOnly|QFile.Text)
			stream = QTextStream(file)
			self.app.setStyleSheet(stream.readAll())


	def about(self):
		dialog = AboutDialog(self)
		dialog.exec()


	def refresh(self, event):
		selection_type = self.current_project.getSelectionType()
		# selected_item = None

		# if selection_type == "asset":
		# 	selected_item = self.asset_list.currentItem().text(0)
		# elif selection_type == "shot":
		# 	selected_item = self.shot_list.currentItem().text()

		# self.updateAssetListView()
		# self.updateShotListView()

		# if selected_item:
		# 	if selection_type == "asset":
		# 		item = self.asset_list.findItems(selected_item, Qt.MatchExactly|Qt.MatchRecursive)[0]
		# 		self.asset_list.setCurrentItem(item)
		# 	elif selection_type == "shot":
		# 		item = self.shot_list.findItems(selected_item, Qt.MatchExactly)[0]
		# 		self.shot_list.setCurrentItem(item)

		if self.version_list.currentItem():
			if selection_type == "asset":
				self.updateVersionListView(asset=self.current_project.getSelection())
			elif selection_type == "shot":
				self.updateVersionListView(shot=self.current_project.getSelection())

		self.versionlistCommand()


	def startObserverThread(self):
		if self.project_observer:
			self.project_observer.stop()
			self.project_observer.join()

		observer_thread = threading.Thread(target=self.runObserver, args=())
		observer_thread.daemon = True
		observer_thread.start()


	def runObserver(self):
		self.current_project.getDirectory()

		my_event_handler = FileSystemEventHandler()
		my_event_handler.on_created = self.refresh
		my_event_handler.on_deleted = self.refresh
		my_event_handler.on_moved = self.refresh

		self.project_observer = Observer()
		self.project_observer.schedule(my_event_handler, self.current_project.getDirectory(), recursive=True)

		self.project_observer.start()

		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			self.project_observer.stop()
			self.project_observer.join()


	def dialog(self, title, purpose, message):
		dialog = QMessageBox()
		dialog.setWindowTitle(title)
		if purpose == "Q":
			res = dialog.question(self, title, message)
			return res == dialog.Yes
		elif purpose == "W":
			dialog.warning(self, title, message)
		elif purpose == "E":
			dialog.critical(self, title, message)

		return None


	def closeEvent(self, event):
		self.deleteLater()
		if self.project_observer:
			self.project_observer.stop()
			self.project_observer.join()


def main():
	app = QApplication(sys.argv)

	window = SuperPipe(app)
	window.showMaximized()

	sys.exit(app.exec())

if __name__ == "__main__":
	main()
