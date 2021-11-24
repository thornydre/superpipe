#!/usr/bin/python

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from Resources import *
from os import listdir

class ManageBackupsDialog(QDialog):
	def __init__(self, parent=None, project=None):
		super(ManageBackupsDialog, self).__init__(parent=parent, f=Qt.WindowTitleHint|Qt.WindowSystemMenuHint)

		self.setWindowTitle("Super Pipe || Clean backups")

		self.project = project

		main_layout = QVBoxLayout()

		self.backup_list = QTreeWidget()
		self.backup_list.setHeaderHidden(True)
		self.backup_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.categories = {"shots":QTreeWidgetItem(["SHOTS"]), "character":QTreeWidgetItem(["CHARACTER"]), "fx":QTreeWidgetItem(["FX"]), "props":QTreeWidgetItem(["PROPS"]), "set":QTreeWidgetItem(["SET"])}
		for cat in self.categories:
			self.backup_list.addTopLevelItem(self.categories[cat])

		for folder in listdir(self.project.getDirectory() + "/05_shot/backup/"):
			self.categories["shots"].addChild(QTreeWidgetItem([folder]))

		for folder in listdir(self.project.getDirectory() + "/04_asset/character/backup/"):
			self.categories["character"].addChild(QTreeWidgetItem([folder]))

		for folder in listdir(self.project.getDirectory() + "/04_asset/FX/backup/"):
			self.categories["fx"].addChild(QTreeWidgetItem([folder]))

		for folder in listdir(self.project.getDirectory() + "/04_asset/props/backup/"):
			self.categories["props"].addChild(QTreeWidgetItem([folder]))

		for folder in listdir(self.project.getDirectory() + "/04_asset/set/backup/"):
			self.categories["set"].addChild(QTreeWidgetItem([folder]))

		main_layout.addWidget(self.backup_list)

		buttons_layout = QHBoxLayout()
		submit_button = QPushButton("Delete")
		submit_button.setObjectName("important")
		submit_button.clicked.connect(self.submitCommand)
		buttons_layout.addWidget(submit_button)
		cancel_button = QPushButton("Cancel")
		cancel_button.clicked.connect(self.cancelCommand)
		buttons_layout.addWidget(cancel_button)
		main_layout.addLayout(buttons_layout)

		self.setLayout(main_layout)


	def submitCommand(self):
		for backup_item in self.backup_list.selectedItems():
			if backup_item not in self.categories:
				parent_item = backup_item.parent()
				if parent_item:
					if parent_item.text(0) == "SHOTS":
						rmtree(self.project.getDirectory() + "/05_shot/backup/" + backup_item.text(0))
					else:
						rmtree(self.project.getDirectory() + "/04_asset/" + backup_item.parent().text(0) + "/backup/" + backup_item.text(0))
		self.close()


	def cancelCommand(self):
		self.close()
