#!/usr/bin/python

from os import makedirs, listdir, path, rename, walk
from shutil import rmtree
from Shot import *
from Asset import *
from Resources import *

import re


class Project:
	def __init__(self, directory):
		self.shot_list = []
		self.asset_list = []

		self.sequence_number = 1
		self.selected_shot = None
		self.selected_asset = None
		self.directory = directory
		self.res_x = 1920
		self.res_y = 1080
		self.valid = True
		self.default_software = "maya"
		self.custom_link = ""

		if not path.isdir(self.directory):
			makedirs(self.directory)

			makedirs(self.directory + "/01_donnee")

			makedirs(self.directory + "/02_ressources")

			makedirs(self.directory + "/03_preprod")
			makedirs(self.directory + "/03_preprod/character")
			makedirs(self.directory + "/03_preprod/colorscript")
			makedirs(self.directory + "/03_preprod/figureFond")
			makedirs(self.directory + "/03_preprod/lumascript")
			makedirs(self.directory + "/03_preprod/props")
			makedirs(self.directory + "/03_preprod/scenario")
			makedirs(self.directory + "/03_preprod/set")
			makedirs(self.directory + "/03_preprod/sound")
			makedirs(self.directory + "/03_preprod/storyboard")

			makedirs(self.directory + "/04_asset")
			makedirs(self.directory + "/04_asset/character")
			makedirs(self.directory + "/04_asset/character/backup")
			makedirs(self.directory + "/04_asset/FX")
			makedirs(self.directory + "/04_asset/FX/backup")
			makedirs(self.directory + "/04_asset/props")
			makedirs(self.directory + "/04_asset/props/backup")
			makedirs(self.directory + "/04_asset/set")
			makedirs(self.directory + "/04_asset/set/backup")

			makedirs(self.directory + "/05_shot")
			makedirs(self.directory + "/05_shot/backup")

			makedirs(self.directory + "/06_postprod")

			makedirs(self.directory + "/07_montage")
			makedirs(self.directory + "/07_montage/input")
			makedirs(self.directory + "/07_montage/inputSon")
			makedirs(self.directory + "/07_montage/output")

			makedirs(self.directory + "/08_linetest")

			makedirs(self.directory + "/09_DEV")

			makedirs(self.directory + "/10_print")

			with open(self.directory + "/project_option.spi", "w") as f:
				f.write("www.google.fr\n")
				f.write("1920x1080\n")
			f.close()

		elif path.isdir(self.directory + "/05_shot"):
			self.updateShotList()
			self.updateAssetList()

			if not Resources.readLine(self.directory + "/project_option.spi", 2):
				Resources.writeAtLine(self.directory + "/project_option.spi", self.res_x + "x" + self.res_y, 2)

			if not Resources.readLine(self.directory + "/project_option.spi", 3):
				Resources.writeAtLine(self.directory + "/project_option.spi", str(self.sequence_number), 3)

			if not Resources.readLine(self.directory + "/project_option.spi", 4):
				Resources.writeAtLine(self.directory + "/project_option.spi", self.default_software, 4)

			res = Resources.readLine(self.directory + "/project_option.spi", 2).split("x")

			self.res_x = res[0]
			self.res_y = res[1]

			self.custom_link = Resources.readLine(self.directory + "/project_option.spi", 1)
			self.sequence_number = int(Resources.readLine(self.directory + "/project_option.spi", 3))
			self.default_software = Resources.readLine(self.directory + "/project_option.spi", 4)

		else:
			self.valid = False


	def getShotList(self):
		return self.shot_list


	def getAssetList(self):
		return self.asset_list


	def updateShotList(self):
		self.shot_list = []
		for shot_name in listdir(self.directory + "/05_shot/"):
			if re.match(r"s[0-9][0-9]p[0-9][0-9][0-9]", shot_name):
				shot = Shot(self.directory, shot_name)
				self.shot_list.append(shot)


	def updateAssetList(self):
		self.asset_list = []

		exclude = ["superpipe"]

		for cur_dir, sub_dirs, files in walk(self.directory + "/04_asset", topdown=True):
			if any([i in sub_dirs for i in exclude]):
				sub_dirs[:] = []
				if not "backup" in cur_dir:
					asset = Asset(self.directory, path.dirname(cur_dir.replace("\\", "/")).replace(self.directory + "/04_asset/", ""), path.basename(cur_dir))
					self.asset_list.append(asset)


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
		current_sequence = 1

		if self.shot_list:
			current_sequence = Shot(self.directory, self.shot_list[-1].getShotName()).getSequence()

		if shot_sequence >= current_sequence:
			shot_nb = len(self.shot_list) + 1

			shot_name = Resources.makeShotName(shot_nb, shot_sequence)

			shot = Shot(self.directory, shot_name, software = self.default_software)

		else:
			shots_to_rename = []

			for shot in self.shot_list:
				if Resources.makeShotNbs(shot.getShotName())[1] > shot_sequence :
					shots_to_rename.append(shot)

			shots_to_rename = shots_to_rename[::-1]

			for shot_to_rename in shots_to_rename:
				cur_shot = Shot(self.directory, shot_to_rename.getShotName())

				cur_shot.renameShot(Resources.makeShotName(shot_to_rename.getShotNb() + 1, cur_shot.getSequence()))

			shot_nb = shots_to_rename[-1].getShotNb()

			shot = Shot(self.directory, Resources.makeShotName(shot_nb, shot_sequence), software = self.default_software)

		self.shot_list.append(shot)

		self.updateShotList()

		return shot_nb


	def removeShot(self, shot_name):
		shot = Shot(self.directory, shot_name)

		shot.deleteShot()

		for i in range(len(self.shot_list) - shot.getShotNb()):
			n = i + shot.getShotNb()

			cur_shot = Shot(self.directory, self.shot_list[n].getShotName())

			cur_shot.renameShot(Resources.makeShotName(self.shot_list[n - 1].getShotNb(), cur_shot.getSequence()))

		self.updateShotList()


	def moveShotUp(self, shot_name):
		shot = Shot(self.directory, shot_name)
		shot_name_backup = shot.getShotName()

		swap_shot = Shot(self.directory, self.shot_list[shot.getShotNb()].getShotName())
		swap_shot_name_backup = swap_shot.getShotName()

		shot.renameShot("s00p000")

		swap_shot.renameShot(shot_name_backup)

		shot.renameShot(swap_shot_name_backup)


	def moveShotDown(self, shot_name):
		shot = Shot(self.directory, shot_name)
		shot_name_backup = shot.getShotName()

		swap_shot = Shot(self.directory, self.shot_list[shot.getShotNb() - 2].getShotName())
		swap_shot_name_backup = swap_shot.getShotName()

		shot.renameShot("s00p000")

		swap_shot.renameShot(shot_name_backup)

		shot.renameShot(swap_shot_name_backup)


	def createAsset(self, asset_name, second_path, software):
		for check_asset in self.asset_list:
			if asset_name == check_asset.getAssetName():
				return False

		asset = Asset(self.directory, second_path, asset_name, software)
		self.asset_list.append(asset)

		return True


	def removeAsset(self, asset_name, second_path):
		asset = Asset(self.directory, second_path, asset_name)
		asset.deleteAsset()
		self.updateAssetList()


	def filterAssetList(self, filter_str):
		filtered_asset_list = []

		for asset in self.asset_list:
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


	def setSelection(self, shot_name = None, asset_name = None, second_path = None):
		if shot_name:
			self.selected_shot = Shot(self.directory, shot_name)
			self.selected_asset = None
		elif asset_name:
			self.selected_asset = Asset(self.directory, second_path, asset_name)
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

		Resources.writeAtLine(self.getDirectory() + "/project_option.spi", self.res_x + "x" + self.res_y, 2)


	def setAllShotsRes(self):
		for shot in listdir(self.getDirectory() + "/05_shot/"):
			if shot != "backup":
				cur_shot = Shot(self.getDirectory(), shot)
				cur_shot.setResolution(self.getResolution())


	def getResolution(self):
		return (self.res_x, self.res_y)


	def setDefaultSoftware(self, default_software):
		self.default_software = default_software
		Resources.writeAtLine(self.getDirectory() + "/project_option.spi", self.default_software, 4)


	def getDefaultSoftware(self):
		return self.default_software


	def setCustomLink(self, custom_link):
		self.custom_link = custom_link
		Resources.writeAtLine(self.getDirectory() + "/project_option.spi", self.custom_link, 1)


	def getCustomLink(self):
		return self.custom_link


	def addSequence(self):
		self.sequence_number += 1
		Resources.writeAtLine(self.getDirectory() + "/project_option.spi", str(self.sequence_number), 3)
