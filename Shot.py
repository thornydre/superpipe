#!/usr/bin/python

from os import makedirs, remove
from shutil import copyfile, copytree, rmtree
from pathlib import Path
from Resources import *
from Settings import *
from XMLParser import *

import time
import subprocess


class Shot:
	def __init__(self, project_dir=None, shot_name=None, software=None):
		self.shot_name = shot_name
		self.shot_nb, self.sequence = Resources.makeShotNbs(self.shot_name)
		self.shot_dir = Path(f"{project_dir}/05_shot/{self.shot_name}")
		self.superpipe_dir = Path(f"{self.shot_dir}/superpipe")
		self.software = software
		self.general_settings = Settings("assets/settings.spi")
		self.general_settings.loadGeneralSettings()

		if not self.shot_dir.is_dir():
			if self.software:
				makedirs(self.shot_dir)

				makedirs(self.superpipe_dir)

				self.createFolderHierarchy()

			else:
				print("ERROR1 : " + self.shot_name)

		elif not Shot.validShot(self.shot_dir):
			print("ERROR2 : " + self.shot_name)

		## SETTINGS ##
		self.versions_settings = Settings(f"{self.superpipe_dir}/versions_data.spi")
		self.versions_settings.loadVersionSettings()

		self.shot_settings = Settings(f"{self.superpipe_dir}/shot_data.spi")
		self.shot_settings.loadShotSettings()

		self.done = self.shot_settings.getSetting("done")
		self.priority = self.shot_settings.getSetting("priority")
		self.step = self.shot_settings.getSetting("step")
		self.percentage = self.shot_settings.getSetting("percentage")
		self.frame_range = self.shot_settings.getSetting("frame_range")
		self.description = self.shot_settings.getSetting("description")
		if self.software:
			self.shot_settings.setSetting("software", self.software)
			self.shot_settings.saveSettings()
		else:
			self.software = self.shot_settings.getSetting("software")

		extensions = {"maya":".ma", "blender":".blend", "houdini":".hip"}

		self.extension = extensions[self.software]

		self.setTaggedPaths()


	def getShotNb(self):
		return self.shot_nb


	def getShotName(self):
		return self.shot_name


	def getDirectory(self):
		return str(self.shot_dir)


	def getPictsPath(self):
		return str(self.screenshot_dir)


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
			copyfile("assets/src/set_up_file_shot_maya.ma", f"{self.scenes_dir}/{self.shot_name}_01_layout_v01.ma")
			Resources.insertAtLine(f"{self.scenes_dir}/{self.shot_name}_01_layout_v01.ma", "setAttr \"sceneConfigurationScriptNode.b\" -type \"string\" \"playbackOptions -min 1001 -max " + str(1000 + self.frame_range) + " -ast 1001 -aet " + str(1000 + self.frame_range) + "\";\nselect -ne :defaultResolution;\n\tsetAttr \".w\" " + str(res[0]) + ";\n\tsetAttr \".h\" " + str(res[1]) + ";", -1)
		elif self.software == "blender":
			copyfile("assets/src/set_up_file_shot_blender.blend", f"{self.scenes_dir}/{self.shot_name}_01_layout_v01.blend")


	def setFrameRange(self, frame_range):
		self.frame_range = frame_range

		if Path(f"{self.scenes_dir}/.mayaSwatches").is_dir():
			rmtree(f"{self.scenes_dir}/.mayaSwatches")

		self.shot_settings.setSetting("frame_range", self.frame_range)
		self.shot_settings.saveSettings()

		for file in self.scenes_dir.iterdir():
			if file.suffix == ".ma":
				Resources.insertAtLine(str(file), "setAttr \"sceneConfigurationScriptNode.b\" -type \"string\" \"playbackOptions -min 1001 -max " + str(1000 + frame_range) + " -ast 1001 -aet " + str(1000 + frame_range) + "\";", -1)
			elif file.suffix == ".blend":
				text = ("import bpy\n"
				"bpy.ops.wm.open_mainfile(filepath=\"{0}\")\n"
				"bpy.context.scene.frame_start = {1}\n"
				"bpy.context.scene.frame_end = {2}\n"
				"bpy.context.scene.frame_current = {1}\n"
				"bpy.ops.wm.save_mainfile()\n"
				"bpy.ops.wm.quit_blender()").format(f"{self.scenes_dir}/{file}", 1001, 1000 + frame_range)

				subprocess.Popen([self.general_settings.getSetting("blender_path"), "-b", "--python-expr", text])


	def setResolution(self, res):
		if Path(f"{self.scenes_dir}/.mayaSwatches").is_dir():
			rmtree(f"{self.scenes_dir}/.mayaSwatches")

		for file in self.scenes_dir.iterdir():
			if file.suffix == ".ma":
				Resources.insertAtLine(str(file), "select -ne :defaultResolution;\n\tsetAttr \".w\" " + str(res[0]) + ";\n\tsetAttr \".h\" " + str(res[1]) + ";", -1)
			elif file.suffix == ".blend":
				print("blender file")


	def isSet(self):
		if self.software == "maya":
			for shot_file in self.scenes_dir.iterdir():
				if shot_file.suffix == ".ma":
					return True

		elif self.software == "blender":
			for shot_file in self.scenes_dir.iterdir():
				if shot_file.suffix == ".blend":
					return True

		return False


	def deleteShot(self):
		copytree(self.shot_dir, f"{self.shot_dir.parent}/backup/{self.shot_name}_{time.strftime('%Y_%m_%d_%H_%M_%S')}")
		rmtree(self.shot_dir)


	def getVersionsList(self, last_only, layout, blocking, splining, rendering, other):
		if not self.scenes_dir.is_dir():
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
			for shot_file in self.scenes_dir.iterdir():
				if not "reference" in shot_file.parts:
					if shot_file.name[0] != "_":
						if shot_file.suffix == ".ma":
							for disp in display:
								if disp in shot_file.name:
									versions_list.append((shot_file.stat().st_mtime, shot_file.name))

							if other:
								if "layout" not in shot_file.name and "blocking" not in shot_file.name and "splining" not in shot_file.name and "rendering" not in shot_file.name:
									versions_list.append((shot_file.stat().st_mtime, shot_file.name))

			if not last_only:
				for shot_file in Path(f"{self.scenes_dir}/edits/").iterdir():
					if shot_file.name[0] != "_":
						if shot_file.suffix == ".ma":
							not_set = True
							for disp in display:
								if disp in shot_file.name:
									not_set = False
									versions_list.append((shot_file.stat().st_mtime, shot_file.name))

							if other:
								if "layout" not in shot_file.name and "blocking" not in shot_file.name and "splining" not in shot_file.name and "rendering" not in shot_file.name:
									versions_list.append((shot_file.stat().st_mtime, shot_file.name))

		elif self.software == "blender":
			for shot_file in self.scenes_dir.iterdir():
				if not "reference" in shot_file.parts:
					if shot_file.name[0] != "_":
						if shot_file.suffix == ".blend":
							for disp in display:
								if disp in shot_file.name:
									versions_list.append((shot_file.stat().st_mtime, shot_file.name))

							if other:
								if "layout" not in shot_file.name and "blocking" not in shot_file.name and "splining" not in shot_file.name and "rendering" not in shot_file.name:
									versions_list.append((shot_file.stat().st_mtime, shot_file.name))

			if not last_only:
				for shot_file in Path(f"{self.scenes_dir}/edits/").iterdir():
					if shot_file.name[0] != "_":
						if shot_file.suffix == ".blend":
							not_set = True
							for disp in display:
								if disp in shot_file.name:
									not_set = False
									versions_list.append((shot_file.stat().st_mtime, shot_file.name))

							if other:
								if "layout" not in shot_file.name and "blocking" not in shot_file.name and "splining" not in shot_file.name and "rendering" not in shot_file.name:
									versions_list.append((shot_file.stat().st_mtime, shot_file.name))

		return sorted(versions_list, reverse=True)


	def getPlayblastsList(self):
		playblasts_list = []
		for playblast_file in self.playblast_dir.iterdir():
			if playblast_file.suffix in (".mov", ".avi"):
				playblasts_list.append((playblast_file.stat().st_mtime, playblast_file.name))

		return sorted(playblasts_list, reverse=True)


	def renameShot(self, new_name):
		new_dir = Path(f"{self.shot_dir.parent}/{new_name}")

		if not new_dir.is_dir():
			try:
				self.shot_dir.rename(new_dir)

				subfolders_list = ["/scenes/", "/scenes/edits/", "/scenes/backup/", "/images/screenshots/"]

				for subfolder in subfolders_list:
					for f in Path(f"{new_dir}{subfolder}").iterdir():
						if self.shot_name in f.parts[-1]:
							f.rename(str(f).replace(self.shot_name, new_name))
							print(f"RENAME : {str(f)} TO {str(f).replace(self.shot_name, new_name)}")

			except Exception as e:
				print(e)
				return False

		self.shot_name = new_name
		self.shot_nb, self.sequence = Resources.makeShotNbs(new_name)
		self.shot_dir = new_dir

		print("#####################")

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

		for file in self.screenshot_dir.iterdir():
			if self.step.lower() in file.name:
				tmp_version_str = file.stem[-2:]
				try:
					if int(tmp_version_str) > version:
						version = int(tmp_version_str)
						version_str = tmp_version_str
				except:
					print("IMPOSSIBLE TO CONVERT " + tmp_version_str + " INTO AN INTEGER")

		for file in self.scenes_dir.iterdir():
			if file.name[:7] == self.shot_name:
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
				copyfile(file_to_upgrade, f"{self.shot_dir}/scenes/{self.shot_name}_02_blocking_v01{ext}")
				if version != 0:
					copyfile(f"{self.screenshot_dir}/{self.shot_name}_01_layout_v{version_str}.jpg", f"{self.screenshot_dir}/{self.shot_name}_02_blocking_v01.jpg")
			elif self.step == "Splining":
				copyfile(file_to_upgrade, f"{self.shot_dir}/scenes/{self.shot_name}_03_splining_v01{ext}")
				if version != 0:
					copyfile(f"{self.screenshot_dir}/{self.shot_name}_02_blocking_v{version_str}.jpg", f"{self.screenshot_dir}/{self.shot_name}_03_splining_v01.jpg")
			elif self.step == "Rendering":
				copyfile(f"assets/src/set_up_file_shot_{self.software}{ext}", f"{self.scenes_dir}/{self.shot_name}_04_rendering_v01{ext}")
				if version != 0:
					copyfile(f"{self.screenshot_dir}/{self.shot_name}_03_splining_v{version_str}.jpg", f"{self.screenshot_dir}/{self.shot_name}_04_rendering_v01.jpg")
			return True
		else:
			print("IMPOSSIBLE TO UPGRADE THIS FILE")
			return False


	def downgrade(self):
		if self.software == "maya":
			ext = ".ma"
		elif self.software == "blender":
			ext = ".blend"

		for file in self.scenes_dir.iterdir():
			if self.step.lower() in file.name:
				file.rename(f"{file.parent}/backup/{file.name}_{time.strftime('%Y_%m_%d_%H_%M_%S')}{ext}")

		for file in Path(f"{self.scenes_dir}/edits/").iterdir():
			if self.step.lower() in file.name:
				file.rename(f"{file.parent}/backup/{file.name}_{time.strftime('%Y_%m_%d_%H_%M_%S')}{ext}")

		for file in self.screenshot_dir.iterdir():
			if self.step.lower() in file.name:
				remove(file)

		if self.step == "Blocking":
			self.step = "Layout"
		elif self.step == "Splining":
			self.step = "Blocking"
		elif self.step == "Rendering":
			self.step = "Splining"

		self.shot_settings.setSetting("step", self.step)
		self.shot_settings.saveSettings()


	def validShot(dir_to_check=None):
		if not Path(dir_to_check).is_dir():
			return False

		if Path(f"{dir_to_check}/superpipe").is_dir():
			if Path(f"{dir_to_check}/scenes").is_dir():
				return True

		return False


	def createFolderHierarchy(self):
		xml_parser = XMLParser("./assets/xml/default_asset_struct.xml")
		xml_parser.parseXML(str(self.shot_dir))


	def setTaggedPaths(self):
		xml_parser = XMLParser("./assets/xml/default_asset_struct.xml")

		tagged_paths = xml_parser.pathToTag(str(self.shot_dir))

		self.screenshot_dir = Path(tagged_paths["screenshot_dir"])
		self.playblast_dir = Path(tagged_paths["playblast_dir"])
		self.scenes_dir = Path(tagged_paths["scenes_dir"])
