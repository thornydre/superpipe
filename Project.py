#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Main import *
from os import makedirs, listdir, path, rename, walk
from shutil import rmtree
from Shot import *
from Asset import *
from tkinter import *
from tkinter import messagebox
from Resources import *

import NewProjectDialog

class Project:
    def __init__(self, directory):
        self.shot_list = []
        self.asset_list = []

        self.current_sequence = 1
        self.selected_shot = None
        self.selected_asset = None
        self.directory = directory

        if not path.isdir(self.directory):
            makedirs(self.directory)

            makedirs(self.directory + "/01_donnee")

            makedirs(self.directory + "/02_ressources")

            makedirs(self.directory + "/03_preprod")
            makedirs(self.directory + "/03_preprod/character")
            makedirs(self.directory + "/03_preprod/coloscript")
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

        elif path.isdir(self.directory + "/05_shot"):
            self.updateShotList()
            self.updateAssetList()

            self.current_sequence = 1

            if self.shot_list:
                shot = Shot(self.directory, self.shot_list[-1][1])
                self.current_sequence = shot.getSequence()

        else:
            dialog = lambda: OkDialog.OkDialog("Set project", "'" + directory + "' is not a project folder")
            self.wait_window(dialog().top)

    def getShotList(self):
        return self.shot_list

    def getAssetList(self):
        return self.asset_list

    def updateShotList(self):
        self.shot_list = []
        for shot_name in listdir(self.directory + "/05_shot/"):
            if shot_name != "backup":
                shot = Shot(self.directory, shot_name)
                self.shot_list.append((shot.getShotNb(), shot.getShotName()))
                
    def updateAssetList(self):
        self.asset_list = []

        for asset in listdir(self.directory + "/04_asset/character"):
            self.asset_list.append((asset, "character"))

        for asset in listdir(self.directory + "/04_asset/FX"):
            self.asset_list.append((asset, "fx"))

        for asset in listdir(self.directory + "/04_asset/props"):
            self.asset_list.append((asset, "props"))

        for asset in listdir(self.directory + "/04_asset/set"):
            self.asset_list.append((asset, "set"))

    def getDirectory(self):
        return self.directory

    def getCurrentSequence(self):
        return self.current_sequence

    def getShot(self, shot_name):
        return Shot(self.directory, shot_name)

    def createShot(self, sequence):
        shot_nb = len(self.shot_list) + 1

        shot_name = Resources.makeShotName(shot_nb, sequence)

        shot = Shot(self.directory, shot_name)
        self.shot_list.append((shot.getShotNb(), shot.getShotName()))

    def removeShot(self, shot_name):
        shot = Shot(self.directory, shot_name)

        shot.deleteShot()

        for i in range(len(self.shot_list) - shot.getShotNb()):
            n = i + shot.getShotNb()

            cur_shot = Shot(self.directory, self.shot_list[n][1])

            if self.shot_list[n - 1][0] < 10:
                new_name = "s0" + str(cur_shot.getSequence()) + "p0" + str(self.shot_list[n - 1][0])
            else:
                new_name = "s0" + str(cur_shot.getSequence()) + "p" + str(self.shot_list[n - 1][0])

            cur_shot.renameShot(new_name)

        self.updateShotList()

    def moveShotUp(self, shot_name):
        shot = Shot(self.directory, shot_name)
        shot_name_backup = shot.getShotName()

        swap_shot = Shot(self.directory, self.shot_list[shot.getShotNb()][1])
        swap_shot_name_backup = swap_shot.getShotName()

        shot.renameShot("s00p00")

        swap_shot.renameShot(shot_name_backup)

        shot = Shot(self.directory, "s00p00")

        shot.renameShot(swap_shot_name_backup)

        # if path.isdir(self.directory + "05_shot/s00p00"):
        #     rmtree(self.directory + "05_shot/s00p00")

    def moveShotDown(self, shot_name):
        shot = Shot(self.directory, shot_name)
        shot_name_backup = shot.getShotName()

        swap_shot = Shot(self.directory, self.shot_list[shot.getShotNb() - 2][1])
        swap_shot_name_backup = swap_shot.getShotName()

        shot.renameShot("s00p00")

        swap_shot.renameShot(shot_name_backup)

        shot = Shot(self.directory, "s00p00")

        shot.renameShot(swap_shot_name_backup)

        # if path.isdir(self.directory + "05_shot/s00p00"):
        #     rmtree(self.directory + "05_shot/s00p00")

    def createAsset(self, asset_name, category):
        asset = Asset(self.directory, asset_name, category)
        self.asset_list.append((asset_name, category))

    def removeAsset(self, asset_name, category):
        asset = Asset(self.directory, asset_name, category)
        asset.deleteAsset()
        self.updateAssetList()

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

    def setSelection(self, shot_name = None, asset_name = None, asset_cat = None):
        if shot_name:
            self.selected_shot = Shot(self.directory, shot_name)
            self.selected_asset = None
        elif asset_name:
            self.selected_asset = Asset(self.directory, asset_name, asset_cat)
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

    def removeAllStudentVersions(self):
        for subdir, dirs, files in walk(self.directory + "/04_asset/"):
            for file in files:
                if file[-3:] == ".ma":
                    Resources.removeStudentVersion(path.join(subdir, file))

        for subdir, dirs, files in walk(self.directory + "/05_shot/"):
            for file in files:
                if file[-3:] == ".ma":
                    Resources.removeStudentVersion(path.join(subdir, file))
