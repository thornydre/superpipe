#!/usr/bin/python

from os import makedirs
from pathlib import Path
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
		self.valid = True

		self.project_dir_path = Path(directory)

		xml_parser = XMLParser("./assets/xml/project_struct.xml")
		tagged_paths = xml_parser.pathToTag(str(self.project_dir_path))

		self.asset_dir_path = Path(tagged_paths["asset_dir"])
		self.shot_dir_path = Path(tagged_paths["shot_dir"])
			
		if not self.project_dir_path.is_dir():
			makedirs(self.project_dir_path)

			xml_parser.parseXML(str(self.project_dir_path))

		elif self.asset_dir_path.is_dir() and self.shot_dir_path.is_dir():
			self.updateShotList()
			self.updateAssetList()

		else:
			self.valid = False

		## SETTINGS ##
		if self.valid:
			self.project_settings = Settings(f"{self.project_dir_path}/project_option.spi")
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
		for shot_path in self.shot_dir_path.iterdir():
			shot_name = shot_path.name
			if re.match(r"s[0-9][0-9]p[0-9][0-9][0-9]", shot_name):
				shot = Shot(self.project_dir_path, shot_name)
				shot_sequence = shot.getSequence()
				if shot_sequence > self.last_used_sequence:
					self.last_used_sequence = shot_sequence
				self.shot_list[shot_name] = shot


	def updateAssetList(self):
		self.asset_list = {}

		exclude = ["superpipe"]

		for superpipe_dir in self.asset_dir_path.rglob("superpipe"):
			if not "backup" in superpipe_dir.parts:
				temp_path = superpipe_dir.relative_to(self.asset_dir_path).parent
				secondary_path = temp_path.parent
				asset_name = temp_path.name
				asset = Asset(self.project_dir_path, secondary_path, asset_name)
				self.asset_list[asset_name] = asset


		# for cur_dir, sub_dirs, files in walk(self.asset_dir_path, topdown=True):
		# 	if any([i in sub_dirs for i in exclude]):
		# 		print(cur_dir)
		# 		sub_dirs[:] = []
		# 		if not "backup" in cur_dir:
		# 			secondary_path = path.dirname(cur_dir.replace("\\", "/")).replace(str(self.project_dir_path) + "/04_asset/", "")
		# 			asset_name = path.basename(cur_dir)
		# 			asset = Asset(self.project_dir_path, secondary_path, asset_name)
		# 			self.asset_list[asset_name] = asset


	def getDirectory(self):
		return str(self.project_dir_path)


	def getName(self):
		return self.project_dir_path.name


	def getSequenceNumber(self):
		return self.sequence_number


	def getShot(self, shot_name):
		return Shot(self.project_dir_path, shot_name)


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
				cur_shot = Shot(self.project_dir_path, shot_to_rename.getShotName())

				cur_shot.renameShot(Resources.makeShotName(shot_to_rename.getShotNb() + 1, cur_shot.getSequence()))

			shot_nb = shots_to_rename[-1].getShotNb()

			shot_name = Resources.makeShotName(shot_nb, shot_sequence)

		shot = Shot(self.project_dir_path, shot_name, software=self.default_software)

		self.shot_list[shot_name] = shot

		self.updateShotList()

		return shot_nb


	def removeShot(self, shot_name):
		shot = self.shot_list[shot_name]

		shot.deleteShot()

		for i in range(len(self.shot_list) - shot.getShotNb()):
			n = i + shot.getShotNb()

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

			shot.setTaggedPaths()
			swap_shot.setTaggedPaths()

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

			shot.setTaggedPaths()
			swap_shot.setTaggedPaths()

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

		asset = Asset(self.project_dir_path, Path(second_path), asset_name, software)
		self.asset_list[asset_name] = asset

		return True


	def removeAsset(self, asset_name, second_path):
		asset = Asset(self.project_dir_path, Path(second_path), asset_name)
		asset.deleteAsset()
		self.updateAssetList()


	def filterAssetList(self, filter_str):
		filtered_asset_list = []

		for asset in self.asset_list.values():
			if re.search(filter_str, asset.getAssetName()):
				filtered_asset_list.append(asset)

		return filtered_asset_list


	def cleanBackups(self):
		rmtree(f"{self.shot_dir_path}/backup")
		makedirs(f"{self.shot_dir_path}/backup")

		rmtree(f"{self.asset_dir_path}/character/backup")
		makedirs(f"{self.asset_dir_path}/character/backup")

		rmtree(f"{self.asset_dir_path}/FX/backup")
		makedirs(f"{self.asset_dir_path}/FX/backup")

		rmtree(f"{self.asset_dir_path}/props/backup")
		makedirs(f"{self.asset_dir_path}/props/backup")

		rmtree(f"{self.asset_dir_path}/set/backup")
		makedirs(f"{self.asset_dir_path}/set/backup")


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
		for shot in Path(f"{self.project_dir_path}/05_shot/").iterdir():
			if shot.name != "backup":
				cur_shot = Shot(self.project_dir_path, shot)
				cur_shot.setResolution((self.res_x, self.res_y))


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
