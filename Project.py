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
        self.res_x = 1920
        self.res_y = 1080
        self.valid = True

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

            with open(self.directory + "/project_option.spi", "w") as f:
                f.write("www.google.fr\n")
                f.write("1920x1080\n")
            f.close()

        elif path.isdir(self.directory + "/05_shot"):
            self.updateShotList()
            self.updateAssetList()

            if not Resources.readLine(self.directory + "/project_option.spi", 2):
                Resources.writeAtLine(self.directory + "/project_option.spi", "1920x1080", 2)

            res = Resources.readLine(self.directory + "/project_option.spi", 2).split("x")

            self.res_x = res[0]
            self.res_y = res[1]

            self.current_sequence = 1

            if self.shot_list:
                shot = Shot(self.directory, self.shot_list[-1][1])
                self.current_sequence = shot.getSequence()

        else:
            self.valid = False

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

        for cur_dir, sub_dirs, files in walk(self.directory + "/04_asset"):
            if "scenes" in sub_dirs:
                if not "backup" in cur_dir:
                    self.asset_list.append((path.basename(cur_dir), "/" + path.dirname(cur_dir.replace("\\", "/")).replace(self.directory + "/04_asset", "")))

    def getDirectory(self):
        return self.directory

    def getCurrentSequence(self):
        return self.current_sequence

    def getShot(self, shot_name):
        return Shot(self.directory, shot_name)

    def isValid(self):
        return self.valid

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

    def createAsset(self, asset_name, second_path):
        if path.isdir(self.directory + "/04_asset/" + second_path + "/" + asset_name):
            return False
        elif path.isdir(self.directory + "/04_asset/" + second_path + "/" + asset_name):
            return False
        elif path.isdir(self.directory + "/04_asset/" + second_path + "/" + asset_name):
            return False
        elif path.isdir(self.directory + "/04_asset/" + second_path + "/" + asset_name):
            return False
        else:
            asset = Asset(self.directory, second_path, asset_name)
            self.asset_list.append((asset_name, second_path))
            return True

    def removeAsset(self, asset_name, second_path):
        asset = Asset(self.directory, second_path, asset_name)
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

    def setSelection(self, shot_name = None, asset_name = None, second_path = None):
        if shot_name:
            self.selected_shot = Shot(self.directory, shot_name)
            self.selected_asset = None
        elif asset_name:
            self.selected_asset = Asset(self.directory, second_path, asset_name)
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

    def setResolution(self, res):
        self.res_x = res[0]
        self.res_y = res[1]

        Resources.writeAtLine(self.getDirectory() + "/project_option.spi", self.res_x + "x" + self.res_y, 2)

    def setAllShotsRes(self):
        for shot in listdir(self.getDirectory() + "/05_shot/"):
            if shot != "backup":
                cur_shot = Shot(self.getDirectory(), shot)
                cur_shot.setResolution(self.getResolution())

    def getResolution(self):
        return (self.res_x, self.res_y)