#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import sys
import os
from  cx_Freeze import setup, Executable

os.environ["TCL_LIBRARY"] = "C:\\Users\\thornydre\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tcl8.6"
os.environ["TK_LIBRARY"] = "C:\\Users\\thornydre\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tk8.6"

base = None

# if sys.platform == "win32":
# 	base = "Win32GUI"

build_exe_options = {"packages": ["tkinter"], "include_files":["img/icon.ico"]}
executables = [Executable("Main.py", base = base, icon = "img/icon.ico")]

setup(name = "SuperPipe", version = "1.0", description = "Pipeline manager", options = {"build_exe": build_exe_options}, executables = executables)
