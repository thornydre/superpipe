#!/usr/bin/python

from os import makedirs, path, listdir
from shutil import copyfile, copytree, rmtree
from Resources import *

import time


class Asset:
	def __init__(self, directory = None, second_path = None, asset_name = None, software = None):
		self.asset_name = asset_name
		self.project_dir = directory
		self.second_path = second_path
		self.directory = directory + "/04_asset/" + self.second_path + "/" + self.asset_name
		self.priority = 0
		self.modeling_done = 0
		self.rig_done = 0
		self.lookdev_done = 0
		self.done = 0
		self.software = software

		if not path.isdir(self.directory):
			if self.software:
				makedirs(self.directory)

				makedirs(self.directory + "/superpipe")

				with open(self.directory + "/superpipe/asset_data.spi", "w") as f:
						f.write(str(self.priority) + "\n" + str(self.modeling_done) + "\n" + str(self.rig_done) + "\n" + str(self.lookdev_done) + "\n" + str(self.done) + "\n" + self.software + "\n")
				f.close()

				open(self.directory + "/superpipe/versions_data.spi", "a").close()

				if self.software == "maya" or self.software == "blender":
					makedirs(self.directory + "/assets")
					
					makedirs(self.directory + "/autosave")
					
					makedirs(self.directory + "/cache")
					makedirs(self.directory + "/cache/nCache")
					makedirs(self.directory + "/cache/nCache/fluid")
					makedirs(self.directory + "/cache/particles")

					makedirs(self.directory + "/clips")
					
					makedirs(self.directory + "/data")
					makedirs(self.directory + "/data/edits")
					
					makedirs(self.directory + "/images")
					makedirs(self.directory + "/images/screenshots")
					
					makedirs(self.directory + "/movies")
					
					makedirs(self.directory + "/renderData")
					makedirs(self.directory + "/renderData/depth")
					makedirs(self.directory + "/renderData/fur")
					makedirs(self.directory + "/renderData/fur/furAttrMap")
					makedirs(self.directory + "/renderData/fur/furEqualMap")
					makedirs(self.directory + "/renderData/fur/furFiles")
					makedirs(self.directory + "/renderData/fur/furImages")
					makedirs(self.directory + "/renderData/fur/furShadowMap")
					makedirs(self.directory + "/renderData/iprImages")
					makedirs(self.directory + "/renderData/shaders")
					
					makedirs(self.directory + "/scenes")
					makedirs(self.directory + "/scenes/backup")
					makedirs(self.directory + "/scenes/edits")

					makedirs(self.directory + "/scripts")
					
					makedirs(self.directory + "/sound")
					
					makedirs(self.directory + "/sourceimages")
					makedirs(self.directory + "/sourceimages/3dPaintTextures")
					makedirs(self.directory + "/sourceimages/edits")
					makedirs(self.directory + "/sourceimages/environment")
					makedirs(self.directory + "/sourceimages/imagePlane")
					makedirs(self.directory + "/sourceimages/imageSequence")

					copyfile("assets/src/workspace.mel", self.directory + "/workspace.mel")

				elif self.software == "houdini":
					makedirs(self.directory + "/abc")
					makedirs(self.directory + "/audio")
					makedirs(self.directory + "/backup")
					makedirs(self.directory + "/comp")
					makedirs(self.directory + "/desk")
					makedirs(self.directory + "/flip")
					makedirs(self.directory + "/geo")
					makedirs(self.directory + "/hda")
					makedirs(self.directory + "/render")
					makedirs(self.directory + "/scripts")
					makedirs(self.directory + "/sim")
					makedirs(self.directory + "/tex")
					makedirs(self.directory + "/video")
				else:
					print("ERROR")

		else:
			if not path.isfile(self.directory + "/superpipe/versions_data.spi"):
				open(self.directory + "/superpipe/versions_data.spi", "a").close()

			if not path.isfile(self.directory + "/superpipe/asset_data.spi"):
				with open(self.directory + "/superpipe/asset_data.spi", "w") as f:
					f.write(str(self.priority) + "\n" + str(self.modeling_done) + "\n" + str(self.rig_done) + "\n" + str(self.lookdev_done) + "\n" + str(self.done) + "\n" + self.software + "\n")
				f.close()

			asset_infos = []
			with open(self.directory + "/superpipe/asset_data.spi", "r") as f:
				for l in f:
					asset_infos.append(l.strip("\n"))
			f.close()

			if len(asset_infos) > 0:
				self.priority = int(asset_infos[0])
			else:
				self.priority = 0

			if len(asset_infos) > 1:
				self.modeling_done = int(asset_infos[1])
			else:
				self.modeling_done = "0"

			if len(asset_infos) > 2:
				self.rig_done = int(asset_infos[2])
			else:
				self.rig_done = "0"

			if len(asset_infos) > 3:
				self.lookdev_done = int(asset_infos[3])
			else:
				self.lookdev_done = "0"

			if len(asset_infos) > 4:
				self.done = int(asset_infos[4])
			else:
				self.done = "0"
			
			if len(asset_infos) > 5:
				self.software = asset_infos[5]
			else:
				self.software = "maya"


	def getAssetName(self):
		return self.asset_name


	def getSecondPath(self):
		return self.second_path


	def getDirectory(self):
		return self.directory


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
		if not path.isfile(self.directory + "/superpipe/versions_data.spi"):
				open(self.directory + "/superpipe/versions_data.spi", "a").close()
		else:
			with open(self.directory + "/superpipe/versions_data.spi", "r") as f:
				all_comments = f.read()
			f.close()

			if all_comments == "":
				return "No comment"

			comment_list = all_comments.split("\n---\n")

			i = 1

			for comment in comment_list:
				if comment == version_file:
					return comment_list[i]

				i += 1

		return "No comment"


	def isDone(self):
		if self.done == 1:
			return True
		else:
			return False


	def setAsset(self):
		if self.software == "maya":
			copyfile("assets/src/set_up_file_asset_maya_lookdev_renderman.ma", self.directory + "/scenes/" + self.asset_name + "_03_lookdev_v01.ma")
			copyfile("assets/src/set_up_file_asset_maya.ma", self.directory + "/scenes/" + self.asset_name + "_02_rigging_v01.ma")
			copyfile("assets/src/set_up_file_asset_maya.ma", self.directory + "/scenes/" + self.asset_name + "_01_modeling_v01.ma")
		elif self.software == "houdini":
			copyfile("assets/src/set_up_file_asset_houdini.hip", self.directory + "/" + self.asset_name + "_v01.hip")
		elif self.software == "blender":
			copyfile("assets/src/set_up_file_asset_blender.blend", self.directory + "/scenes/" + self.asset_name + "_03_lookdev_v01.blend")
			copyfile("assets/src/set_up_file_asset_blender.blend", self.directory + "/scenes/" + self.asset_name + "_02_rigging_v01.blend")
			copyfile("assets/src/set_up_file_asset_blender.blend", self.directory + "/scenes/" + self.asset_name + "_01_modeling_v01.blend")


	def isSet(self):
		if self.software == "maya":
			for asset_file in listdir(self.directory + "/scenes/"):
				if path.splitext(asset_file)[1] == ".ma":
					return True

		elif self.software == "houdini":
			for asset_file in listdir(self.directory):
				if path.splitext(asset_file)[1] == ".hip":
					return True

		elif self.software == "blender":
			for asset_file in listdir(self.directory + "/scenes/"):
				if path.splitext(asset_file)[1] == ".blend":
					return True

		return False


	def deleteAsset(self):
		copytree(self.directory, self.project_dir +"/04_asset/" + self.second_path.split("/")[1] + "/backup/" + self.asset_name + "_" + time.strftime("%Y_%m_%d_%H_%M_%S"))
		rmtree(self.directory)


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
			for asset_file in listdir(self.directory + "/scenes/"):
				if not "reference" in asset_file:
					if not asset_file[0] == "_":
						if path.splitext(asset_file)[1] == ".ma":
							for disp in display:
								if disp in asset_file:
									versions_list.append((path.getmtime(self.directory + "/scenes/" + asset_file), asset_file))

							if other:
								if "modeling" not in asset_file and "rigging" not in asset_file and "lookdev" not in asset_file:
									versions_list.append((path.getmtime(self.directory + "/scenes/" + asset_file), asset_file))

			if not last_only:
				for asset_file in listdir(self.directory + "/scenes/edits/"):
					if not asset_file[0] == "_":
						if path.splitext(asset_file)[1] == ".ma":
							for disp in display:
								if disp in asset_file:
									versions_list.append((path.getmtime(self.directory + "/scenes/edits/" + asset_file), asset_file))

							if other:
								if "modeling" not in asset_file and "rigging" not in asset_file and "lookdev" not in asset_file:
									versions_list.append((path.getmtime(self.directory + "/scenes/edits/" + asset_file), asset_file))

		elif self.software == "houdini":
			for asset_file in listdir(self.directory + "/"):
				if path.splitext(asset_file)[1] in (".hip", ".hipnc"):
					versions_list.append((path.getmtime(self.directory + "/" + asset_file), asset_file))

			if not last_only:
				for asset_file in listdir(self.directory + "/backup/"):
					if path.splitext(asset_file)[1] in (".hip", ".hipnc"):
						versions_list.append((path.getmtime(self.directory + "/backup/" + asset_file), asset_file))

		elif self.software == "blender":
			for asset_file in listdir(self.directory + "/scenes/"):
				if not "reference" in asset_file:
					if not asset_file[0] == "_":
						if path.splitext(asset_file)[1] == ".blend":
							for disp in display:
								if disp in asset_file:
									versions_list.append((path.getmtime(self.directory + "/scenes/" + asset_file), asset_file))

							if other:
								if "modeling" not in asset_file and "rigging" not in asset_file and "lookdev" not in asset_file:
									versions_list.append((path.getmtime(self.directory + "/scenes/" + asset_file), asset_file))

			if not last_only:
				for asset_file in listdir(self.directory + "/scenes/edits/"):
					if not asset_file[0] == "_":
						if path.splitext(asset_file)[1] == ".blend":
							for disp in display:
								if disp in asset_file:
									versions_list.append((path.getmtime(self.directory + "/scenes/edits/" + asset_file), asset_file))

							if other:
								if "modeling" not in asset_file and "rigging" not in asset_file and "lookdev" not in asset_file:
									versions_list.append((path.getmtime(self.directory + "/scenes/edits/" + asset_file), asset_file))

		return sorted(versions_list, reverse = True)


	def getPlayblastsList(self):
		playblasts_list = []
		for playblast_file in listdir(self.directory + "/movies/"):
			if path.splitext(playblast_file)[1] in (".mov", ".avi"):
				playblasts_list.append((path.getmtime(self.directory + "/movies/" + playblast_file), playblast_file))

		return sorted(playblasts_list, reverse = True)


	def renameAsset(self, new_name):
		new_dir = path.dirname(self.directory) + "/" + new_name

		rename(self.directory, new_dir)

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
		Resources.writeAtLine(self.directory + "/superpipe/asset_data.spi", str(self.priority), 1)


	def setModelingDone(self, modeling_done):
		self.modeling_done = int(modeling_done)
		Resources.writeAtLine(self.directory + "/superpipe/asset_data.spi", str(self.modeling_done), 2)


	def setRigDone(self, rig_done):
		self.rig_done = int(rig_done)
		Resources.writeAtLine(self.directory + "/superpipe/asset_data.spi", str(self.rig_done), 3)


	def setLookdevDone(self, lookdev_done):
		self.lookdev_done = int(lookdev_done)
		Resources.writeAtLine(self.directory + "/superpipe/asset_data.spi", str(self.lookdev_done), 4)


	def setDone(self, done):
		self.done = int(done)
		Resources.writeAtLine(self.directory + "/superpipe/asset_data.spi", str(self.done), 5)
