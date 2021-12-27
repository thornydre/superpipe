#!/usr/bin/python

from os import makedirs, path, listdir, rename
from shutil import copyfile, copytree, rmtree
from Settings import *

import time


class Asset:
	def __init__(self, directory=None, second_path=None, asset_name=None, software=None):
		self.asset_name = asset_name
		self.project_dir = directory
		self.second_path = second_path
		self.asset_directory = directory + "/04_asset/" + self.second_path + "/" + self.asset_name
		self.software = software

		if not path.isdir(self.asset_directory):
			if self.software:
				makedirs(self.asset_directory)

				makedirs(self.asset_directory + "/superpipe")

				self.createFolderHierarchy()

		## SETTINGS ##
		self.versions_settings = Settings(self.asset_directory + "/superpipe/versions_data.spi")
		self.versions_settings.loadVersionSettings()

		self.asset_settings = Settings(self.asset_directory + "/superpipe/asset_data.spi")
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


	def getAssetName(self):
		return self.asset_name


	def getSecondPath(self):
		return self.second_path


	def getDirectory(self):
		return self.asset_directory


	def getPictsPath(self):
		directory = self.asset_directory + "/images/screenshots/"

		if self.software == "houdini":
			directory = self.asset_directory + "/render/screenshots/"

		return directory


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
			copyfile("assets/src/set_up_file_asset_maya_lookdev_renderman.ma", self.asset_directory + "/scenes/" + self.asset_name + "_03_lookdev_v01.ma")
			copyfile("assets/src/set_up_file_asset_maya.ma", self.asset_directory + "/scenes/" + self.asset_name + "_02_rigging_v01.ma")
			copyfile("assets/src/set_up_file_asset_maya.ma", self.asset_directory + "/scenes/" + self.asset_name + "_01_modeling_v01.ma")
		elif self.software == "houdini":
			copyfile("assets/src/set_up_file_asset_houdini.hip", self.asset_directory + "/" + self.asset_name + "_v01.hip")
		elif self.software == "blender":
			copyfile("assets/src/set_up_file_asset_blender.blend", self.asset_directory + "/scenes/" + self.asset_name + "_03_lookdev_v01.blend")
			copyfile("assets/src/set_up_file_asset_blender.blend", self.asset_directory + "/scenes/" + self.asset_name + "_02_rigging_v01.blend")
			copyfile("assets/src/set_up_file_asset_blender.blend", self.asset_directory + "/scenes/" + self.asset_name + "_01_modeling_v01.blend")


	def isSet(self):
		if self.software == "maya":
			for asset_file in listdir(self.asset_directory + "/scenes/"):
				if path.splitext(asset_file)[1] == ".ma":
					return True

		elif self.software == "houdini":
			for asset_file in listdir(self.asset_directory):
				if path.splitext(asset_file)[1] in (".hip", ".hipnc"):
					return True

		elif self.software == "blender":
			for asset_file in listdir(self.asset_directory + "/scenes/"):
				if path.splitext(asset_file)[1] == ".blend":
					return True

		return False


	def deleteAsset(self):
		copytree(self.asset_directory, self.project_dir +"/04_asset/" + self.second_path.split("/")[1] + "/backup/" + self.asset_name + "_" + time.strftime("%Y_%m_%d_%H_%M_%S"))
		rmtree(self.asset_directory)


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
			for asset_file in listdir(self.asset_directory + "/scenes/"):
				if not "reference" in asset_file:
					if not asset_file[0] == "_":
						if path.splitext(asset_file)[1] == ".ma":
							for disp in display:
								if disp in asset_file:
									versions_list.append((path.getmtime(self.asset_directory + "/scenes/" + asset_file), asset_file))

							if other:
								if "modeling" not in asset_file and "rigging" not in asset_file and "lookdev" not in asset_file:
									versions_list.append((path.getmtime(self.asset_directory + "/scenes/" + asset_file), asset_file))

			if not last_only:
				for asset_file in listdir(self.asset_directory + "/scenes/edits/"):
					if not asset_file[0] == "_":
						if path.splitext(asset_file)[1] == ".ma":
							for disp in display:
								if disp in asset_file:
									versions_list.append((path.getmtime(self.asset_directory + "/scenes/edits/" + asset_file), asset_file))

							if other:
								if "modeling" not in asset_file and "rigging" not in asset_file and "lookdev" not in asset_file:
									versions_list.append((path.getmtime(self.asset_directory + "/scenes/edits/" + asset_file), asset_file))

		elif self.software == "houdini":
			for asset_file in listdir(self.asset_directory + "/"):
				if path.splitext(asset_file)[1] in (".hip", ".hipnc"):
					versions_list.append((path.getmtime(self.asset_directory + "/" + asset_file), asset_file))

			if not last_only:
				for asset_file in listdir(self.asset_directory + "/backup/"):
					if path.splitext(asset_file)[1] in (".hip", ".hipnc"):
						versions_list.append((path.getmtime(self.asset_directory + "/backup/" + asset_file), asset_file))

		elif self.software == "blender":
			for asset_file in listdir(self.asset_directory + "/scenes/"):
				if not "reference" in asset_file:
					if not asset_file[0] == "_":
						if path.splitext(asset_file)[1] == ".blend":
							for disp in display:
								if disp in asset_file:
									versions_list.append((path.getmtime(self.asset_directory + "/scenes/" + asset_file), asset_file))

							if other:
								if "modeling" not in asset_file and "rigging" not in asset_file and "lookdev" not in asset_file:
									versions_list.append((path.getmtime(self.asset_directory + "/scenes/" + asset_file), asset_file))

			if not last_only:
				for asset_file in listdir(self.asset_directory + "/scenes/edits/"):
					if not asset_file[0] == "_":
						if path.splitext(asset_file)[1] == ".blend":
							for disp in display:
								if disp in asset_file:
									versions_list.append((path.getmtime(self.asset_directory + "/scenes/edits/" + asset_file), asset_file))

							if other:
								if "modeling" not in asset_file and "rigging" not in asset_file and "lookdev" not in asset_file:
									versions_list.append((path.getmtime(self.asset_directory + "/scenes/edits/" + asset_file), asset_file))

		return sorted(versions_list, reverse = True)


	def getPlayblastsList(self):
		playblasts_list = []
		for playblast_file in listdir(self.asset_directory + "/movies/"):
			if path.splitext(playblast_file)[1] in (".mov", ".avi"):
				playblasts_list.append((path.getmtime(self.asset_directory + "/movies/" + playblast_file), playblast_file))

		return sorted(playblasts_list, reverse = True)


	def renameAsset(self, new_name):
		new_dir = path.dirname(self.asset_directory) + "/" + new_name

		rename(self.asset_directory, new_dir)

		if self.software == "maya" or self.software == "blender":
			for f in listdir(new_dir + "/scenes/"):
				if self.asset_name in f:
					rename(new_dir + "/scenes/" + f, new_dir + "/scenes/" + f.replace(self.asset_name, new_name))

			for f in listdir(new_dir + "/scenes/edits/"):
				if self.asset_name in f:
					rename(new_dir + "/scenes/edits/" + f, new_dir + "/scenes/edits/" + f.replace(self.asset_name, new_name))

			for f in listdir(new_dir + "/scenes/backup/"):
				if self.asset_name in f:
					rename(new_dir + "/scenes/backup/" + f, new_dir + "/scenes/backup/" + f.replace(self.asset_name, new_name))

			for f in listdir(new_dir + "/images/screenshots/"):
				if self.asset_name in f:
					rename(new_dir + "/images/screenshots/" + f, new_dir + "/images/screenshots/" + f.replace(self.asset_name, new_name))

		elif self.software == "houdini":
			for f in listdir(new_dir):
				if self.asset_name in f:
					rename(new_dir + "/" + f, new_dir + "/" + f.replace(self.asset_name, new_name))


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
			makedirs(self.asset_directory + "/assets")
			
			makedirs(self.asset_directory + "/autosave")
			
			makedirs(self.asset_directory + "/cache")
			makedirs(self.asset_directory + "/cache/nCache")
			makedirs(self.asset_directory + "/cache/nCache/fluid")
			makedirs(self.asset_directory + "/cache/particles")

			makedirs(self.asset_directory + "/clips")
			
			makedirs(self.asset_directory + "/data")
			makedirs(self.asset_directory + "/data/edits")
			
			makedirs(self.asset_directory + "/images")
			makedirs(self.asset_directory + "/images/screenshots")
			
			makedirs(self.asset_directory + "/movies")
			
			makedirs(self.asset_directory + "/renderData")
			makedirs(self.asset_directory + "/renderData/depth")
			makedirs(self.asset_directory + "/renderData/fur")
			makedirs(self.asset_directory + "/renderData/fur/furAttrMap")
			makedirs(self.asset_directory + "/renderData/fur/furEqualMap")
			makedirs(self.asset_directory + "/renderData/fur/furFiles")
			makedirs(self.asset_directory + "/renderData/fur/furImages")
			makedirs(self.asset_directory + "/renderData/fur/furShadowMap")
			makedirs(self.asset_directory + "/renderData/iprImages")
			makedirs(self.asset_directory + "/renderData/shaders")
			
			makedirs(self.asset_directory + "/scenes")
			makedirs(self.asset_directory + "/scenes/backup")
			makedirs(self.asset_directory + "/scenes/edits")

			makedirs(self.asset_directory + "/scripts")
			
			makedirs(self.asset_directory + "/sound")
			
			makedirs(self.asset_directory + "/sourceimages")
			makedirs(self.asset_directory + "/sourceimages/3dPaintTextures")
			makedirs(self.asset_directory + "/sourceimages/edits")
			makedirs(self.asset_directory + "/sourceimages/environment")
			makedirs(self.asset_directory + "/sourceimages/imagePlane")
			makedirs(self.asset_directory + "/sourceimages/imageSequence")

			copyfile("assets/src/workspace.mel", self.asset_directory + "/workspace.mel")

		elif self.software == "houdini":
			makedirs(self.asset_directory + "/abc")
			makedirs(self.asset_directory + "/audio")
			makedirs(self.asset_directory + "/backup")
			makedirs(self.asset_directory + "/comp")
			makedirs(self.asset_directory + "/desk")
			makedirs(self.asset_directory + "/flip")
			makedirs(self.asset_directory + "/geo")
			makedirs(self.asset_directory + "/hda")
			makedirs(self.asset_directory + "/render")
			makedirs(self.asset_directory + "/scripts")
			makedirs(self.asset_directory + "/sim")
			makedirs(self.asset_directory + "/tex")
			makedirs(self.asset_directory + "/video")
		else:
			print("ERROR")