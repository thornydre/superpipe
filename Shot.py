#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from os import makedirs, path, listdir, rename, remove
from tkinter import *
from shutil import copyfile, copytree, rmtree
from Resources import *

import time

class Shot:
    def __init__(self, directory = None, shot_name = None):
        self.shot_name = shot_name
        self.shot_nb, self.sequence = Resources.makeShotNbs(self.shot_name)
        self.directory = directory + "/05_shot/" + self.shot_name
        self.done = 0
        self.priority = "Low"
        self.step = "Layout"
        self.frame_range = 200

        if not path.isdir(self.directory):
            makedirs(self.directory)

            makedirs(self.directory + "/assets")
            
            makedirs(self.directory + "/autosave")
            
            makedirs(self.directory + "/cache")
            makedirs(self.directory + "/cache/nCache")
            makedirs(self.directory + "/cache/nCache/fluid")
            makedirs(self.directory + "/cache/particles")

            makedirs(self.directory + "/clips")
            
            makedirs(self.directory + "/data")
            makedirs(self.directory + "/data/edits")
            with open(self.directory + "/data/shot_data.spi", "w") as f:
                f.write(str(self.done) + "\n" + self.priority + "\n" + self.step + "\n" + str(self.frame_range) + "\n")
            f.close()

            open(self.directory + "/data/versions_data.spi", "a").close()
            
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
            makedirs(self.directory + "/sourceimages/3dPatinTextures")
            makedirs(self.directory + "/sourceimages/edits")
            makedirs(self.directory + "/sourceimages/environement")
            makedirs(self.directory + "/sourceimages/imagePlane")
            makedirs(self.directory + "/sourceimages/imageSequence")

            copyfile("src/workspace.mel", self.directory + "/workspace.mel")

        else:
            if not path.isfile(self.directory + "/data/versions_data.spi"):
                open(self.directory + "/data/versions_data.spi", "a").close()

            if not path.isfile(self.directory + "/data/shot_data.spi"):
                with open(self.directory + "/data/shot_data.spi", "w") as f:
                    f.write(str(self.done) + "\n" + self.priority + "\n" + self.step + "\n" + str(self.frame_range) + "\n")
                f.close()

            if not Resources.readLine(self.directory + "/data/shot_data.spi", 4):
                Resources.writeAtLine(self.directory + "/data/shot_data.spi", "200", 4)

            shot_infos = []
            with open(self.directory + "/data/shot_data.spi", "r") as f:
                for l in f:
                    shot_infos.append(l.strip("\n"))
            f.close()

            self.done = int(shot_infos[0])
            self.priority = shot_infos[1]
            self.step = shot_infos[2]
            self.frame_range = int(shot_infos[3])

    def getShotNb(self):
        return self.shot_nb

    def getShotName(self):
        return self.shot_name

    def getDirectory(self):
        return self.directory

    def getSequence(self):
        return self.sequence

    def getPriority(self):
        return self.priority

    def getStep(self):
        return self.step

    def getFrameRange(self):
        return self.frame_range

    def getComment(self, version_file):
        if not path.isfile(self.directory + "/data/versions_data.spi"):
                open(self.directory + "/data/versions_data.spi", "a").close()
        else:
            with open(self.directory + "/data/versions_data.spi", "r") as f:
                all_comments = f.read()
            f.close()

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

    def setShot(self, res):
        copyfile("src/set_up_file_shot.ma", self.directory + "/scenes/" + self.shot_name + "_01_layout_v01.ma")

        Resources.insertAtLine(self.directory + "/scenes/" + self.shot_name + "_01_layout_v01.ma", "setAttr \"sceneConfigurationScriptNode.b\" -type \"string\" \"playbackOptions -min 1001 -max " + str(1000 + self.frame_range) + " -ast 1001 -aet " + str(1000 + self.frame_range) + "\";\nselect -ne :defaultResolution;\n\tsetAttr \".w\" " + str(res[0]) + ";\n\tsetAttr \".h\" " + str(res[1]) + ";", -1)

    def setFrameRange(self, frame_range):
        self.frame_range = frame_range

        if path.isdir(self.directory + "/scenes/.mayaSwatches"):
                    rmtree(self.directory + "/scenes/.mayaSwatches")

        Resources.writeAtLine(self.directory + "/data/shot_data.spi", str(self.frame_range), 4)

        for file in listdir(self.directory + "/scenes/"):
            if ".ma" in file:
                Resources.insertAtLine(self.directory + "/scenes/" + file, "setAttr \"sceneConfigurationScriptNode.b\" -type \"string\" \"playbackOptions -min 1001 -max " + str(1000 + frame_range) + " -ast 1001 -aet " + str(1000 + frame_range) + "\";", -1)

    def setResolution(self, res):
        if path.isdir(self.directory + "/scenes/.mayaSwatches"):
                    rmtree(self.directory + "/scenes/.mayaSwatches")

        for file in listdir(self.directory + "/scenes/"):
            if ".ma" in file:
                Resources.insertAtLine(self.directory + "/scenes/" + file, "select -ne :defaultResolution;\n\tsetAttr \".w\" " + str(res[0]) + ";\n\tsetAttr \".h\" " + str(res[1]) + ";", -1)

    def isSet(self):
        for shot_file in listdir(self.directory + "/scenes/"):
            if shot_file[-3:] == ".ma":
                return True

        return False

    def deleteShot(self):
        copytree(self.directory, self.directory +"/../backup/" + self.shot_name + "_" + time.strftime("%Y_%m_%d_%H_%M_%S"))
        rmtree(self.directory)

    def getVersionsList(self, last_only):
        versions_list = []
        for shot_file in listdir(self.directory + "/scenes/"):
            if not "reference" in shot_file:
                if shot_file[-3:] == ".ma":
                    versions_list.append((path.getctime(self.directory + "/scenes/" + shot_file), shot_file))

        if not last_only:
            for shot_file in listdir(self.directory + "/scenes/edits/"):
                if shot_file[-3:] == ".ma":
                    versions_list.append((path.getctime(self.directory + "/scenes/edits/" + shot_file), shot_file))

        return sorted(versions_list, reverse = True)

    def renameShot(self, new_name):
        new_dir = path.dirname(self.directory) + "/" + new_name

        if not path.isdir(new_dir):
            rename(self.directory, new_dir)

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

    def setDone(self, done):
        self.done = done
        Resources.writeAtLine(self.directory + "/data/shot_data.spi", str(self.done), 1)

    def setPriority(self, priority):
        self.priority = priority
        Resources.writeAtLine(self.directory + "/data/shot_data.spi", self.priority, 2)

    def upgrade(self):
        version = 0
        version_str = ""

        for file in listdir(self.directory + "/images/screenshots/"):
            if self.step.lower() in file:
                if not "small" in file:
                    tmp_version_str = file.strip(".gif")[-2:]
                    if int(tmp_version_str) > version:
                        version = int(tmp_version_str)
                        version_str = tmp_version_str

        if self.step == "Layout":
            self.step = "Blocking"
        elif self.step == "Blocking":
            self.step = "Splining"
        elif self.step == "Splining":
            self.step = "Rendering"

        Resources.writeAtLine(self.directory + "/data/shot_data.spi", self.step, 3)

        for file in listdir(self.directory + "/scenes/"):
            if file[:6] == self.shot_name:
                file_to_upgrade = file

        if self.step == "Blocking":
            copyfile(self.directory + "/scenes/" + file_to_upgrade, self.directory + "/scenes/" + self.shot_name + "_02_blocking_v01.ma")
            if version != 0:
                copyfile(self.directory + "/images/screenshots/" + self.shot_name + "_01_layout_v" + version_str + ".gif", self.directory + "/images/screenshots/" + self.shot_name + "_02_blocking_v01.gif")
                copyfile(self.directory + "/images/screenshots/" + self.shot_name + "_01_layout_v" + version_str + "_small.gif", self.directory + "/images/screenshots/" + self.shot_name + "_02_blocking_v01_small.gif")
        elif self.step == "Splining":
            copyfile(self.directory + "/scenes/" + file_to_upgrade, self.directory + "/scenes/" + self.shot_name + "_03_splining_v01.ma")
            if version != 0:
                copyfile(self.directory + "/images/screenshots/" + self.shot_name + "_02_blocking_v" + version_str + ".gif", self.directory + "/images/screenshots/" + self.shot_name + "_03_splining_v01.gif")
                copyfile(self.directory + "/images/screenshots/" + self.shot_name + "_02_blocking_v" + version_str + "_small.gif", self.directory + "/images/screenshots/" + self.shot_name + "_03_splining_v01_small.gif")
        elif self.step == "Rendering":
            copyfile("src/set_up_file_shot.ma", self.directory + "/scenes/" + self.shot_name + "_04_rendering_v01.ma")
            if version != 0:
                copyfile(self.directory + "/images/screenshots/" + self.shot_name + "_03_splining_v" + version_str + ".gif", self.directory + "/images/screenshots/" + self.shot_name + "_04_rendering_v01.gif")
                copyfile(self.directory + "/images/screenshots/" + self.shot_name + "_03_splining_v" + version_str + "_small.gif", self.directory + "/images/screenshots/" + self.shot_name + "_04_rendering_v01_small.gif")

    def downgrade(self):
        for file in listdir(self.directory + "/scenes/"):
            if self.step.lower() in file:
                rename(self.directory +"/scenes/" + file, self.directory +"/scenes/backup/" + file.strip(".ma") + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + ".ma")

        for file in listdir(self.directory + "/scenes/edits/"):
            if self.step.lower() in file:
                rename(self.directory +"/scenes/edits/" + file, self.directory +"/scenes/backup/" + file.strip(".ma") + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + ".ma")

        for file in listdir(self.directory + "/images/screenshots/"):
            if self.step.lower() in file:
                remove(self.directory + "/images/screenshots/" + file)

        if self.step == "Blocking":
            self.step = "Layout"
        elif self.step == "Splining":
            self.step = "Blocking"
        elif self.step == "Rendering":
            self.step = "Splining"

        Resources.writeAtLine(self.directory + "/data/shot_data.spi", self.step, 3)
