#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import sys
from  cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
	base = "Win32GUI"

build_exe_options = {"packages": ["tkinter"], "include_files":["icon.ico"]}
executables = [Executable("Main.py", base = base, icon = "icon.ico")]

setup(name = "SuperPipe", version = "1.0", description = "Pipeline manager", options = {"build_exe": build_exe_options}, executables = executables)