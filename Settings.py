#!/usr/bin/python

from Resources import *
from os import path
import json


class Settings:
	def __init__(self):
		self.loadSettings()


	def setSetting(self, setting, value):
		self.settings[setting] = str(value)


	def getSetting(self, setting):
		return self.settings[setting]


	def saveSettings(self):
		with open("assets/settings.spi", "w") as file:
			json.dump(self.settings, file)


	def loadSettings(self):
		if not path.isfile("assets/settings.spi"):
			self.settings = {"project_dir": "","theme": "dark", "maya_path": "C:/Program Files/Autodesk/Maya2022/bin/maya.exe", "houdini_path": "C:/Program Files/Houdini/houdini.exe", "blender_path": "C:/Program Files/Blender/blender.exe", "video_player_path": "C:/Program Files/VLC/vlc.exe"}
			self.saveSettings()
		else:
			with open("assets/settings.spi", "r") as file:
				self.settings = json.load(file)