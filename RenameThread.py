#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir
from Shot import *
from PIL import Image, ImageTk

import threading
import time

class UpdatePreviewShotsThread(threading.Thread):
	def __init__(self, current_project, datas):
		threading.Thread.__init__(self)
		self.current_project = current_project
		self.datas = datas

	def run(self):
		all_shots_preview = []

		for shot_dir in listdir(self.current_project.getDirectory() + "/05_shot/"):
			if shot_dir != "backup":
				all_picts_path = self.current_project.getDirectory() + "/05_shot/" + shot_dir + "/images/screenshots/"

				all_picts_path_array = []

				for f in listdir(all_picts_path):
					all_picts_path_array.append(all_picts_path + f)

				cur_shot = Shot(self.current_project.getDirectory(), shot_dir)

				if all_picts_path_array:
					all_shots_preview.append([cur_shot.getShotNb(), cur_shot.getShotName(), max(all_picts_path_array, key = path.getmtime)])
				else:
					all_shots_preview.append([cur_shot.getShotNb(), cur_shot.getShotName(), "assets/img/img_not_available.jpg"])

		self.datas.put(all_shots_preview)
