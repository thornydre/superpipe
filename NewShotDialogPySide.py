#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Main import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from Resources import *
from os import path


class NewShotDialogPySide(QDialog):
	def __init__(self, parent=None, project=None):
		super(NewShotDialogPySide, self).__init__(parent=parent, f=Qt.WindowTitleHint|Qt.WindowSystemMenuHint)

		# flags = Qt.WindowFlags
		# help_flag = Qt.WindowContextHelpButtonHint
		# flags = flags & (~help_flag)
		# self.setWindowFlags(flags)

		self.validate = True
		self.project = project

		self.setWindowTitle("Super Pipe || Add shot")

		main_layout = QVBoxLayout()

		sequence_label = QLabel("Select a sequence")
		main_layout.addWidget(sequence_label)

		self.sequence_list = QListWidget()
		for sequence in range(self.project.getSequenceNumber()):
			self.sequence_list.addItem("Sequence " + str(sequence + 1))
		self.sequence_list.setCurrentRow(self.project.getSequenceNumber() - 1)
		main_layout.addWidget(self.sequence_list)

		buttons_layout = QHBoxLayout()
		submit_button = QPushButton("Create shot")
		submit_button.clicked.connect(self.submitCommand)
		buttons_layout.addWidget(submit_button)
		sequence_button = QPushButton("Create sequence")
		sequence_button.clicked.connect(self.addSequenceCommand)
		buttons_layout.addWidget(sequence_button)
		cancel_button = QPushButton("Cancel")
		cancel_button.clicked.connect(self.cancelCommand)
		buttons_layout.addWidget(cancel_button)
		main_layout.addLayout(buttons_layout)

		self.setLayout(main_layout)


	def submitCommand(self):
		self.sequence = self.sequence_list.currentRow() + 1

		if self.sequence:
			self.close()


	def addSequenceCommand(self):
		self.project.addSequence()

		self.sequence_list.addItem("Sequence " + str(self.project.getSequenceNumber()))
		self.sequence_list.setCurrentRow(self.project.getSequenceNumber() - 1)


	def cancelCommand(self):
		self.validate = False
		self.close()


	def getData(self):
		if self.validate:
			if self.sequence:
				result = {}
				result["seq"] = self.sequence
				return result
		return None
