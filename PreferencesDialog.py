#!/usr/bin/python

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from Resources import *
from os import listdir, path
from Settings import *


class PreferencesDialog(QDialog):
	def __init__(self, parent=None):
		super(PreferencesDialog, self).__init__(parent=parent, f=Qt.WindowTitleHint|Qt.WindowSystemMenuHint)

		self.validate = True

		settings = Settings("assets/settings.spi")
		settings.loadGeneralSettings()

		self.setWindowTitle("Super Pipe || Preferences")
		
		main_layout = QVBoxLayout()

		tab_widget = QTabWidget()

		softwares_widget = QWidget()
		softwares_layout = QVBoxLayout()

		maya_label = QLabel("Path to Maya :")
		softwares_layout.addWidget(maya_label)

		maya_layout = QHBoxLayout()
		self.maya_path_textfield = QLineEdit()
		self.maya_path_textfield.setText(settings.getSetting("maya_path"))
		maya_layout.addWidget(self.maya_path_textfield)
		maya_button = QPushButton("Browse")
		maya_button.clicked.connect(self.mayaPathCommand)
		maya_layout.addWidget(maya_button)
		softwares_layout.addLayout(maya_layout)

		houdini_label = QLabel("Path to Houdini :")
		softwares_layout.addWidget(houdini_label)

		houdini_layout = QHBoxLayout()
		self.houdini_path_textfield = QLineEdit()
		self.houdini_path_textfield.setText(settings.getSetting("houdini_path"))
		houdini_layout.addWidget(self.houdini_path_textfield)
		houdini_button = QPushButton("Browse")
		houdini_button.clicked.connect(self.houdiniPathCommand)
		houdini_layout.addWidget(houdini_button)
		softwares_layout.addLayout(houdini_layout)

		blender_label = QLabel("Path to Blender :")
		softwares_layout.addWidget(blender_label)

		blender_layout = QHBoxLayout()
		self.blender_path_textfield = QLineEdit()
		self.blender_path_textfield.setText(settings.getSetting("blender_path"))
		blender_layout.addWidget(self.blender_path_textfield)
		blender_button = QPushButton("Browse")
		blender_button.clicked.connect(self.blenderPathCommand)
		blender_layout.addWidget(blender_button)
		softwares_layout.addLayout(blender_layout)

		vlc_label = QLabel("Path to VLC :")
		softwares_layout.addWidget(vlc_label)

		vlc_layout = QHBoxLayout()
		self.vlc_path_textfield = QLineEdit()
		self.vlc_path_textfield.setText(settings.getSetting("video_player_path"))
		vlc_layout.addWidget(self.vlc_path_textfield)
		vlc_button = QPushButton("Browse")
		vlc_button.clicked.connect(self.vlcPathCommand)
		vlc_layout.addWidget(vlc_button)
		softwares_layout.addLayout(vlc_layout)

		softwares_widget.setLayout(softwares_layout)

		tab_widget.addTab(softwares_widget, "Softwares")

		themes_widget = QWidget()
		themes_layout = QVBoxLayout()

		themes_list = sorted(listdir("assets/themes/"))

		current_theme = settings.getSetting("theme")

		self.radio_buttons = []

		for theme in themes_list:
			theme_name = path.splitext(theme)[0]

			radio_button = QRadioButton(theme_name)
			self.radio_buttons.append(radio_button)
			themes_layout.addWidget(radio_button)

			if current_theme == theme_name:
				radio_button.setChecked(True)

		themes_widget.setLayout(themes_layout)

		tab_widget.addTab(themes_widget, "Themes")

		main_layout.addWidget(tab_widget)

		buttons_layout = QHBoxLayout()
		submit_button = QPushButton("Save")
		submit_button.setObjectName("important")
		submit_button.clicked.connect(self.submitCommand)
		buttons_layout.addWidget(submit_button)
		cancel_button = QPushButton("Cancel")
		cancel_button.clicked.connect(self.cancelCommand)
		buttons_layout.addWidget(cancel_button)
		main_layout.addLayout(buttons_layout)

		self.setLayout(main_layout)

		self.resize(600, 100)


	def mayaPathCommand(self):
		maya_path = QFileDialog.getOpenFileName(caption="Select Maya.exe", dir=self.maya_path_textfield.text(), filter="Maya (*maya*.exe)")[0]

		if maya_path:
			self.maya_path_textfield.setText(maya_path)


	def houdiniPathCommand(self):
		houdini_path = QFileDialog.getOpenFileName(caption="Select Houdini.exe", dir=self.houdini_path_textfield.text(), filter="Houdini (*Houdini*.exe)")[0]

		if houdini_path:
			self.houdini_path_textfield.setText(houdini_path)


	def blenderPathCommand(self):
		blender_path = QFileDialog.getOpenFileName(caption="Select Blender.exe", dir=self.blender_path_textfield.text(), filter="Blender (*Blender*.exe)")[0]

		if blender_path:
			self.blender_path_textfield.setText(blender_path)


	def vlcPathCommand(self):
		vlc_path = QFileDialog.getOpenFileName(caption="Select vlc.exe", dir=self.vlc_path_textfield.text(), filter="VLC (*vlc*.exe)")[0]

		if vlc_path:
			self.vlc_path_textfield.setText(vlc_path)


	def cancelCommand(self):
		self.validate = False
		self.close()


	def submitCommand(self, dict_key):
		self.maya_path = self.maya_path_textfield.text()
		self.houdini_path = self.houdini_path_textfield.text()
		self.blender_path = self.blender_path_textfield.text()
		self.vlc_path = self.vlc_path_textfield.text()
		for radio_button in self.radio_buttons:
			if radio_button.isChecked():
				self.theme = radio_button.text()
		if self.maya_path and self.houdini_path and self.blender_path and self.vlc_path and self.theme:
			self.close()


	def getData(self):
		if self.validate:
			if self.maya_path and self.houdini_path and self.blender_path and self.vlc_path and self.theme:
				result = {}
				result["maya_path"] = self.maya_path
				result["houdini_path"] = self.houdini_path
				result["blender_path"] = self.blender_path
				result["vlc_path"] = self.vlc_path
				result["theme"] = self.theme
				return result
		return None
