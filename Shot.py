#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from os import makedirs, path, listdir, rename, remove
from tkinter import *
from shutil import copyfile, copytree, rmtree
from Resources import *

import time

class Shot:
	def __init__(self, directory = None, shot_name = None, software = None):
		self.shot_name = shot_name
		self.shot_nb, self.sequence = Resources.makeShotNbs(self.shot_name)
		self.shot_directory = directory + "/05_shot/" + self.shot_name
		self.postprod_directory = directory + "/06_postprod/" + self.shot_name
		self.done = 0
		self.priority = "Low"
		self.step = "Layout"
		self.frame_range = 200
		self.software = software

		if not path.isdir(self.shot_directory):
			if self.software:
				makedirs(self.shot_directory)

				makedirs(self.shot_directory + "/superpipe")

				with open(self.shot_directory + "/superpipe/shot_data.spi", "w") as f:
					f.write(str(self.done) + "\n" + self.priority + "\n" + self.step + "\n" + str(self.frame_range) + "\n" + self.software + "\n")
				f.close()

				open(self.shot_directory + "/superpipe/versions_data.spi", "a").close()

				if self.software == "maya" or self.software == "blender":
					makedirs(self.shot_directory + "/assets")
					
					makedirs(self.shot_directory + "/autosave")
					
					makedirs(self.shot_directory + "/cache")
					makedirs(self.shot_directory + "/cache/nCache")
					makedirs(self.shot_directory + "/cache/nCache/fluid")
					makedirs(self.shot_directory + "/cache/particles")

					makedirs(self.shot_directory + "/clips")
					
					makedirs(self.shot_directory + "/data")
					makedirs(self.shot_directory + "/data/edits")
					
					makedirs(self.shot_directory + "/images")
					makedirs(self.shot_directory + "/images/screenshots")
					
					makedirs(self.shot_directory + "/movies")
					
					makedirs(self.shot_directory + "/renderData")
					makedirs(self.shot_directory + "/renderData/depth")
					makedirs(self.shot_directory + "/renderData/fur")
					makedirs(self.shot_directory + "/renderData/fur/furAttrMap")
					makedirs(self.shot_directory + "/renderData/fur/furEqualMap")
					makedirs(self.shot_directory + "/renderData/fur/furFiles")
					makedirs(self.shot_directory + "/renderData/fur/furImages")
					makedirs(self.shot_directory + "/renderData/fur/furShadowMap")
					makedirs(self.shot_directory + "/renderData/iprImages")
					makedirs(self.shot_directory + "/renderData/shaders")
					
					makedirs(self.shot_directory + "/scenes")
					makedirs(self.shot_directory + "/scenes/backup")
					makedirs(self.shot_directory + "/scenes/edits")

					makedirs(self.shot_directory + "/scripts")
					
					makedirs(self.shot_directory + "/sound")
					
					makedirs(self.shot_directory + "/sourceimages")
					makedirs(self.shot_directory + "/sourceimages/3dPaintTextures")
					makedirs(self.shot_directory + "/sourceimages/edits")
					makedirs(self.shot_directory + "/sourceimages/environment")
					makedirs(self.shot_directory + "/sourceimages/imagePlane")
					makedirs(self.shot_directory + "/sourceimages/imageSequence")

					copyfile("src/workspace.mel", self.shot_directory + "/workspace.mel")

				elif self.software == "houdini":
					makedirs(self.shot_directory + "/abc")

					makedirs(self.shot_directory + "/audio")

					makedirs(self.shot_directory + "/backup")

					makedirs(self.shot_directory + "/comp")

					makedirs(self.shot_directory + "/desk")

					makedirs(self.shot_directory + "/flip")

					makedirs(self.shot_directory + "/geo")

					makedirs(self.shot_directory + "/hda")

					makedirs(self.shot_directory + "/render")

					makedirs(self.shot_directory + "/scripts")

					makedirs(self.shot_directory + "/sim")

					makedirs(self.shot_directory + "/tex")

					makedirs(self.shot_directory + "/video")

			else:
				print("ERROR1 : " + self.shot_name)

		elif Shot.validShot(self.shot_directory):
			if not path.isfile(self.shot_directory + "/superpipe/versions_data.spi"):
				open(self.shot_directory + "/superpipe/versions_data.spi", "a").close()

			if not path.isfile(self.shot_directory + "/superpipe/shot_data.spi"):
				with open(self.shot_directory + "/superpipe/shot_data.spi", "w") as f:
					f.write(str(self.done) + "\n" + self.priority + "\n" + self.step + "\n" + str(self.frame_range) + "\n" + self.software + "\n")
				f.close()

			if not Resources.readLine(self.shot_directory + "/superpipe/shot_data.spi", 4):
				Resources.writeAtLine(self.shot_directory + "/superpipe/shot_data.spi", "200", 4)

			shot_infos = []
			with open(self.shot_directory + "/superpipe/shot_data.spi", "r") as f:
				for l in f:
					shot_infos.append(l.strip("\n"))
			f.close()

			self.done = int(shot_infos[0])
			self.priority = shot_infos[1]
			self.step = shot_infos[2]
			self.frame_range = int(shot_infos[3])
			if len(shot_infos) > 4:
				self.software = shot_infos[4]
			else:
				self.software = "maya"

		else:
			print("ERROR2 : " + self.shot_name)

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

	def getSequence(self):
		return self.sequence

	def getPriority(self):
		return self.priority

	def getStep(self):
		return self.step

	def getFrameRange(self):
		return self.frame_range

	def getComment(self, version_file):
		if not path.isfile(self.shot_directory + "/superpipe/versions_data.spi"):
				open(self.shot_directory + "/superpipe/versions_data.spi", "a").close()
		else:
			with open(self.shot_directory + "/superpipe/versions_data.spi", "r") as f:
				all_comments = f.read()
			f.close()

			comment_list = all_comments.split("\n---\n")

			if comment_list[0]:
				i = 1

				for comment in comment_list:
					if comment == version_file:
						if comment_list[i]:
							return comment_list[i]
						else:
							return "No comment"

					i += 1
			else:
				return "No comment"

		return "No comment"

	def isDone(self):
		if self.done == 1:
			return True
		else:
			return False

	def setShot(self, res):
		if self.software == "maya":
			copyfile("src/set_up_file_shot_maya.ma", self.shot_directory + "/scenes/" + self.shot_name + "_01_layout_v01.ma")
			Resources.insertAtLine(self.shot_directory + "/scenes/" + self.shot_name + "_01_layout_v01.ma", "setAttr \"sceneConfigurationScriptNode.b\" -type \"string\" \"playbackOptions -min 1001 -max " + str(1000 + self.frame_range) + " -ast 1001 -aet " + str(1000 + self.frame_range) + "\";\nselect -ne :defaultResolution;\n\tsetAttr \".w\" " + str(res[0]) + ";\n\tsetAttr \".h\" " + str(res[1]) + ";", -1)
		elif self.software == "blender":
			copyfile("src/set_up_file_shot_blender.blend", self.shot_directory + "/scenes/" + self.shot_name + "_01_layout_v01.blend")

	def setFrameRange(self, frame_range):
		self.frame_range = frame_range

		if path.isdir(self.shot_directory + "/scenes/.mayaSwatches"):
					rmtree(self.shot_directory + "/scenes/.mayaSwatches")

		Resources.writeAtLine(self.shot_directory + "/superpipe/shot_data.spi", str(self.frame_range), 4)

		for file in listdir(self.shot_directory + "/scenes/"):
			if path.splitext(file)[1] == ".ma":
				Resources.insertAtLine(self.shot_directory + "/scenes/" + file, "setAttr \"sceneConfigurationScriptNode.b\" -type \"string\" \"playbackOptions -min 1001 -max " + str(1000 + frame_range) + " -ast 1001 -aet " + str(1000 + frame_range) + "\";", -1)

	def setResolution(self, res):
		if path.isdir(self.shot_directory + "/scenes/.mayaSwatches"):
					rmtree(self.shot_directory + "/scenes/.mayaSwatches")

		for file in listdir(self.shot_directory + "/scenes/"):
			if path.splitext(file)[1] == ".ma":
				Resources.insertAtLine(self.shot_directory + "/scenes/" + file, "select -ne :defaultResolution;\n\tsetAttr \".w\" " + str(res[0]) + ";\n\tsetAttr \".h\" " + str(res[1]) + ";", -1)

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
				return False

		self.shot_name = new_name
		self.shot_nb, self.sequence = Resources.makeShotNbs(new_name)
		self.shot_directory = new_dir

		return True

	def setDone(self, done):
		self.done = done
		Resources.writeAtLine(self.shot_directory + "/superpipe/shot_data.spi", str(self.done), 1)

	def setPriority(self, priority):
		self.priority = priority
		Resources.writeAtLine(self.shot_directory + "/superpipe/shot_data.spi", self.priority, 2)

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
			if file[:6] == self.shot_name:
				file_to_upgrade = file

		if "file_to_upgrade" in locals():
			if self.step == "Layout":
				self.step = "Blocking"
			elif self.step == "Blocking":
				self.step = "Splining"
			elif self.step == "Splining":
				self.step = "Rendering"

			Resources.writeAtLine(self.shot_directory + "/superpipe/shot_data.spi", self.step, 3)

			if self.step == "Blocking":
				copyfile(self.shot_directory + "/scenes/" + file_to_upgrade, self.shot_directory + "/scenes/" + self.shot_name + "_02_blocking_v01" + ext)
				if version != 0:
					copyfile(self.shot_directory + "/images/screenshots/" + self.shot_name + "_01_layout_v" + version_str + ".jpg", self.shot_directory + "/images/screenshots/" + self.shot_name + "_02_blocking_v01.jpg")
			elif self.step == "Splining":
				copyfile(self.shot_directory + "/scenes/" + file_to_upgrade, self.shot_directory + "/scenes/" + self.shot_name + "_03_splining_v01" + ext)
				if version != 0:
					copyfile(self.shot_directory + "/images/screenshots/" + self.shot_name + "_02_blocking_v" + version_str + ".jpg", self.shot_directory + "/images/screenshots/" + self.shot_name + "_03_splining_v01.jpg")
			elif self.step == "Rendering":
				copyfile("src/set_up_file_shot_" + self.software + ext, self.shot_directory + "/scenes/" + self.shot_name + "_04_rendering_v01" + ext)
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

		Resources.writeAtLine(self.shot_directory + "/superpipe/shot_data.spi", self.step, 3)

	def validShot(dir_to_check = None):
		if not path.isdir(dir_to_check):
			return False

		if path.isdir(dir_to_check + "/superpipe"):
			if path.isdir(dir_to_check + "/scenes"):
				return True

		return False
