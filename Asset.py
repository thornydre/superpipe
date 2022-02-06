#!/usr/bin/python

from os import makedirs
from shutil import copyfile, copytree, rmtree
from pathlib import Path
from Settings import *
from XMLParser import *

import time


class Asset:
	def __init__(self, project_dir=None, second_path=None, asset_name=None, software=None):
		self.asset_name = asset_name
		self.project_dir = project_dir
		self.second_path = second_path
		self.asset_dir = Path(f"{project_dir}/04_asset/{self.second_path}/{self.asset_name}")
		self.superpipe_dir = Path(f"{self.asset_dir}/superpipe")
		self.software = software

		if not self.asset_dir.is_dir():
			if self.software:
				makedirs(self.asset_dir)

				makedirs(self.superpipe_dir)

				self.createFolderHierarchy()

		## SETTINGS ##
		self.versions_settings = Settings(f"{self.superpipe_dir}/versions_data.spi")
		self.versions_settings.loadVersionSettings()

		self.asset_settings = Settings(f"{self.superpipe_dir}/asset_data.spi")
		self.asset_settings.loadAssetSettings()

		self.priority = self.asset_settings.getSetting("priority")
		self.modeling_done = self.asset_settings.getSetting("modeling_done")
		self.rig_done = self.asset_settings.getSetting("rig_done")
		self.lookdev_done = self.asset_settings.getSetting("lookdev_done")
		self.done = self.asset_settings.getSetting("done")
		if self.software:
			self.asset_settings.setSetting("software", self.software)
			self.asset_settings.saveSettings()
		else:
			self.software = self.asset_settings.getSetting("software")
		
		self.setTaggedPaths()


	def getAssetName(self):
		return self.asset_name


	def getSecondPath(self):
		return self.second_path


	def getDirectory(self):
		return str(self.asset_dir)


	def getPictsPath(self):
		return str(self.screenshot_dir)


	def getCategory(self):
		return self.category


	def getPriority(self):
		return self.priority


	def getModelingDone(self):
		return self.modeling_done


	def getRigDone(self):
		return self.rig_done


	def getLookdevDone(self):
		return self.lookdev_done


	def getDone(self):
		return self.done


	def getSoftware(self):
		return self.software


	def getComment(self, version_file):
		self.versions_settings.loadVersionSettings()
		comment = self.versions_settings.getSetting(version_file)

		if comment:
			return comment

		return "No comment"


	def isDone(self):
		return self.done


	def setAsset(self):
		if self.software == "maya":
			copyfile("assets/src/set_up_file_asset_maya_lookdev_renderman.ma", f"{self.asset_dir}/scenes/{self.asset_name}_03_lookdev_v01.ma")
			copyfile("assets/src/set_up_file_asset_maya.ma", f"{self.asset_dir}/scenes/{self.asset_name}_02_rigging_v01.ma")
			copyfile("assets/src/set_up_file_asset_maya.ma", f"{self.asset_dir}/scenes/{self.asset_name}_01_modeling_v01.ma")
		elif self.software == "houdini":
			copyfile("assets/src/set_up_file_asset_houdini.hip", f"{self.asset_dir}/{self.asset_name}_v01.hip")
		elif self.software == "blender":
			copyfile("assets/src/set_up_file_asset_blender.blend", f"{self.asset_dir}/scenes/{self.asset_name}_03_lookdev_v01.blend")
			copyfile("assets/src/set_up_file_asset_blender.blend", f"{self.asset_dir}/scenes/{self.asset_name}_02_rigging_v01.blend")
			copyfile("assets/src/set_up_file_asset_blender.blend", f"{self.asset_dir}/scenes/{self.asset_name}_01_modeling_v01.blend")


	def isSet(self):
		if self.software == "maya":
			for asset_file in Path(f"{self.asset_dir}/scenes/").iterdir():
				if asset_file.suffix == ".ma":
					return True

		elif self.software == "houdini":
			for asset_file in self.asset_dir.iterdir():
				if asset_file.suffix in (".hip", ".hipnc"):
					return True

		elif self.software == "blender":
			for asset_file in Path(f"{self.asset_dir}/scenes/").iterdir():
				if asset_file.suffix == ".blend":
					return True

		return False


	def deleteAsset(self):
		copytree(self.asset_dir, f"{self.project_dir}/04_asset/{self.second_path.parts[1]}/backup/{self.asset_name}_{time.strftime('%Y_%m_%d_%H_%M_%S')}")
		rmtree(self.asset_dir)


	def getVersionsList(self, last_only, modeling, rigging, lookdev, other):
		versions_list = []

		display = []
		if modeling:
			display.append("modeling")
		if rigging:
			display.append("rigging")
		if lookdev:
			display.append("lookdev")

		if self.software == "maya":
			for asset_file in Path(f"{self.asset_dir}/scenes/").iterdir():
				if not "reference" in asset_file.name:
					if not asset_file.name[0] == "_":
						if asset_file.suffix == ".ma":
							for disp in display:
								if disp in asset_file.name:
									versions_list.append((asset_file.stat().st_mtime, asset_file.name))

							if other:
								if "modeling" not in asset_file.name and "rigging" not in asset_file.name and "lookdev" not in asset_file.name:
									versions_list.append((asset_file.stat().st_mtime, asset_file.name))

			if not last_only:
				for asset_file in Path(f"{self.asset_dir}/scenes/edits/").iterdir():
					if not asset_file.name[0] == "_":
						if asset_file.suffix == ".ma":
							for disp in display:
								if disp in asset_file.name:
									versions_list.append((asset_file.stat().st_mtime, asset_file.name))

							if other:
								if "modeling" not in asset_file.name and "rigging" not in asset_file.name and "lookdev" not in asset_file.name:
									versions_list.append((asset_file.stat().st_mtime, asset_file.name))

		elif self.software == "houdini":
			for asset_file in self.asset_dir.iterdir():
				if asset_file.suffix in (".hip", ".hipnc"):
					versions_list.append((asset_file.stat().st_mtime, asset_file.name))

			if not last_only:
				for asset_file in Path(f"{self.asset_dir}/backup/").iterdir():
					if asset_file.suffix in (".hip", ".hipnc"):
						versions_list.append((asset_file.stat().st_mtime, asset_file.name))

		elif self.software == "blender":
			for asset_file in Path(f"{self.asset_dir}/scenes/").iterdir():
				if not "reference" in asset_file.name:
					if not asset_file.name[0] == "_":
						if asset_file.suffix == ".blend":
							for disp in display:
								if disp in asset_file.name:
									versions_list.append((asset_file.stat().st_mtime, asset_file.name))

							if other:
								if "modeling" not in asset_file.name and "rigging" not in asset_file.name and "lookdev" not in asset_file.name:
									versions_list.append((asset_file.stat().st_mtime, asset_file.name))

			if not last_only:
				for asset_file in Path(f"{self.asset_dir}/scenes/edits/").iterdir():
					if not asset_file.name[0] == "_":
						if asset_file.suffix == ".blend":
							for disp in display:
								if disp in asset_file.name:
									versions_list.append((asset_file.stat().st_mtime, asset_file.name))

							if other:
								if "modeling" not in asset_file.name and "rigging" not in asset_file.name and "lookdev" not in asset_file.name:
									versions_list.append((asset_file.stat().st_mtime, asset_file.name))

		return sorted(versions_list, reverse = True)


	def getPlayblastsList(self):
		playblasts_list = []
		for playblast_file in self.playblast_dir.iterdir():
			if playblast_file.suffix in (".mov", ".avi"):
				playblasts_list.append((playblast_file.stat().st_mtime, playblast_file.name))

		return sorted(playblasts_list, reverse=True)


	def renameAsset(self, new_name):
		new_dir = f"{self.asset_dir.parent}/{new_name}"

		self.asset_dir.rename(new_dir)

		if self.software == "maya" or self.software == "blender":
			for f in Path(f"{new_dir}/scenes/").iterdir():
				if self.asset_name in f.parts:
					f.rename(str(f).replace(self.asset_name, new_name))

			for f in Path(f"{new_dir}/scenes/edits/").iterdir():
				if self.asset_name in f.parts:
					f.rename(str(f).replace(self.asset_name, new_name))

			for f in Path(f"{new_dir}/scenes/backup/").iterdir():
				if self.asset_name in f.parts:
					f.rename(str(f).replace(self.asset_name, new_name))

			for f in Path(f"{new_dir}/images/screenshots/").iterdir():
				if self.asset_name in f.parts:
					f.rename(str(f).replace(self.asset_name, new_name))

		elif self.software == "houdini":
			for f in Path(new_dir).iterdir():
				if self.asset_name in f.parts:
					f.rename(str(f).replace(self.asset_name, new_name))


	def setPriority(self, priority):
		self.priority = int(priority)
		self.asset_settings.setSetting("priority", self.priority)
		self.asset_settings.saveSettings()


	def setModelingDone(self, modeling_done):
		self.modeling_done = modeling_done
		self.asset_settings.setSetting("modeling_done", self.modeling_done)
		self.asset_settings.saveSettings()


	def setRigDone(self, rig_done):
		self.rig_done = rig_done
		self.asset_settings.setSetting("rig_done", self.rig_done)
		self.asset_settings.saveSettings()


	def setLookdevDone(self, lookdev_done):
		self.lookdev_done = lookdev_done
		self.asset_settings.setSetting("lookdev_done", self.lookdev_done)
		self.asset_settings.saveSettings()


	def setDone(self, done):
		self.done = done
		self.asset_settings.setSetting("done", self.done)
		self.asset_settings.saveSettings()


	def createFolderHierarchy(self):
		if self.software == "maya" or self.software == "blender":
			xml_parser = XMLParser("./assets/xml/default_asset_struct.xml")
		elif self.software == "houdini":
			xml_parser = XMLParser("./assets/xml/houdini_asset_struct.xml")
		else:
			print("ERROR")
		
		xml_parser.parseXML(str(self.asset_dir))


	def setTaggedPaths(self):
		if self.software == "maya" or self.software == "blender":
			xml_parser = XMLParser("./assets/xml/default_asset_struct.xml")
		elif self.software == "houdini":
			xml_parser = XMLParser("./assets/xml/houdini_asset_struct.xml")
		else:
			print("ERROR")

		tagged_paths = xml_parser.pathToTag(str(self.asset_dir))

		self.screenshot_dir = Path(tagged_paths["screenshot_dir"])
		self.playblast_dir = Path(tagged_paths["playblast_dir"])
		self.backup_dir = Path(tagged_paths["backup_dir"])
		self.edit_dir = Path(tagged_paths["edit_dir"])
