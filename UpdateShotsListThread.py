#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir
from tkinter import *
from Shot import *

import threading
import OkDialog

class UpdateShotsListThread(threading.Thread):
    def __init__(self, project, shot_list, frame):
        threading.Thread.__init__(self)

        self.current_project = project
        
        self.previous_dirs = []

        self.shot_list = shot_list

        self.frame = frame

        self.active = True

    def run(self):
        while self.active:
            if listdir(self.current_project.getDirectory() + "/05_shot/") != self.previous_dirs:
                self.frame.config(cursor = "wait")
                self.frame.update()
                
                self.shot_list.delete(0, END)

                shots = self.current_project.getShotList()

                for shot in shots:
                    if path.isdir(self.current_project.getDirectory() + "/05_shot/" + shot[1]):
                        if Shot.validShot(self.current_project.getDirectory() + "/05_shot/" + shot[1]):
                            self.shot_list.insert(shot[0], shot[1])

                            cur_shot = Shot(self.current_project.getDirectory(), shot[1])

                            if cur_shot.isDone():
                                self.shot_list.itemconfig(shot[0] - 1, bg = "#89C17F", selectbackground = "#466341")
                            elif cur_shot.getPriority() == "Urgent":
                                self.shot_list.itemconfig(shot[0] - 1, bg = "#E55252", selectbackground = "#822121")
                            elif cur_shot.getPriority() == "High":
                                self.shot_list.itemconfig(shot[0] - 1, bg = "#EFB462", selectbackground = "#997646")
                            elif cur_shot.getPriority() == "Medium":
                                self.shot_list.itemconfig(shot[0] - 1, bg = "#F4E255", selectbackground = "#9B9145")

                        else:
                            dialog = lambda: OkDialog.OkDialog(self.frame, "ERROR", "The shot " + shot[1] + " is not valid !", padding = 20)
                            self.frame.wait_window(dialog().top)

                self.previous_dirs = listdir(self.current_project.getDirectory() + "/05_shot/")

                self.frame.config(cursor = "")

    def stop(self):
        self.active = False
