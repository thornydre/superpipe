#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unicodedata
import string
import re

class Resources:
	def writeAtLine(file, text, line):
		with open(file, "r") as f:
			lines = f.readlines()
		f.close()

		if len(lines) < line:
			for i in range(line - len(lines)):
				lines.append("\n")

		lines[line - 1] = text + "\n"

		with open(file, "w") as f:
			for l in lines:
				f.write(l)
		f.close()

	def insertAtLine(file, text, line):
		if line == -1:
			with open(file, "a") as f:
				f.write(text)
			f.close()
		else:
			with open(file, "r") as f:
				lines = f.readlines()
			f.close()

			if len(lines) < line:
				for i in range(line - len(lines)):
					lines.append("\n")

			lines.insert(line, text + "\n")

			with open(file, "w") as f:
				for l in lines:
					f.write(l)
			f.close()

	def readLine(file, line):
		lines = []
		with open(file, "r") as f:
			for l in f:
				lines.append(l.strip("\n"))
		f.close()

		if line > len(lines):
			return False

		return lines[line - 1]

	def normString(data):
		str_array = re.split(r"[_ ]", data)

		new_str_array = []

		numbers = "0123456789"

		for word in str_array:
			new_word = "".join(e for e in word if e.isalnum())
			new_str_array.append(unicodedata.normalize("NFKD", new_word).encode("ASCII", "ignore").decode().lower())

		return "_".join(new_str_array)

	def getCategoryName(cat):
		if cat == 1:
			return "character"
		elif cat == 2:
			return "fx"
		elif cat == 3:
			return "props"
		elif cat == 4:
			return "set"

		return ""

	def makeShotName(shot_nb, sequence):
		seq_name = "s" + str(sequence).zfill(2)
		shot_name = "p" + str(shot_nb).zfill(3)

		return seq_name + shot_name

	def makeShotNbs(shot_name):
		return (int(shot_name[-3:]), int(shot_name[1:3]))

	def removeStudentVersion(file):
		with open(file, "r") as f:
			lines = f.readlines()
		f.close()

		new_lines = []

		corrected = False

		for l in lines:
			if corrected:
				new_lines.append(l)

			else:
				if 'fileInfo "license" "student";' in l:
					corrected = True
				if 'fileInfo "license" "education";' in l:
					corrected = True

				if not corrected:
					new_lines.append(l)

		with open(file, "w") as f:
			for l in new_lines:
				f.write(l)
		f.close()

	def resizeImage(img, size_limit):
		ori_width, ori_height = img.size

		new_width = size_limit
		new_height = size_limit

		if ori_width > ori_height:
			new_height = round(new_width / ori_width * ori_height)
		elif ori_height > ori_width:
			new_width = round(new_height / ori_height * ori_width)

		resized_img = img.resize((new_width, new_height))

		return resized_img
