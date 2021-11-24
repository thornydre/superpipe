#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Main import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from Resources import *
from os import listdir, path


class PreferencesDialogPySide(QDialog):
	def __init__(self, parent=None,):
		super(PreferencesDialogPySide, self).__init__(parent=parent, f=Qt.WindowTitleHint|Qt.WindowSystemMenuHint)

		self.validate = True

		self.setWindowTitle("Super Pipe || Preferences")

		main_layout = QVBoxLayout()

		maya_label = QLabel("Path to Maya :")
		main_layout.addWidget(maya_label)

		maya_layout = QHBoxLayout()
		self.maya_path_textfield = QLineEdit()
		self.maya_path_textfield.setText(Resources.readLine("save/options.spi", 3))
		maya_layout.addWidget(self.maya_path_textfield)
		maya_button = QPushButton("Browse")
		maya_button.clicked.connect(self.mayaPathCommand)
		maya_layout.addWidget(maya_button)
		main_layout.addLayout(maya_layout)

		houdini_label = QLabel("Path to Houdini :")
		main_layout.addWidget(houdini_label)

		houdini_layout = QHBoxLayout()
		self.houdini_path_textfield = QLineEdit()
		self.houdini_path_textfield.setText(Resources.readLine("save/options.spi", 4))
		houdini_layout.addWidget(self.houdini_path_textfield)
		houdini_button = QPushButton("Browse")
		houdini_button.clicked.connect(self.houdiniPathCommand)
		houdini_layout.addWidget(houdini_button)
		main_layout.addLayout(houdini_layout)

		blender_label = QLabel("Path to Blender :")
		main_layout.addWidget(blender_label)

		blender_layout = QHBoxLayout()
		self.blender_path_textfield = QLineEdit()
		self.blender_path_textfield.setText(Resources.readLine("save/options.spi", 5))
		blender_layout.addWidget(self.blender_path_textfield)
		blender_button = QPushButton("Browse")
		blender_button.clicked.connect(self.blenderPathCommand)
		blender_layout.addWidget(blender_button)
		main_layout.addLayout(blender_layout)

		vlc_label = QLabel("Path to VLC :")
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
		# theme = path.splitext(self.themes_list[self.rb_theme.get()])[0]
		if self.maya_path and self.houdini_path and self.blender_path and self.vlc_path:
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
