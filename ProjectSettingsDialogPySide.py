#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Main import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from Resources import *
from os import listdir

import Theme

class ProjectSettingsDialogPySide(QDialog):
	def __init__(self, parent=None, project=None):
		super(ProjectSettingsDialogPySide, self).__init__(parent=parent, f=Qt.WindowTitleHint|Qt.WindowSystemMenuHint)

		self.project = project
		project_options_path = self.project.getDirectory() + "/project_option.spi"

		self.validate = True

		self.setWindowTitle("Super Pipe || Project settings")

		main_layout = QVBoxLayout()

		software_label = QLabel("Default software :")
		main_layout.addWidget(software_label)

		software_layout = QGridLayout()
		self.software_button_group = QButtonGroup()
		self.softwares_list = ("maya", "houdini", "blender")
		i = 0

		default_software = "maya"

		if project_options_path:
			default_software = Resources.readLine(project_options_path, 4)

		for software in self.softwares_list:
			software_radiobutton = QRadioButton(software)
			software_layout.addWidget(software_radiobutton, int(i/3), i % 3)
			self.software_button_group.addButton(software_radiobutton)

			if software == self.project.getDefaultSoftware():
				software_radiobutton.setChecked(True)

			i += 1

		main_layout.addLayout(software_layout)
		
		resolution_label = QLabel("Default shots resolution :")
		main_layout.addWidget(resolution_label)

		res_str = Resources.readLine(self.project.getDirectory() + "/project_option.spi", 2)

		if res_str:
			res = res_str.split("x")
		else:
			res = (0, 0)

		resolution_layout = QHBoxLayout()
		x_label = QLabel("x :")
		resolution_layout.addWidget(x_label)
		self.x_textfield = QLineEdit()
		self.x_textfield.setText(res[0])
		self.x_textfield.setValidator(QIntValidator(0, 9999))
		resolution_layout.addWidget(self.x_textfield)
		y_label = QLabel("y :")
		resolution_layout.addWidget(y_label)
		self.y_textfield = QLineEdit()
		self.y_textfield.setText(res[1])
		self.y_textfield.setValidator(QIntValidator(0, 9999))
		resolution_layout.addWidget(self.y_textfield)
		apply_res_button = QPushButton("Apply to all shots")
		apply_res_button.clicked.connect(self.applyResToAllCommand)
		resolution_layout.addWidget(apply_res_button)
		main_layout.addLayout(resolution_layout)

		custom_link_label = QLabel("Edit custom link :")
		main_layout.addWidget(custom_link_label)

		self.custom_link_textfield = QLineEdit()
		self.custom_link_textfield.setText(self.project.getCustomLink())
		main_layout.addWidget(self.custom_link_textfield)

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


	def applyResToAllCommand(self):
		self.project.setResolution((self.res_x_entry.get(), self.res_y_entry.get()))
		self.project.setAllShotsRes()


	def cancelCommand(self):
		self.validate = False
		self.close()


	def submitCommand(self):
		self.res_x = self.x_textfield.text()
		self.res_y = self.y_textfield.text()
		self.software = self.software_button_group.checkedButton().text()
		self.custom_link = self.custom_link_textfield.text()

		if self.res_x and self.res_y and self.software:
			self.close()


	def getData(self):
		if self.validate:
			if self.res_x and self.res_y and self.software and self.custom_link:
				result = {}
				result["res"] = (self.res_x, self.res_y)
				result["software"] = self.software
				result["custom_link"] = self.custom_link
				return result
		return None
