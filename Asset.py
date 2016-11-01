#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from os import makedirs, path
from tkinter import *
from shutil import copyfile, copytree

import time

class Asset:
    def __init__(self, directory = None, asset_name = None, category = None):
        self.asset_name = asset_name

        self.category = category

        self.directory = directory + "/04_asset/" + self.category + "/" + self.asset_name

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

    def getAssetName(self):
        return self.asset_name

    def getDirectory(self):
        return self.directory

    def getCategory(self):
        return self.category

    def setAsset(self):
        copyfile("src/set_up_file_asset.ma", self.directory + "/scenes/" + self.asset_name + "_v01.ma")

    def isSet(self):
        for asset_file in listdir(self.directory + "/scenes/"):
            if asset_file[-3:] == ".ma":
                return True

        return False

    def deleteAsset(self):
        copytree(self.directory, self.directory +"/../backup/" + self.asset_name + "_" + time.strftime("%Y_%m_%d_%H_%M_%S"))
        rmtree(self.directory)

    def getVersionsList(self, last_only):
        versions_list = []
        for asset_file in listdir(self.directory + "/scenes/"):
            if asset_file[-3:] == ".ma":
                versions_list.append(asset_file)

        if not last_only:
            for asset_file in listdir(self.directory + "/scenes/edits/"):
                if asset_file[-3:] == ".ma":
                    versions_list.append(asset_file)

        return versions_list

    def renameAsset(self, new_name):
        new_dir = path.dirname(self.directory) + "/" + new_name

        if not path.isdir(new_dir):
            rename(self.directory, new_dir)

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

            return True

        else:
            return False