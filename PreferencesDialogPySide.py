#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Main import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from Resources import *
from os import listdir, path


class PreferencesDialogPySide(QDialog):
	def __init__(self, parent=None):
		super(PreferencesDialogPySide, self).__init__(parent=parent, f=Qt.WindowTitleHint|Qt.WindowSystemMenuHint)

		self.validate = True

		self.setWindowTitle("Super Pipe || Preferences")

		main_layout = QVBoxLayout()

		# software_label = QLabel("Default software")
		# main_layout.addWidget(software_label)

		# software_layout = QHBoxLayout()
		# self.software_button_group = QButtonGroup()
		# self.softwares_list = ("maya", "houdini", "blender")
		# i = 0

		# default_software = "maya"

		# if project_options_path:
		# 	default_software = Resources.readLine(project_options_path, 4)

		# for software in self.softwares_list:
		# 	software_radiobutton = QRadioButton(software)
		# 	software_layout.addWidget(software_radiobutton, int(i/2), i % 2)
		# 	self.software_button_group.addButton(software_radiobutton)

		# 	if software == project.default_software:
		# 		software_radiobutton.setChecked(True)

		# 	i += 1

		# main_layout.addLayout(software_layout)

		maya_label = QLabel("Path to Maya")
		main_layout.addWidget(maya_label)

		maya_layout = QHBoxLayout()
		self.maya_path_textfield = QLineEdit()
		self.maya_path_textfield.setText(Resources.readLine("save/options.spi", 3))
		maya_layout.addWidget(self.maya_path_textfield)
		maya_button = QPushButton("Browse")
		maya_button.clicked.connect(self.mayaPathCommand)
		maya_layout.addWidget(maya_button)
		main_layout.addLayout(maya_layout)

		houdini_label = QLabel("Path to Houdini")
		main_layout.addWidget(houdini_label)

		houdini_layout = QHBoxLayout()
		self.houdini_path_textfield = QLineEdit()
		self.houdini_path_textfield.setText(Resources.readLine("save/options.spi", 4))
		houdini_layout.addWidget(self.houdini_path_textfield)
		houdini_button = QPushButton("Browse")
		houdini_button.clicked.connect(self.houdiniPathCommand)
		houdini_layout.addWidget(houdini_button)
		main_layout.addLayout(houdini_layout)

		blender_label = QLabel("Path to Blender")
		main_layout.addWidget(blender_label)

		blender_layout = QHBoxLayout()
		self.blender_path_textfield = QLineEdit()
		self.blender_path_textfield.setText(Resources.readLine("save/options.spi", 5))
		blender_layout.addWidget(self.blender_path_textfield)
		blender_button = QPushButton("Browse")
		blender_button.clicked.connect(self.blenderPathCommand)
		blender_layout.addWidget(blender_button)
		main_layout.addLayout(blender_layout)

		vlc_label = QLabel("Path to VLC")
		main_layout.addWidget(vlc_label)

		vlc_layout = QHBoxLayout()
		self.vlc_path_textfield = QLineEdit()
		self.vlc_path_textfield.setText(Resources.readLine("save/options.spi", 6))
		vlc_layout.addWidget(self.vlc_path_textfield)
		vlc_button = QPushButton("Browse")
		vlc_button.clicked.connect(self.vlcPathCommand)
		vlc_layout.addWidget(vlc_button)
		main_layout.addLayout(vlc_layout)

		buttons_layout = QHBoxLayout()
		submit_button = QPushButton("Save")
		submit_button.clicked.connect(self.submitCommand)
		buttons_layout.addWidget(submit_button)
		cancel_button = QPushButton("Cancel")
		cancel_button.clicked.connect(self.cancelCommand)
		buttons_layout.addWidget(cancel_button)
		main_layout.addLayout(buttons_layout)

		# custom_link_label = QLabel("Edit custom link")
		# main_layout.addWidget(custom_link_label)

		# self.custom_link_textfield = QLineEdit()
		# self.custom_link_textfield.setText(Resources.readLine("save/options.spi", 1))
		# main_layout.addWidget(self.custom_link_textfield)

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
		maya_path = self.maya_path_textfield.text()
		houdini_path = self.houdini_path_textfield.text()
		blender_path = self.blender_path_textfield.text()
		vlc_path = self.vlc_path_textfield.text()
		# theme = path.splitext(self.themes_list[self.rb_theme.get()])[0]
		if maya_path and houdini_path and blender_path and vlc_path:
			self.maya_path = maya_path
			self.houdini_path = houdini_path
			self.blender_path = blender_path
			self.vlc_path = vlc_path
			self.close()


	def getData(self):
		if self.validate:
			if self.maya_path and self.houdini_path and self.blender_path and self.vlc_path:
				result = {}
				result["maya_path"] = self.maya_path
				result["houdini_path"] = self.houdini_path
				result["blender_path"] = self.blender_path
				result["vlc_path"] = self.vlc_path
				return result
		return None
