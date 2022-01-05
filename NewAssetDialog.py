#!/usr/bin/python

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from Resources import *
from os import path
from Asset import *


class NewAssetDialog(QDialog):
# Class: Creates a window with options to create a new asset
	def __init__(self, parent=None, project=None):
		super(NewAssetDialog, self).__init__(parent=parent, f=Qt.WindowTitleHint|Qt.WindowSystemMenuHint)

		# flags = Qt.WindowFlags
		# help_flag = Qt.WindowContextHelpButtonHint
		# flags = flags & (~help_flag)
		# self.setWindowFlags(flags)

		self.validate = True

		self.setWindowTitle("Super Pipe || Add asset")

		main_layout = QVBoxLayout()

		software_label = QLabel("Select asset software :")
		main_layout.addWidget(software_label)

		software_layout = QGridLayout()
		self.software_button_group = QButtonGroup()
		self.softwares_list = ("maya", "houdini", "blender")
		i = 0

		for software in self.softwares_list:
			software_radiobutton = QRadioButton(software)
			software_layout.addWidget(software_radiobutton, int(i/2), i % 2)
			self.software_button_group.addButton(software_radiobutton)

			if software == project.getDefaultSoftware():
				software_radiobutton.setChecked(True)

			i += 1

		main_layout.addLayout(software_layout)

		category_label = QLabel("Select asset category :")
		main_layout.addWidget(category_label)

		self.categories_list = QTreeWidget()
		self.categories_list.setHeaderHidden(True)
		self.categories = {"character":QTreeWidgetItem(["CHARACTER"]), "fx":QTreeWidgetItem(["FX"]), "props":QTreeWidgetItem(["PROPS"]), "set":QTreeWidgetItem(["SET"])}
		for cat in self.categories:
			self.categories_list.addTopLevelItem(self.categories[cat])

		assets = project.getAssetList()

		for asset in assets.values():
			if asset.getAssetName() != "backup":
				if path.isdir(project.getDirectory() + "/04_asset/" + asset.getSecondPath() + "/" + asset.getAssetName() + "/superpipe"):
					asset_subfolders = asset.getSecondPath().strip("/").split("/")
					current_category = self.categories[asset_subfolders[0].lower()]

					for subfolder in asset_subfolders[1:]:
						if not self.categories_list.findItems(subfolder.upper(), Qt.MatchFixedString|Qt.MatchRecursive):
							new_item = QTreeWidgetItem([subfolder.upper()])
							current_category.addChild(new_item)
							current_category = new_item
						else:
							current_category = self.categories_list.findItems(subfolder.upper(), Qt.MatchFixedString|Qt.MatchRecursive)[0]
				else:
					dialog = QMessageBox()
					dialog.setWindowTitle("ERROR")
					dialog.setIcon(QMessageBox.Warning)
					dialog.setText("The asset \"" + asset.getAssetName() + "\" has a problem !")
					dialog.exec_()

		main_layout.addWidget(self.categories_list)

		asset_name_layout = QHBoxLayout()
		asset_name_label = QLabel("Asset name :")
		asset_name_layout.addWidget(asset_name_label)
		self.asset_name_textfield = QLineEdit()
		asset_name_layout.addWidget(self.asset_name_textfield)
		main_layout.addLayout(asset_name_layout)

		buttons_layout = QHBoxLayout()
		submit_button = QPushButton("Create asset")
		submit_button.setObjectName("important")
		submit_button.clicked.connect(self.submitCommand)
		buttons_layout.addWidget(submit_button)
		cancel_button = QPushButton("Cancel")
		cancel_button.clicked.connect(self.cancelCommand)
		buttons_layout.addWidget(cancel_button)
		main_layout.addLayout(buttons_layout)

		self.setLayout(main_layout)


	def submitCommand(self):
		# method: Submit, validate the data and close the window
		parent = self.categories_list.currentItem()
		category_list = []
		
		while parent:
			category_list.insert(0, parent.text(0))
			parent = parent.parent()

		self.category = "/" + "/".join(category_list)

		self.name = self.asset_name_textfield.text()
		self.name = Resources.normString(self.name)
		self.software = self.software_button_group.checkedButton().text()

		if category_list and self.name:
			self.close()


	def cancelCommand(self):
		# method: Close the window and set the validate flag to False
		self.validate = False
		self.close()


	def getData(self):
		# method: Query the data that has previously been submitted
		if self.validate:
			if self.name and self.category and self.software:
				result = {}
				result["name"] = self.name
				result["cat"] = self.category
				result["software"] = self.software
				return result
		return None
