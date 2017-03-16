#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from watchdog.events import FileSystemEventHandler

class ListsObserver(FileSystemEventHandler):
    def __init__(self, list_to_update, path_to_oberve):
        self.shot_list = list_to_update
        self.path = path_to_oberve

    def on_created(self, event):
        print("created")
        # self.shot_list.delete(0, END)

        # shots = listdir(self.path)

        # for shot in shots:
        #     self.shot_list.insert(END, shot)

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