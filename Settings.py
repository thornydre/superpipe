#!/usr/bin/python

from Resources import *
from os import path
import json


class Settings:
	def __init__(self, settings_file):
		self.settings = {}
		self.settings_file = settings_file


	def setSetting(self, setting, value):
		self.settings[setting] = value


	def getSetting(self, setting):
		return self.settings.get(setting)


	def saveSettings(self):
		with open(self.settings_file, "w") as file:
			json.dump(self.settings, file)
		file.close()


	def loadGeneralSettings(self):
		if not path.isfile(self.settings_file):
			self.settings = {"project_dir": "", "theme": "dark", "maya_path": "C:/Program Files/Autodesk/Maya2022/bin/maya.exe", "houdini_path": "C:/Program Files/Houdini/houdini.exe", "blender_path": "C:/Program Files/Blender/blender.exe", "video_player_path": "C:/Program Files/VLC/vlc.exe"}
			self.saveSettings()
		else:
			with open(self.settings_file, "r") as file:
				self.settings = json.load(file)
			file.close()


	def loadProjectSettings(self):
		if not path.isfile(self.settings_file):
			self.settings = {"custom_link": "", "res_x": 1920, "res_y": 1080, "sequence_number": 1, "default_software": "maya"}
			self.saveSettings()
		else:
			with open(self.settings_file, "r") as file:
				self.settings = json.load(file)
			file.close()


	def loadAssetSettings(self):
		if not path.isfile(self.settings_file):
			self.settings = {"priority": 0, "modeling_done": False, "rig_done": False, "lookdev_done": False, "done": False, "software": "maya"}
			self.saveSettings()
		else:
			with open(self.settings_file, "r") as file:
				self.settings = json.load(file)
			file.close()


	def loadShotSettings(self):
		if not path.isfile(self.settings_file):
			self.settings = {"priority": 0, "step": "Layout", "percentage": 0, "done": False, "frame_range": 200, "description": "", "software": "maya"}
			self.saveSettings()
		else:
			with open(self.settings_file, "r") as file:
				self.settings = json.load(file)
			file.close()


	def loadVersionSettings(self):
		if not path.isfile(self.settings_file):
			self.settings = {}
			self.saveSettings()
		else:
			with open(self.settings_file, "r") as file:
				self.settings = json.load(file)
			file.close()