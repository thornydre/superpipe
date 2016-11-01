#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

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
        if shot_nb < 10:
            return "s0" + str(sequence) + "p0" + str(shot_nb)
        else:
            return "s0" + str(sequence) + "p" + str(shot_nb)

    def makeShotNbs(shot_name):
        return (int(shot_name[-2:]), int(shot_name[1:3]))

    def removeStudentVersion(file):
        with open(file, "r") as f:
            lines = f.readlines()
        f.close()

        new_lines = []

        for l in lines:
            if 'fileInfo "license" "student";' not in l:
                new_lines.append(l)

        with open(file, "w") as f:
            for l in new_lines:
                f.write(l)
        f.close()