#!/usr/bin/python

from os import makedirs, path, listdir, rename, remove
from shutil import copyfile, copytree, rmtree
from Resources import *
from Settings import *
from XMLParser import *

import time
import subprocess


class Shot:
	def __init__(self, directory = None, shot_name = None, software = None):
		self.shot_name = shot_name
		self.shot_nb, self.sequence = Resources.makeShotNbs(self.shot_name)
		self.shot_directory = directory + "/05_shot/" + self.shot_name
		self.postprod_directory = directory + "/06_postprod/" + self.shot_name
		self.software = software
		self.general_settings = Settings("assets/settings.spi")
		self.general_settings.loadGeneralSettings()

		if not path.isdir(self.shot_directory):
			if self.software:
				makedirs(self.shot_directory)

				makedirs(self.shot_directory + "/superpipe")

				self.createFolderHierarchy()

			else:
				print("ERROR1 : " + self.shot_name)

		elif not Shot.validShot(self.shot_directory):
			print("ERROR2 : " + self.shot_name)

		## SETTINGS ##
		self.versions_settings = Settings(self.shot_directory + "/superpipe/versions_data.spi")
		self.versions_settings.loadVersionSettings()

		self.shot_settings = Settings(self.shot_directory + "/superpipe/shot_data.spi")
		self.shot_settings.loadShotSettings()

		self.done = self.shot_settings.getSetting("done")
		self.priority = self.shot_settings.getSetting("priority")
		self.step = self.shot_settings.getSetting("step")
		self.percentage = self.shot_settings.getSetting("percentage")
		self.frame_range = self.shot_settings.getSetting("frame_range")
		self.description = self.shot_settings.getSetting("description")
		if not self.software:
			self.software = self.shot_settings.getSetting("software")

		if not path.isdir(self.postprod_directory):
			makedirs(self.postprod_directory)

			makedirs(self.postprod_directory + "/input")
			makedirs(self.postprod_directory + "/output")


	def getShotNb(self):
		return self.shot_nb


	def getShotName(self):
		return self.shot_name


	def getDirectory(self):
		return self.shot_directory


	def getPictsPath(self):
		return self.shot_directory + "/images/screenshots/"


	def getSequence(self):
		return self.sequence


	def getDescription(self):
		return self.description


	def getPriority(self):
		return self.priority


	def getDone(self):
		return self.done


	def getSoftware(self):
		return self.software


	def getStep(self):
		return self.step


	def getPercentage(self):
		return self.percentage


	def getFrameRange(self):
		return self.frame_range


	def getComment(self, version_file):
		self.versions_settings.loadVersionSettings()
		comment = self.versions_settings.getSetting(version_file)

		if comment:
			return comment

		return "No comment"


	def isDone(self):
		if self.done == 1:
			return True
		else:
			return False


	def setShot(self, res):
		if self.software == "maya":
			copyfile("assets/src/set_up_file_shot_maya.ma", self.shot_directory + "/scenes/" + self.shot_name + "_01_layout_v01.ma")
			Resources.insertAtLine(self.shot_directory + "/scenes/" + self.shot_name + "_01_layout_v01.ma", "setAttr \"sceneConfigurationScriptNode.b\" -type \"string\" \"playbackOptions -min 1001 -max " + str(1000 + self.frame_range) + " -ast 1001 -aet " + str(1000 + self.frame_range) + "\";\nselect -ne :defaultResolution;\n\tsetAttr \".w\" " + str(res[0]) + ";\n\tsetAttr \".h\" " + str(res[1]) + ";", -1)
		elif self.software == "blender":
			copyfile("assets/src/set_up_file_shot_blender.blend", self.shot_directory + "/scenes/" + self.shot_name + "_01_layout_v01.blend")


	def setFrameRange(self, frame_range):
		self.frame_range = frame_range

		if path.isdir(self.shot_directory + "/scenes/.mayaSwatches"):
					rmtree(self.shot_directory + "/scenes/.mayaSwatches")

		self.shot_settings.setSetting("frame_range", self.frame_range)
		self.shot_settings.saveSettings()

		for file in listdir(self.shot_directory + "/scenes/"):
			if path.splitext(file)[1] == ".ma":
				Resources.insertAtLine(self.shot_directory + "/scenes/" + file, "setAttr \"sceneConfigurationScriptNode.b\" -type \"string\" \"playbackOptions -min 1001 -max " + str(1000 + frame_range) + " -ast 1001 -aet " + str(1000 + frame_range) + "\";", -1)
			elif path.splitext(file)[1] == ".blend":
				text = ("import bpy\n"
				"bpy.ops.wm.open_mainfile(filepath=\"{0}\")\n"
				"bpy.context.scene.frame_start = {1}\n"
				"bpy.context.scene.frame_end = {2}\n"
				"bpy.context.scene.frame_current = {1}\n"
				"bpy.ops.wm.save_mainfile()\n"
				"bpy.ops.wm.quit_blender()").format(self.shot_directory + "/scenes/" + file, 1001, 1000 + frame_range)

				subprocess.Popen([self.general_settings.getSetting("blender_path"), "-b", "--python-expr", text])


	def setResolution(self, res):
		if path.isdir(self.shot_directory + "/scenes/.mayaSwatches"):
					rmtree(self.shot_directory + "/scenes/.mayaSwatches")

		for file in listdir(self.shot_directory + "/scenes/"):
			if path.splitext(file)[1] == ".ma":
				Resources.insertAtLine(self.shot_directory + "/scenes/" + file, "select -ne :defaultResolution;\n\tsetAttr \".w\" " + str(res[0]) + ";\n\tsetAttr \".h\" " + str(res[1]) + ";", -1)
			elif path.splitext(file)[1] == ".blend":
				print("blender file")


	def isSet(self):
		if self.software == "maya":
			for shot_file in listdir(self.shot_directory + "/scenes/"):
				if path.splitext(shot_file)[1] == ".ma":
					return True

		elif self.software == "blender":
			for shot_file in listdir(self.shot_directory + "/scenes/"):
				if path.splitext(shot_file)[1] == ".blend":
					return True

		return False


	def deleteShot(self):
		copytree(self.shot_directory, self.shot_directory +"/../backup/" + self.shot_name + "_" + time.strftime("%Y_%m_%d_%H_%M_%S"))
		rmtree(self.shot_directory)


	def getVersionsList(self, last_only, layout, blocking, splining, rendering, other):
		if not path.isdir(self.shot_directory + "/scenes/"):
			return []

		versions_list = []

		display = []
		if layout:
			display.append("layout")
		if blocking:
			display.append("blocking")
		if splining:
			display.append("splining")
		if rendering:
			display.append("rendering")

		if self.software == "maya":
			for shot_file in listdir(self.shot_directory + "/scenes/"):
				if not "reference" in shot_file:
					if shot_file[0] != "_":
						if path.splitext(shot_file)[1] == ".ma":
							for disp in display:
								if disp in shot_file:
									versions_list.append((path.getmtime(self.shot_directory + "/scenes/" + shot_file), shot_file))

							if other:
								if "layout" not in shot_file and "blocking" not in shot_file and "splining" not in shot_file and "rendering" not in shot_file:
									versions_list.append((path.getmtime(self.shot_directory + "/scenes/" + shot_file), shot_file))

			if not last_only:
				for shot_file in listdir(self.shot_directory + "/scenes/edits/"):
					if shot_file[0] != "_":
						if path.splitext(shot_file)[1] == ".ma":
							not_set = True
							for disp in display:
								if disp in shot_file:
									not_set = False
									versions_list.append((path.getmtime(self.shot_directory + "/scenes/edits/" + shot_file), shot_file))

							if other:
								if "layout" not in shot_file and "blocking" not in shot_file and "splining" not in shot_file and "rendering" not in shot_file:
									versions_list.append((path.getmtime(self.shot_directory + "/scenes/edits/" + shot_file), shot_file))

		elif self.software == "blender":
			for shot_file in listdir(self.shot_directory + "/scenes/"):
				if not "reference" in shot_file:
					if shot_file[0] != "_":
						if path.splitext(shot_file)[1] == ".blend":
							for disp in display:
								if disp in shot_file:
									versions_list.append((path.getmtime(self.shot_directory + "/scenes/" + shot_file), shot_file))

							if other:
								if "layout" not in shot_file and "blocking" not in shot_file and "splining" not in shot_file and "rendering" not in shot_file:
									versions_list.append((path.getmtime(self.shot_directory + "/scenes/" + shot_file), shot_file))

			if not last_only:
				for shot_file in listdir(self.shot_directory + "/scenes/edits/"):
					if shot_file[0] != "_":
						if path.splitext(shot_file)[1] == ".blend":
							not_set = True
							for disp in display:
								if disp in shot_file:
									not_set = False
									versions_list.append((path.getmtime(self.shot_directory + "/scenes/edits/" + shot_file), shot_file))

							if other:
								if "layout" not in shot_file and "blocking" not in shot_file and "splining" not in shot_file and "rendering" not in shot_file:
									versions_list.append((path.getmtime(self.shot_directory + "/scenes/edits/" + shot_file), shot_file))

		return sorted(versions_list, reverse = True)


	def getPlayblastsList(self):
		playblasts_list = []
		for playblast_file in listdir(self.shot_directory + "/movies/"):
			if path.splitext(playblast_file)[1] in (".mov", ".avi"):
				playblasts_list.append((path.getmtime(self.shot_directory + "/movies/" + playblast_file), playblast_file))

		return sorted(playblasts_list, reverse = True)


	def renameShot(self, new_name):
		new_dir = path.dirname(self.shot_directory) + "/" + new_name

		if not path.isdir(new_dir):
			try:
				rename(self.shot_directory, new_dir)

				for f in listdir(new_dir + "/scenes/"):
					if self.shot_name in f:
						rename(new_dir + "/scenes/" + f, new_dir + "/scenes/" + f .replace(self.shot_name, new_name))

				for f in listdir(new_dir + "/scenes/edits/"):
					if self.shot_name in f:
						rename(new_dir + "/scenes/edits/" + f, new_dir + "/scenes/edits/" + f.replace(self.shot_name, new_name))

				for f in listdir(new_dir + "/scenes/backup/"):
					if self.shot_name in f:
						rename(new_dir + "/scenes/backup/" + f, new_dir + "/scenes/backup/" + f.replace(self.shot_name, new_name))

				for f in listdir(new_dir + "/images/screenshots/"):
					if self.shot_name in f:
						rename(new_dir + "/images/screenshots/" + f, new_dir + "/images/screenshots/" + f.replace(self.shot_name, new_name))
			except Exception as e:
				print(e)
				return False

		self.shot_name = new_name
		self.shot_nb, self.sequence = Resources.makeShotNbs(new_name)
		self.shot_directory = new_dir

		return True


	def setDescription(self, description):
		self.description = description
		self.shot_settings.setSetting("description", self.description)
		self.shot_settings.saveSettings()


	def setDone(self, done):
		self.done = done
		self.shot_settings.setSetting("done", self.done)
		self.shot_settings.saveSettings()


	def setPriority(self, priority):
		self.priority = int(priority)
		self.shot_settings.setSetting("priority", self.priority)
		self.shot_settings.saveSettings()


	def setPercentage(self, percentage):
		self.percentage = percentage
		self.shot_settings.setSetting("percentage", self.percentage)
		self.shot_settings.saveSettings()


	def upgrade(self):
		version = 0
		version_str = ""

		if self.software == "maya":
			ext = ".ma"
		elif self.software == "blender":
			ext = ".blend"

		for file in listdir(self.shot_directory + "/images/screenshots/"):
			if self.step.lower() in file:
				tmp_version_str = path.splitext(file)[0][-2:]
				try:
					if int(tmp_version_str) > version:
						version = int(tmp_version_str)
						version_str = tmp_version_str
				except:
					print("IMPOSSIBLE TO CONVERT " + tmp_version_str + " INTO AN INTEGER")

		for file in listdir(self.shot_directory + "/scenes/"):
			if file[:7] == self.shot_name:
				file_to_upgrade = file

		if "file_to_upgrade" in locals():
			if self.step == "Layout":
				self.step = "Blocking"
			elif self.step == "Blocking":
				self.step = "Splining"
			elif self.step == "Splining":
				self.step = "Rendering"

			self.shot_settings.setSetting("step", self.step)
			self.shot_settings.saveSettings()

			if self.step == "Blocking":
				copyfile(self.shot_directory + "/scenes/" + file_to_upgrade, self.shot_directory + "/scenes/" + self.shot_name + "_02_blocking_v01" + ext)
				if version != 0:
					copyfile(self.shot_directory + "/images/screenshots/" + self.shot_name + "_01_layout_v" + version_str + ".jpg", self.shot_directory + "/images/screenshots/" + self.shot_name + "_02_blocking_v01.jpg")
			elif self.step == "Splining":
				copyfile(self.shot_directory + "/scenes/" + file_to_upgrade, self.shot_directory + "/scenes/" + self.shot_name + "_03_splining_v01" + ext)
				if version != 0:
					copyfile(self.shot_directory + "/images/screenshots/" + self.shot_name + "_02_blocking_v" + version_str + ".jpg", self.shot_directory + "/images/screenshots/" + self.shot_name + "_03_splining_v01.jpg")
			elif self.step == "Rendering":
				copyfile("assets/src/set_up_file_shot_" + self.software + ext, self.shot_directory + "/scenes/" + self.shot_name + "_04_rendering_v01" + ext)
				if version != 0:
					copyfile(self.shot_directory + "/images/screenshots/" + self.shot_name + "_03_splining_v" + version_str + ".jpg", self.shot_directory + "/images/screenshots/" + self.shot_name + "_04_rendering_v01.jpg")
			return True
		else:
			print("IMPOSSIBLE TO UPGRADE THIS FILE")
			return False


	def downgrade(self):
		if self.software == "maya":
			ext = ".ma"
		elif self.software == "blender":
			ext = ".blend"

		for file in listdir(self.shot_directory + "/scenes/"):
			if self.step.lower() in file:
				rename(self.shot_directory +"/scenes/" + file, self.shot_directory +"/scenes/backup/" + path.splitext(file)[0] + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + ext)

		for file in listdir(self.shot_directory + "/scenes/edits/"):
			if self.step.lower() in file:
				rename(self.shot_directory +"/scenes/edits/" + file, self.shot_directory +"/scenes/backup/" + path.splitext(file)[0] + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + ext)

		for file in listdir(self.shot_directory + "/images/screenshots/"):
			if self.step.lower() in file:
				remove(self.shot_directory + "/images/screenshots/" + file)

		if self.step == "Blocking":
			self.step = "Layout"
		elif self.step == "Splining":
			self.step = "Blocking"
		elif self.step == "Rendering":
			self.step = "Splining"

		self.shot_settings.setSetting("step", self.step)
		self.shot_settings.saveSettings()


	def validShot(dir_to_check=None):
		if not path.isdir(dir_to_check):
			return False

		if path.isdir(dir_to_check + "/superpipe"):
			if path.isdir(dir_to_check + "/scenes"):
				return True

		return False


	def createFolderHierarchy(self):
		if self.software == "maya" or self.software == "blender":
			xml_parser = XMLParser("./assets/xml/default_asset_struct.xml")
			xml_parser.parseXML(self.shot_directory)

		elif self.software == "houdini":
			xml_parser = XMLParser("./assets/xml/houdini_asset_struct.xml")
			xml_parser.parseXML(self.shot_directory)
