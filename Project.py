#!/usr/bin/python

from os import makedirs, listdir, path, rename, walk
from shutil import rmtree
from Shot import *
from Asset import *
from Resources import *
from Settings import *
from XMLParser import *

import re


class Project:
	def __init__(self, directory):
		self.shot_list = {}
		self.asset_list = {}

		self.last_used_sequence = 1

		self.selected_shot = None
		self.selected_asset = None
		self.directory = directory
		self.valid = True

		if not path.isdir(self.directory):
			makedirs(self.directory)

			xml_parser = XMLParser("./assets/xml/project_struct.xml")
			xml_parser.parseXML(self.directory)

		elif path.isdir(self.directory + "/05_shot"):
			self.updateShotList()
			self.updateAssetList()

		else:
			self.valid = False

		## SETTINGS ##
		self.project_settings = Settings(self.directory + "/project_option.spi")
		self.project_settings.loadProjectSettings()

		self.custom_link = self.project_settings.getSetting("custom_link")
		self.res_x = self.project_settings.getSetting("res_x")
		self.res_y = self.project_settings.getSetting("res_y")
		self.sequence_number = self.project_settings.getSetting("sequence_number")
		self.default_software = self.project_settings.getSetting("default_software")


	def getShotList(self):
		return self.shot_list


	def getAssetList(self):
		return self.asset_list


	def updateShotList(self):
		self.shot_list = {}
		for shot_name in listdir(self.directory + "/05_shot/"):
			if re.match(r"s[0-9][0-9]p[0-9][0-9][0-9]", shot_name):
				shot = Shot(self.directory, shot_name)
				shot_sequence = shot.getSequence()
				if shot_sequence > self.last_used_sequence:
					self.last_used_sequence = shot_sequence
				self.shot_list[shot_name] = shot


	def updateAssetList(self):
		self.asset_list = {}

		exclude = ["superpipe"]

		for cur_dir, sub_dirs, files in walk(self.directory + "/04_asset", topdown=True):
			if any([i in sub_dirs for i in exclude]):
				sub_dirs[:] = []
				if not "backup" in cur_dir:
					secondary_path = path.dirname(cur_dir.replace("\\", "/")).replace(self.directory + "/04_asset/", "")
					asset_name = path.basename(cur_dir)
					asset = Asset(self.directory, secondary_path, asset_name)
					self.asset_list[asset_name] = asset


	def getDirectory(self):
		return self.directory


	def getName(self):
		return self.directory.split("/")[-1]


	def getSequenceNumber(self):
		return self.sequence_number


	def getShot(self, shot_name):
		return Shot(self.directory, shot_name)


	def isValid(self):
		return self.valid


	def createShot(self, shot_sequence):
		if shot_sequence >= self.last_used_sequence:
			shot_nb = len(self.shot_list) + 1

			shot_name = Resources.makeShotName(shot_nb, shot_sequence)

		else:
			shots_to_rename = []

			for shot in self.shot_list.values():
				if Resources.makeShotNbs(shot.getShotName())[1] > shot_sequence :
					shots_to_rename.append(shot)

			shots_to_rename = shots_to_rename[::-1]

			for shot_to_rename in shots_to_rename:
				cur_shot = Shot(self.directory, shot_to_rename.getShotName())

				cur_shot.renameShot(Resources.makeShotName(shot_to_rename.getShotNb() + 1, cur_shot.getSequence()))

			shot_nb = shots_to_rename[-1].getShotNb()

			shot_name = Resources.makeShotName(shot_nb, shot_sequence)

		shot = Shot(self.directory, shot_name, software=self.default_software)

		self.shot_list[shot_name] = shot

		self.updateShotList()

		return shot_nb


	def removeShot(self, shot_name):
		shot = self.shot_list[shot_name]

		shot.deleteShot()

		for i in range(len(self.shot_list) - shot.getShotNb()):
			n = i + shot.getShotNb()

			#cur_shot = Shot(self.directory, self.shot_list[n].getShotName())
			cur_shot = self.shot_list.values()[n]

			cur_shot.renameShot(Resources.makeShotName(self.shot_list.values()[n - 1].getShotNb(), cur_shot.getSequence()))

		self.updateShotList()


	def moveShotUp(self, shot_name):
		shot = self.shot_list[shot_name]
		shot_name_backup = shot.getShotName()

		swap_shot = self.getShotFromNumber(shot.getShotNb() + 1)
		swap_shot_name_backup = swap_shot.getShotName()

		try:
			shot.renameShot("s00p000")
			self.shot_list["s00p000"] = self.shot_list.pop(shot_name_backup)

			swap_shot.renameShot(shot_name_backup)
			self.shot_list[shot_name_backup] = self.shot_list.pop(swap_shot_name_backup)

			shot.renameShot(swap_shot_name_backup)
			self.shot_list[swap_shot_name_backup] = self.shot_list.pop("s00p000")
		except:
			print("ERROR : Could not rename the shots")


	def moveShotDown(self, shot_name):
		shot = self.shot_list[shot_name]
		shot_name_backup = shot.getShotName()

		swap_shot = self.getShotFromNumber(shot.getShotNb() - 1)
		swap_shot_name_backup = swap_shot.getShotName()

		try:
			shot.renameShot("s00p000")
			self.shot_list["s00p000"] = self.shot_list.pop(shot_name_backup)

			swap_shot.renameShot(shot_name_backup)
			self.shot_list[shot_name_backup] = self.shot_list.pop(swap_shot_name_backup)

			shot.renameShot(swap_shot_name_backup)
			self.shot_list[swap_shot_name_backup] = self.shot_list.pop("s00p000")
		except:
			print("ERROR : Could not rename the shots")


	def getShotFromNumber(self, nb):
		for shot in self.shot_list.values():
			if shot.getShotNb() == nb:
				return shot

		return None


	def createAsset(self, asset_name, second_path, software):
		if self.asset_list.get(asset_name):
			return False

		asset = Asset(self.directory, second_path, asset_name, software)
		self.asset_list[asset_name] = asset

		return True


	def removeAsset(self, asset_name, second_path):
		asset = Asset(self.directory, second_path, asset_name)
		asset.deleteAsset()
		self.updateAssetList()


	def filterAssetList(self, filter_str):
		filtered_asset_list = []

		for asset in self.asset_list.values():
			if re.search(filter_str, asset.getAssetName()):
				filtered_asset_list.append(asset)

		return filtered_asset_list


	def cleanBackups(self):
		rmtree(self.directory + "/05_shot/backup")
		makedirs(self.directory + "/05_shot/backup")

		rmtree(self.directory + "/04_asset/character/backup")
		makedirs(self.directory + "/04_asset/character/backup")

		rmtree(self.directory + "/04_asset/FX/backup")
		makedirs(self.directory + "/04_asset/FX/backup")

		rmtree(self.directory + "/04_asset/props/backup")
		makedirs(self.directory + "/04_asset/props/backup")

		rmtree(self.directory + "/04_asset/set/backup")
		makedirs(self.directory + "/04_asset/set/backup")


	def setSelection(self, shot_name=None, asset_name=None, second_path=None):
		if shot_name:
			self.selected_shot = self.shot_list[shot_name]
			self.selected_asset = None
		elif asset_name:
			self.selected_asset = self.asset_list[asset_name]
			self.selected_shot = None


	def getSelection(self):
		if self.selected_shot:
			return self.selected_shot
		elif self.selected_asset:
			return self.selected_asset


	def getSelectionType(self):
		if self.selected_shot:
			return "shot"
		elif self.selected_asset:
			return "asset"


	def setResolution(self, res):
		self.res_x = res[0]
		self.res_y = res[1]

		self.project_settings.setSetting("res_x", self.res_x)
		self.project_settings.setSetting("res_y", self.res_y)
		self.project_settings.saveSettings()


	def setAllShotsRes(self):
		for shot in listdir(self.getDirectory() + "/05_shot/"):
			if shot != "backup":
				cur_shot = Shot(self.getDirectory(), shot)
				cur_shot.setResolution(self.getResolution())


	def getResolution(self):
		return (self.res_x, self.res_y)


	def setDefaultSoftware(self, default_software):
		self.default_software = default_software

		self.project_settings.setSetting("default_software", self.default_software)
		self.project_settings.saveSettings()


	def getDefaultSoftware(self):
		return self.default_software


	def setCustomLink(self, custom_link):
		self.custom_link = custom_link

		self.project_settings.setSetting("custom_link", self.custom_link)
		self.project_settings.saveSettings()


	def getCustomLink(self):
		return self.custom_link


	def addSequence(self):
		self.sequence_number += 1

		self.project_settings.setSetting("sequence_number", self.sequence_number)
		self.project_settings.saveSettings()
