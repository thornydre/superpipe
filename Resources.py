#!/usr/bin/python

import unicodedata
import re

class Resources:
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


	def normString(data):
		str_array = re.split(r"[_ ]", data)

		new_str_array = []

		numbers = "0123456789"

		for word in str_array:
			new_word = "".join(e for e in word if e.isalnum())
			new_str_array.append(unicodedata.normalize("NFKD", new_word).encode("ASCII", "ignore").decode().lower())

		return "_".join(new_str_array)


	def makeShotName(shot_nb, sequence):
		seq_name = "s" + str(sequence).zfill(2)
		shot_name = "p" + str(shot_nb).zfill(3)

		return seq_name + shot_name


	def makeShotNbs(shot_name):
		return (int(shot_name[-3:]), int(shot_name[1:3]))
