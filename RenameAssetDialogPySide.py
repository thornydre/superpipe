#!/usr/bin/python

from Main import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from Resources import *
from os import path

class RenameAssetDialogPySide(QDialog):
	def __init__(self, parent=None):
		super(RenameAssetDialogPySide, self).__init__(parent=parent, f=Qt.WindowTitleHint|Qt.WindowSystemMenuHint)

		self.validate = True

		self.setWindowTitle("Super Pipe || Rename asset")

		main_layout = QVBoxLayout()

		asset_name_layout = QHBoxLayout()
		asset_name_label = QLabel("New asset name :")
		asset_name_layout.addWidget(asset_name_label)
		self.asset_name_textfield = QLineEdit()
		asset_name_layout.addWidget(self.asset_name_textfield)
		main_layout.addLayout(asset_name_layout)

		buttons_layout = QHBoxLayout()
		submit_button = QPushButton("Rename asset")
		submit_button.setObjectName("important")
		submit_button.clicked.connect(self.submitCommand)
		buttons_layout.addWidget(submit_button)
		cancel_button = QPushButton("Cancel")
		cancel_button.clicked.connect(self.cancelCommand)
		buttons_layout.addWidget(cancel_button)
		main_layout.addLayout(buttons_layout)

		self.setLayout(main_layout)


	def submitCommand(self):
		self.name = self.asset_name_textfield.text()
		self.name = Resources.normString(self.name)

		if self.name:
			self.close()


	def cancelCommand(self):
		self.validate = False
		self.close()


	def getData(self):
		if self.validate:
			if self.name:
				result = {}
				result["name"] = self.name
				return result
		return None
