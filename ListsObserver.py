#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from tkinter import *
from watchdog.events import FileSystemEventHandler
from os import path
from Shot import *

class ListsObserver(FileSystemEventHandler):
    def __init__(self, current_project, list_to_update, path_to_oberve):
        self.current_project = current_project
        self.shot_list = list_to_update
        self.path = path_to_oberve

    def on_created(self, event):
        print("created")
        self.current_project.updateShotList()
        
        self.shot_list.delete(0, END)

        shots = self.current_project.getShotList()

        for shot in shots:
            if path.isdir(self.current_project.getDirectory() + "/05_shot/" + shot[1] + "/superpipe"):
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
                dialog = lambda: OkDialog.OkDialog(self.parent, "ERROR", "The shot " + shot[1] + " has a problem !", padding = 20)

    def on_moved(self, event):
        print("moved")
        # self.shot_list.delete(0, END)

        # shots = listdir(self.path)

        # for shot in shots:
        #     self.shot_list.insert(END, shot)

    def on_deleted(self, event):
        print("deleted")
        # self.shot_list.delete(0, END)

        # shots = listdir(self.path)

        # for shot in shots:
        #     self.shot_list.insert(END, shot)