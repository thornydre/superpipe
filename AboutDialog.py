#!/usr/bin/python

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from Resources import *


class AboutDialog(QDialog):
	def __init__(self, parent=None):
		super(AboutDialog, self).__init__(parent=parent, f=Qt.WindowTitleHint|Qt.WindowSystemMenuHint)

		version = 2.1

		self.setWindowTitle("Super Pipe || About")

		main_layout = QVBoxLayout()

		text = QLabel("Superpipe v" + str(version) + "\nPipeline manager\n(C) Lucas Boutrot")
		text.setAlignment(Qt.AlignCenter)
		main_layout.addWidget(text)

		button = QPushButton("OK")
		button.clicked.connect(self.submitCommand)
		f = QFont("Arial", 10)
		text.setFont(f)
		main_layout.addWidget(button)
	
		self.setLayout(main_layout)

		self.resize(250, 150)


	def submitCommand(self, dict_key):
		self.close()
