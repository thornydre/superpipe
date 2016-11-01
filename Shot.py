#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from os import makedirs, path, listdir, rename
from tkinter import *
from shutil import copyfile, copytree, rmtree
from Resources import *

import time

class Shot:
    def __init__(self, directory = None, shot_name = None):
        self.shot_name = shot_name
        self.shot_nb, self.sequence = Resources.makeShotNbs(self.shot_name)
        self.directory = directory + "/05_shot/" + self.shot_name

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

    def getShotNb(self):
        return self.shot_nb

    def getShotName(self):
        return self.shot_name

    def getDirectory(self):
        return self.directory

    def getSequence(self):
        return self.sequence

    def setShot(self):
        copyfile("src/set_up_file_shot.ma", self.directory + "/scenes/" + self.shot_name + "_01_layout_v01.ma")
        copyfile("src/set_up_file_shot.ma", self.directory + "/scenes/" + self.shot_name + "_02_blocking_v01.ma")
        copyfile("src/set_up_file_shot.ma", self.directory + "/scenes/" + self.shot_name + "_03_splining_v01.ma")
        copyfile("src/set_up_file_shot.ma", self.directory + "/scenes/" + self.shot_name + "_04_rendering_v01.ma")

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
            if shot_file[-3:] == ".ma":
                versions_list.append(shot_file)

        if not last_only:
            for shot_file in listdir(self.directory + "/scenes/edits/"):
                if shot_file[-3:] == ".ma":
                    versions_list.append(shot_file)

        return versions_list

    def renameShot(self, new_name):
        new_dir = path.dirname(self.directory) + "/" + new_name

        if not path.isdir(new_dir):
            rename(self.directory, new_dir)

            for f in listdir(new_dir + "/scenes/"):
                if self.shot_name in f:
                    rename(new_dir + "/scenes/" + f, new_dir + "/scenes/" + f.replace(self.shot_name, new_name))

            for f in listdir(new_dir + "/scenes/edits/"):
                if self.shot_name in f:
                    rename(new_dir + "/scenes/edits/" + f, new_dir + "/scenes/edits/" + f.replace(self.shot_name, new_name))

            for f in listdir(new_dir + "/scenes/backup/"):
                if self.shot_name in f:
                    rename(new_dir + "/scenes/backup/" + f, new_dir + "/scenes/backup/" + f.replace(self.shot_name, new_name))

            for f in listdir(new_dir + "/images/screenshots/"):
                if self.shot_name in f:
                    rename(new_dir + "/images/screenshots/" + f, new_dir + "/images/screenshots/" + f.replace(self.shot_name, new_name))
        else:
            print("va te faire foutre !")