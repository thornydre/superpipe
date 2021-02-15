#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Main import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt


class NewProjectDialogPySide(QDialog):
	def __init__(self, parent=None):
		super(NewProjectDialogPySide, self).__init__(parent=parent, f=Qt.WindowTitleHint|Qt.WindowSystemMenuHint)

		self.validate = True

		self.setWindowTitle("Superpipe || New project")

		main_layout = QVBoxLayout()

		new_project_label = QLabel("New project")
		main_layout.addWidget(new_project_label)

		directory_layout = QHBoxLayout()
		self.project_directory_textfield = QLineEdit()
		directory_layout.addWidget(self.project_directory_textfield)
		directory_button = QPushButton("Browse")
		directory_button.clicked.connect(self.browseDirectoryCommand)
		directory_layout.addWidget(directory_button)
		main_layout.addLayout(directory_layout)

		project_name_layout = QHBoxLayout()
		project_name_label = QLabel("Project name :")
		project_name_layout.addWidget(project_name_label)
		self.project_name_textfield = QLineEdit()
		project_name_layout.addWidget(self.project_name_textfield)
		main_layout.addLayout(project_name_layout)

		buttons_layout = QHBoxLayout()
		submit_button = QPushButton("Create project")
		submit_button.clicked.connect(self.submitCommand)
		buttons_layout.addWidget(submit_button)
		cancel_button = QPushButton("Cancel")
		cancel_button.clicked.connect(self.cancelCommand)
		buttons_layout.addWidget(cancel_button)
		main_layout.addLayout(buttons_layout)

		self.setLayout(main_layout)

		self.resize(500, 100)


	def browseDirectoryCommand(self):
		directory = QFileDialog.getExistingDirectory(caption="New project")

		self.project_directory_textfield.setText(directory)


	def submitCommand(self, dict_key):
		directory = self.project_directory_textfield.text()
		name = self.project_name_textfield.text()

		if directory and name:
			self.directory = directory + "/" + name
			self.close()


	def cancelCommand(self):
		self.validate = False
		self.close()


	def getData(self):
		if self.validate:
			if self.directory:
				result = {}
				result["directory"] = self.directory
				return result
		return None
